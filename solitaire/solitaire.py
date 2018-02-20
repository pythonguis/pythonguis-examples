from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os
import random

WINDOW_SIZE = 840, 600

CARD_DIMENSIONS = QSize(80, 116)
CARD_RECT = QRect(0, 0, 80, 116)
CARD_SPACING_X = 110
CARD_BACK = QImage(os.path.join('images', 'back.png'))

DEAL_RECT = QRect(30, 30, 110, 140)

OFFSET_X = 50
OFFSET_Y = 50
WORK_STACK_Y = 200

SIDE_FACE = 0
SIDE_BACK = 1

BOUNCE_ENERGY = 0.8

# We store cards as numbers 1-13, since we only need
# to know their order for solitaire.
SUITS = ["C", "S", "H", "D"]


class Signals(QObject):
    complete = pyqtSignal()
    clicked = pyqtSignal()
    doubleclicked = pyqtSignal()


class Card(QGraphicsPixmapItem):

    def __init__(self, value, suit, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)

        self.signals = Signals()

        self.stack = None  # Stack this card currently is in.
        self.child = None  # Card stacked on this one (for work deck).

        # Store the value & suit of the cards internal to it.
        self.value = value
        self.suit = suit
        self.side = None

        # For end animation only.
        self.vector = None

        # Cards have no internal transparent areas, so we can use this faster method.
        self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

        self.load_images()

    def load_images(self):
        self.face = QPixmap(
            os.path.join('cards', '%s%s.png' % (self.value, self.suit))
        )

        self.back = QPixmap(
            os.path.join('images', 'back.png')
        )

    def turn_face_up(self):
        self.side = SIDE_FACE
        self.setPixmap(self.face)

    def turn_back_up(self):
        self.side = SIDE_BACK
        self.setPixmap(self.back)

    @property
    def is_face_up(self):
        return self.side == SIDE_FACE

    @property
    def color(self):
        return 'r' if self.suit in ('H', 'D') else 'b'

    def mousePressEvent(self, e):
        if not self.is_face_up and self.stack.cards[-1] == self:
            self.turn_face_up()  # We can do this without checking.
            e.accept()
            return

        if self.stack and not self.stack.is_free_card(self):
            e.ignore()
            return

        self.stack.activate()

        e.accept()

        super(Card, self).mouseReleaseEvent(e)

    def mouseReleaseEvent(self, e):
        self.stack.deactivate()

        items = self.collidingItems()
        if items:
            # Find the topmost item from a different stack:
            for item in items:
                if ((isinstance(item, Card) and item.stack != self.stack) or
                    (isinstance(item, StackBase) and item != self.stack)):

                    if item.stack.is_valid_drop(self):
                        # Remove card + all children from previous stack, add to the new.
                        # Note: the only place there will be children is on a workstack.
                        cards = self.stack.remove_card(self)
                        item.stack.add_cards(cards)
                        break

        # Refresh this card's stack, pulling it back if it was dropped.
        self.stack.update()

        super(Card, self).mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, e):
        if self.stack.is_free_card(self):
            self.signals.doubleclicked.emit()
            e.accept()

        super(Card, self).mouseDoubleClickEvent(e)


class StackBase(QGraphicsRectItem):

    def __init__(self, *args, **kwargs):
        super(StackBase, self).__init__(*args, **kwargs)

        self.setRect(QRectF(CARD_RECT))
        self.setZValue(-1)

        # Cards on this deck, in order.
        self.cards = []

        # Store a self ref, so the collision logic can handle cards and
        # stacks with the same approach.
        self.stack = self
        self.setup()
        self.reset()

    def setup(self):
        pass

    def reset(self):
        self.remove_all_cards()

    def update(self):
        for n, card in enumerate(self.cards):
            card.setPos( self.pos() + QPointF(n * self.offset_x, n * self.offset_y))
            card.setZValue(n)

    def activate(self):
        pass

    def deactivate(self):
        pass

    def add_card(self, card, update=True):
        card.stack = self
        self.cards.append(card)
        if update:
            self.update()

    def add_cards(self, cards):
        for card in cards:
            self.add_card(card, update=False)
        self.update()

    def remove_card(self, card):
        card.stack = None
        self.cards.remove(card)
        self.update()
        return [card] # Returns a list, as WorkStack must return children

    def remove_all_cards(self):
        for card in self.cards[:]:
            card.stack = None
        self.cards = []

    def is_valid_drop(self, card):
        return True

    def is_free_card(self, card):
        return False


