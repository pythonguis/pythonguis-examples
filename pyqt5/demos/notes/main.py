import sys

from MainWindow import Ui_MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
)
from PyQt6.QtGui import QColor, QPalette
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Note(Base):
    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    text = Column(String(1000), nullable=False)
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)


engine = create_engine("sqlite:///notes.db")
# Initalize the database if it is not already.
# if not engine.dialect.has_table(engine, "note"):
Base.metadata.create_all(engine)

# Create a session to handle updates.
Session = sessionmaker(bind=engine)
session = Session()

_ACTIVE_NOTES = {}


def create_new_note():
    MainWindow()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, obj=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.show()

        # Load/save note data, store this notes db reference.
        if obj:
            self.obj = obj
            self.load()
        else:
            self.obj = Note()
            self.save()

        self.closeButton.pressed.connect(self.delete_window)
        self.moreButton.pressed.connect(create_new_note)
        self.textEdit.textChanged.connect(self.save)

        # Flags to store dragged-dropped
        self._drag_active = False

    def load(self):
        self.move(self.obj.x, self.obj.y)
        self.textEdit.setHtml(self.obj.text)
        _ACTIVE_NOTES[self.obj.id] = self

    def save(self):
        self.obj.x = self.x()
        self.obj.y = self.y()
        self.obj.text = self.textEdit.toHtml()
        session.add(self.obj)
        session.commit()
        _ACTIVE_NOTES[self.obj.id] = self

    def mousePressEvent(self, e):
        self.previous_pos = e.globalPos()

    def mouseMoveEvent(self, e):
        delta = e.globalPos() - self.previous_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.previous_pos = e.globalPos()

        self._drag_active = True

    def mouseReleaseEvent(self, e):
        if self._drag_active:
            self.save()
            self._drag_active = False

    def delete_window(self):
        result = QMessageBox.question(
            self,
            "Confirm delete",
            "Are you sure you want to delete this note?",
        )
        if result == QMessageBox.StandardButton.Yes:
            session.delete(self.obj)
            session.commit()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Brown Note")
    app.setStyle("Fusion")

    # Custom brown palette.
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(188, 170, 164))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(121, 85, 72))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(121, 85, 72))
    palette.setColor(QPalette.ColorRole.Text, QColor(121, 85, 72))
    palette.setColor(QPalette.ColorRole.Base, QColor(188, 170, 164))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(188, 170, 164))
    app.setPalette(palette)

    existing_notes = session.query(Note).all()
    if len(existing_notes) == 0:
        MainWindow()
    else:
        for note in existing_notes:
            MainWindow(obj=note)

    app.exec_()
