import os

import constants
from PySide2.QtCore import QObject, QPointF, QRectF, Qt, Signal
from PySide2.QtGui import QBrush, QColor, QPen, QPixmap
from PySide2.QtWidgets import (
    QGraphicsItem,
    QGraphicsPixmapItem,
    QGraphicsRectItem,
)


class Signals(QObject):
    complete = Signal()
    clicked = Signal()
    doubleclicked = Signal()


class Card(QGraphicsPixmapItem):
    def __init__(self, value, suit):
        super().__init__()

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
        self.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

        self.load_images()

    def load_images(self):
        self.face = QPixmap(os.path.join("cards", "%s%s.png" % (self.value, self.suit)))

        self.back = QPixmap(os.path.join("images", "back.png"))

    def turn_face_up(self):
        self.side = constants.SIDE_FACE
        self.setPixmap(self.face)

    def turn_back_up(self):
        self.side = constants.SIDE_BACK
        self.setPixmap(self.back)

    @property
    def is_face_up(self):
        return self.side == constants.SIDE_FACE

    @property
    def color(self):
        return "r" if self.suit in ("H", "D") else "b"

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

        super().mouseReleaseEvent(e)

    def mouseReleaseEvent(self, e):
        self.stack.deactivate()

        items = self.collidingItems()
        if items:
            # Find the topmost item from a different stack:
            for item in items:
                if (isinstance(item, Card) and item.stack != self.stack) or (
                    isinstance(item, StackBase) and item != self.stack
                ):
                    if item.stack.is_valid_drop(self):
                        # Remove card + all children from previous stack, add to the new.
                        # Note: the only place there will be children is on a workstack.
                        cards = self.stack.remove_card(self)
                        item.stack.add_cards(cards)
                        break

        # Refresh this card's stack, pulling it back if it was dropped.
        self.stack.update()

        super().mouseReleaseEvent(e)

    def mouseDoubleClickEvent(self, e):
        if self.stack.is_free_card(self):
            self.signals.doubleclicked.emit()
            e.accept()

        super().mouseDoubleClickEvent(e)


class StackBase(QGraphicsRectItem):
    def __init__(self):
        super().__init__()

        self.setRect(QRectF(constants.CARD_RECT))
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
            card.setPos(self.pos() + QPointF(n * self.offset_x, n * self.offset_y))
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
        return [card]  # Returns a list, as WorkStack must return children

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
        super().reset()
        self.restack_counter = 0
        self.set_color(Qt.GlobalColor.green)

    def stack_cards(self, cards):
        for card in cards:
            self.add_card(card)
            card.turn_back_up()

    def can_restack(self, n_rounds=3):
        return n_rounds is None or self.restack_counter < n_rounds - 1

    def update_stack_status(self, n_rounds):
        if not self.can_restack(n_rounds):
            self.set_color(Qt.GlobalColor.red)
        else:
            # We only need this if players change the round number during a game.
            self.set_color(Qt.GlobalColor.green)

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
        self.setPen(QPen(Qt.PenStyle.NoPen))

    def is_valid_drop(self, card):
        return False


class DealStack(StackBase):
    offset_x = 20
    offset_y = 0

    spread_from = 0

    def setup(self):
        self.setPen(QPen(Qt.PenStyle.NoPen))
        color = QColor(Qt.GlobalColor.black)
        color.setAlpha(50)
        brush = QBrush(color)
        self.setBrush(brush)

    def reset(self):
        super().reset()
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
        self.setPen(QPen(Qt.PenStyle.NoPen))
        color = QColor(Qt.GlobalColor.black)
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

        if card.color != self.cards[-1].color and card.value == self.cards[-1].value - 1:
            return True

        return False

    def is_free_card(self, card):
        return card.is_face_up  # self.cards and card == self.cards[-1]

    def add_card(self, card, update=True):
        if self.cards:
            card.setParentItem(self.cards[-1])
        else:
            card.setParentItem(self)

        super().add_card(card, update=update)

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
        self.stack.setZValue(-1)  # Reset this stack the the background.
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
        color = QColor(Qt.GlobalColor.blue)
        color.setAlpha(50)
        pen = QPen(color)
        pen.setWidth(5)
        self.setPen(pen)

    def reset(self):
        super().reset()
        self.suit = None
        self.value = 0

    def is_valid_drop(self, card):
        if (self.suit is None or card.suit == self.suit) and (card.value == self.value + 1):
            return True

        return False

    def add_card(self, card, update=True):
        super().add_card(card, update=update)
        self.suit = card.suit
        self.value = self.cards[-1].value

        if self.is_complete:
            self.signals.complete.emit()

    def remove_card(self, card):
        super().remove_card(card)
        self.value = self.cards[-1].value if self.cards else 0

    @property
    def is_complete(self):
        return self.value == 13


class DealTrigger(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.setRect(QRectF(constants.DEAL_RECT))
        self.setZValue(1000)

        pen = QPen(Qt.PenStyle.NoPen)
        self.setPen(pen)

        self.signals = Signals()

    def mousePressEvent(self, e):
        self.signals.clicked.emit()


class AnimationCover(QGraphicsRectItem):
    def __init__(self):
        super().__init__()
        self.setRect(QRectF(0, 0, *constants.WINDOW_SIZE))
        self.setZValue(5000)
        pen = QPen(Qt.PenStyle.NoPen)
        self.setPen(pen)

    def mousePressEvent(self, e):
        e.accept()