class DeckStack(StackBase):

    offset_x = -0.2
    offset_y = -0.3

    restack_counter = 0

    def reset(self):
        super(DeckStack, self).reset()
        self.restack_counter = 0
        self.set_color(Qt.green)

    def stack_cards(self, cards):
        for card in cards:
            self.add_card(card)
            card.turn_back_up()

    def can_restack(self, n_rounds=3):
        return n_rounds is None or self.restack_counter < n_rounds-1

    def update_stack_status(self, n_rounds):
        if not self.can_restack(n_rounds):
            self.set_color(Qt.red)
        else:
            # We only need this if players change the round number during a game.
            self.set_color(Qt.green)

    def restack(self, fromstack):
        self.restack_counter += 1

        # We need to slice as we're adding to the list, reverse to stack back
        # in the original order.
        for card in fromstack.cards[::-1]:
            fromstack.remove_card(card)
            self.add_card(card)
            card.turn_back_up()

    def take_top_card(self):
        try:
            card = self.cards[-1]
            self.remove_card(card)
            return card
        except IndexError:
            pass

    def set_color(self, color):
        color = QColor(color)
        color.setAlpha(50)
        brush = QBrush(color)
        self.setBrush(brush)
        self.setPen(QPen(Qt.NoPen))

    def is_valid_drop(self, card):
        return False


class DealStack(StackBase):

    offset_x = 20
    offset_y = 0

    spread_from = 0

    def setup(self):
        self.setPen(QPen(Qt.NoPen))
        color = QColor(Qt.black)
        color.setAlpha(50)
        brush = QBrush(color)
        self.setBrush(brush)

    def reset(self):
        super(DealStack, self).reset()
        self.spread_from = 0  # Card index to start spreading cards out.

    def is_valid_drop(self, card):
        return False

    def is_free_card(self, card):
        return card == self.cards[-1]

    def update(self):
        # Only spread the top 3 cards
        offset_x = 0
        for n, card in enumerate(self.cards):
            card.setPos(self.pos() + QPointF(offset_x, 0))
            card.setZValue(n)

            if n >= self.spread_from:
                offset_x = offset_x + self.offset_x


class WorkStack(StackBase):

    offset_x = 0
    offset_y = 15
    offset_y_back = 5

    def setup(self):
        self.setPen(QPen(Qt.NoPen))
        color = QColor(Qt.black)
        color.setAlpha(50)
        brush = QBrush(color)
        self.setBrush(brush)

    def activate(self):
        # Raise z-value of this stack so children float above all other cards.
        self.setZValue(1000)

    def deactivate(self):
        self.setZValue(-1)

    def is_valid_drop(self, card):
        if not self.cards:
            return True

        if (card.color != self.cards[-1].color and
            card.value == self.cards[-1].value -1):
            return True

        return False

    def is_free_card(self, card):
        return card.is_face_up #self.cards and card == self.cards[-1]

    def add_card(self, card, update=True):
        if self.cards:
            card.setParentItem(self.cards[-1])
        else:
            card.setParentItem(self)

        super(WorkStack, self).add_card(card, update=update)

    def remove_card(self, card):
        index = self.cards.index(card)
        self.cards, cards = self.cards[:index], self.cards[index:]

        for card in cards:
            # Remove card and all children, returning a list of cards removed in order.
            card.setParentItem(None)
            card.stack = None

        self.update()
        return cards

    def remove_all_cards(self):
        for card in self.cards[:]:
            card.setParentItem(None)
            card.stack = None
        self.cards = []

    def update(self):
        self.stack.setZValue(-1) # Reset this stack the the background.
        # Only spread the top 3 cards
        offset_y = 0
        for n, card in enumerate(self.cards):
            card.setPos(QPointF(0, offset_y))

            if card.is_face_up:
                offset_y = self.offset_y
            else:
                offset_y = self.offset_y_back


