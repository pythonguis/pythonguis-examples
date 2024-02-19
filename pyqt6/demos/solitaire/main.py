import os
import random
import sys

import constants
from items import (
    AnimationCover,
    Card,
    DealStack,
    DealTrigger,
    DeckStack,
    DropStack,
    WorkStack,
)
from PyQt6.QtCore import (
    QPoint,
    QPointF,
    QRectF,
    Qt,
    QTimer,
)
from PyQt6.QtGui import (
    QAction,
    QActionGroup,
    QBrush,
    QIcon,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
    QMessageBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        view = QGraphicsView()
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(
            QRectF(0, 0, constants.WINDOW_SIZE[0] - 10, constants.WINDOW_SIZE[1] - 50)
        )

        felt = QBrush(QPixmap(os.path.join("images", "felt.png")))
        self.scene.setBackgroundBrush(felt)

        name = QGraphicsPixmapItem()
        name.setPixmap(QPixmap(os.path.join("images", "name.png")))
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

        deal_action = QAction(
            QIcon(os.path.join("images", "playing-card.png")),
            "Deal...",
            self,
        )
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

        for suit in constants.SUITS:
            for value in range(1, 14):
                card = Card(value, suit)
                self.deck.append(card)
                self.scene.addItem(card)
                card.signals.doubleclicked.connect(
                    lambda card=card: self.auto_drop_card(card)
                )

        self.setCentralWidget(view)
        self.setFixedSize(*constants.WINDOW_SIZE)

        self.deckstack = DeckStack()
        self.deckstack.setPos(constants.OFFSET_X, constants.OFFSET_Y)
        self.scene.addItem(self.deckstack)

        # Set up the working locations.
        self.works = []
        for n in range(7):
            stack = WorkStack()
            stack.setPos(
                constants.OFFSET_X + constants.CARD_SPACING_X * n,
                constants.WORK_STACK_Y,
            )
            self.scene.addItem(stack)
            self.works.append(stack)

        self.drops = []
        # Set up the drop locations.
        for n in range(4):
            stack = DropStack()
            stack.setPos(
                constants.OFFSET_X + constants.CARD_SPACING_X * (3 + n),
                constants.OFFSET_Y,
            )
            stack.signals.complete.connect(self.check_win_condition)

            self.scene.addItem(stack)
            self.drops.append(stack)

        # Add the deal location.
        self.dealstack = DealStack()
        self.dealstack.setPos(
            constants.OFFSET_X + constants.CARD_SPACING_X, constants.OFFSET_Y
        )
        self.scene.addItem(self.dealstack)

        # Add the deal click-trigger.
        dealtrigger = DealTrigger()
        dealtrigger.signals.clicked.connect(self.deal)
        self.scene.addItem(dealtrigger)

        self.shuffle_and_stack()

        self.setWindowTitle("Saltaire")
        self.show()

    def restart_game(self):
        reply = QMessageBox.question(
            self,
            "Deal again",
            "Are you sure you want to start a new game?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
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
                if a == n - 1:
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
                if (
                    card.pos().y()
                    > constants.WINDOW_SIZE[1] - constants.CARD_DIMENSIONS.height()
                ):
                    # Bounce the card, losing some energy.
                    card.vector = QPoint(
                        card.vector.x(),
                        -max(1, int(card.vector.y() * constants.BOUNCE_ENERGY)),
                    )
                    # Bump back up to base of screen.
                    card.setPos(
                        card.pos().x(),
                        constants.WINDOW_SIZE[1] - constants.CARD_DIMENSIONS.height(),
                    )

                if card.pos().x() < -constants.CARD_DIMENSIONS.width():
                    card.vector = None
                    # Put the card back where it started.
                    card.stack.add_card(card)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