class DropStack(StackBase):

    offset_x = -0.2
    offset_y = -0.3

    suit = None
    value = 0

    def setup(self):
        self.signals = Signals()
        color = QColor(Qt.blue)
        color.setAlpha(50)
        pen = QPen(color)
        pen.setWidth(5)
        self.setPen(pen)

    def reset(self):
        super(DropStack, self).reset()
        self.suit = None
        self.value = 0

    def is_valid_drop(self, card):
        if ((self.suit is None or card.suit == self.suit) and
                (card.value == self.value + 1)):
            return True

        return False

    def add_card(self, card, update=True):
        super(DropStack, self).add_card(card, update=update)
        self.suit = card.suit
        self.value = self.cards[-1].value

        if self.is_complete:
            self.signals.complete.emit()

    def remove_card(self, card):
        super(DropStack, self).remove_card(card)
        self.value = self.cards[-1].value if self.cards else 0

    @property
    def is_complete(self):
        return self.value == 13


class DealTrigger(QGraphicsRectItem):

    def __init__(self, *args, **kwargs):
        super(DealTrigger, self).__init__(*args, **kwargs)
        self.setRect(QRectF(DEAL_RECT))
        self.setZValue(1000)

        pen = QPen(Qt.NoPen)
        self.setPen(pen)

        self.signals = Signals()

    def mousePressEvent(self, e):
        self.signals.clicked.emit()


class AnimationCover(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(AnimationCover, self).__init__(*args, **kwargs)
        self.setRect(QRectF(0, 0, *WINDOW_SIZE))
        self.setZValue(5000)
        pen = QPen(Qt.NoPen)
        self.setPen(pen)

    def mousePressEvent(self, e):
        e.accept()


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(QRectF(0, 0, *WINDOW_SIZE))

        felt = QBrush(QPixmap(os.path.join('images','felt.png')))
        self.scene.setBackgroundBrush(felt)

        name = QGraphicsPixmapItem()
        name.setPixmap(QPixmap(os.path.join('images','ronery.png')))
        name.setPos(QPointF(170, 375))
        self.scene.addItem(name)

        view.setScene(self.scene)

        # Timer for the win animation only.
        self.timer = QTimer()
        self.timer.setInterval(5)
        self.timer.timeout.connect(self.win_animation)

        self.animation_event_cover = AnimationCover()
        self.scene.addItem(self.animation_event_cover)

        menu = self.menuBar().addMenu("&Game")

        deal_action = QAction(QIcon(os.path.join('images', 'playing-card.png')), "Deal...", self)
        deal_action.triggered.connect(self.restart_game)
        menu.addAction(deal_action)

        menu.addSeparator()

        deal1_action = QAction("1 card", self)
        deal1_action.setCheckable(True)
        deal1_action.triggered.connect(lambda: self.set_deal_n(1))
        menu.addAction(deal1_action)

        deal3_action = QAction("3 card", self)
        deal3_action.setCheckable(True)
        deal3_action.setChecked(True)
        deal3_action.triggered.connect(lambda: self.set_deal_n(3))

        menu.addAction(deal3_action)

        dealgroup = QActionGroup(self)
        dealgroup.addAction(deal1_action)
        dealgroup.addAction(deal3_action)
        dealgroup.setExclusive(True)

        menu.addSeparator()

        rounds3_action = QAction("3 rounds", self)
        rounds3_action.setCheckable(True)
        rounds3_action.setChecked(True)
        rounds3_action.triggered.connect(lambda: self.set_rounds_n(3))
        menu.addAction(rounds3_action)

        rounds5_action = QAction("5 rounds", self)
        rounds5_action.setCheckable(True)
        rounds5_action.triggered.connect(lambda: self.set_rounds_n(5))
        menu.addAction(rounds5_action)

        roundsu_action = QAction("Unlimited rounds", self)
        roundsu_action.setCheckable(True)
        roundsu_action.triggered.connect(lambda: self.set_rounds_n(None))
        menu.addAction(roundsu_action)

        roundgroup = QActionGroup(self)
        roundgroup.addAction(rounds3_action)
        roundgroup.addAction(rounds5_action)
        roundgroup.addAction(roundsu_action)
        roundgroup.setExclusive(True)

        menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit)
        menu.addAction(quit_action)

        self.deck = []
        self.deal_n = 3  # Number of cards to deal each time
        self.rounds_n = 3  # Number of rounds (restacks) before end.

        for suit in SUITS:
            for value in range(1, 14):
                card = Card(value, suit)
                self.deck.append(card)
                self.scene.addItem(card)
                card.signals.doubleclicked.connect(lambda card=card: self.auto_drop_card(card))

        self.setCentralWidget(view)
        self.setFixedSize(*WINDOW_SIZE)

        self.deckstack = DeckStack()
        self.deckstack.setPos(OFFSET_X, OFFSET_Y)
        self.scene.addItem(self.deckstack)

        # Set up the working locations.
        self.works = []
        for n in range(7):
            stack = WorkStack()
            stack.setPos(OFFSET_X + CARD_SPACING_X*n, WORK_STACK_Y)
            self.scene.addItem(stack)
            self.works.append(stack)

        self.drops = []
        # Set up the drop locations.
        for n in range(4):
            stack = DropStack()
            stack.setPos(OFFSET_X + CARD_SPACING_X * (3+n), OFFSET_Y)
            stack.signals.complete.connect(self.check_win_condition)

            self.scene.addItem(stack)
            self.drops.append(stack)

        # Add the deal location.
        self.dealstack = DealStack()
        self.dealstack.setPos(OFFSET_X + CARD_SPACING_X, OFFSET_Y)
        self.scene.addItem(self.dealstack)

        # Add the deal click-trigger.
        dealtrigger = DealTrigger()
        dealtrigger.signals.clicked.connect(self.deal)
        self.scene.addItem(dealtrigger)

        self.shuffle_and_stack()

        self.setWindowTitle("Ronery")
        self.show()

    def restart_game(self):
        reply = QMessageBox.question(self, "Deal again", "Are you sure you want to start a new game?",
                                      QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.shuffle_and_stack()

    def quit(self):
        self.close()

    def set_deal_n(self, n):
        self.deal_n = n

    def set_rounds_n(self, n):
        self.rounds_n = n
        self.deckstack.update_stack_status(self.rounds_n)

    def shuffle_and_stack(self):
        # Stop any ongoing animation.
        self.timer.stop()
        self.animation_event_cover.hide()

        # Remove cards from all stacks.
        for stack in [self.deckstack, self.dealstack] + self.drops + self.works:
            stack.reset()

        random.shuffle(self.deck)

        # Deal out from the top of the deck, turning over the
        # final card on each line.
        cards = self.deck[:]
        for n, workstack in enumerate(self.works, 1):
            for a in range(n):
                card = cards.pop()
                workstack.add_card(card)
                card.turn_back_up()
                if a == n-1:
                    card.turn_face_up()

        # Ensure removed from all other stacks here.
        self.deckstack.stack_cards(cards)

    def deal(self):
        if self.deckstack.cards:
            self.dealstack.spread_from = len(self.dealstack.cards)
            for n in range(self.deal_n):
                card = self.deckstack.take_top_card()
                if card:
                    self.dealstack.add_card(card)
                    card.turn_face_up()

        elif self.deckstack.can_restack(self.rounds_n):
            self.deckstack.restack(self.dealstack)
            self.deckstack.update_stack_status(self.rounds_n)

    def auto_drop_card(self, card):
        for stack in self.drops:
            if stack.is_valid_drop(card):
                card.stack.remove_card(card)
                stack.add_card(card)
                break

    def check_win_condition(self):
        complete = all(s.is_complete for s in self.drops)
        if complete:
            # Add click-proof cover to play area.
            self.animation_event_cover.show()
            # Get the stacks of cards from the drop,stacks.
            self.timer.start()

    def win_animation(self):
        # Start off a new card
        for drop in self.drops:
            if drop.cards:
                card = drop.cards.pop()
                if card.vector is None:
                    card.vector = QPoint(-random.randint(3, 10), -random.randint(0, 10))
                    break

        for card in self.deck:
            if card.vector is not None:
                card.setPos(card.pos() + card.vector)
                card.vector += QPoint(0, 1)  # Gravity
                if card.pos().y() > WINDOW_SIZE[1] - CARD_DIMENSIONS.height():
                    # Bounce the card, losing some energy.
                    card.vector = QPoint(card.vector.x(), -max(1, int(card.vector.y() * BOUNCE_ENERGY)) )
                    # Bump back up to base of screen.
                    card.setPos(card.pos().x(), WINDOW_SIZE[1] - CARD_DIMENSIONS.height())

                if card.pos().x() < - CARD_DIMENSIONS.width():
                    card.vector = None
                    # Put the card back where it started.
                    card.stack.add_card(card)





if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()