from MainWindow import Ui_MainWindow
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
)

try:
    from googletrans import Translator

    GOOGLE_TRANSLATE_AVAILABLE = True

except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

import json
import sys
from urllib import parse

import constants
import requests


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.translator = Translator()

        self.destTextEdit.setReadOnly(True)

        if GOOGLE_TRANSLATE_AVAILABLE:
            self.srcLanguage.addItems(constants.AVAILABLE_LANGUAGES.keys())
            self.srcLanguage.currentTextChanged[str].connect(self.update_src_language)
            self.srcLanguage.setCurrentText("English")
        else:
            self.srcLanguage.hide()

        self.translateButton.pressed.connect(self.translate)

        self.show()

    def update_src_language(self, l):
        self.language_src = constants.AVAILABLE_LANGUAGES[l]

    def google_translate(self, text):
        params = dict(dest="en", text=text)

        if self.language_src:
            params["src"] = self.language_src

        try:
            tr = self.translator.translate(**params)

        except Exception:
            self.destTextEdit.setPlainText("Google translate error :(. Try translating from English")
            return False

        else:
            return tr.text

    def translate(self):
        # Perform pre-translation to English via Google Translate.
        if self.language_src != "en":
            text = self.google_translate(self.srcTextEdit.toPlainText())
            if not text:
                return False

        # Already in English.
        else:
            text = self.srcTextEdit.toPlainText()

        # Perform translation to piraat.
        r = requests.get("http://api.funtranslations.com/translate/pirate.json?%s" % parse.urlencode({"text": text}))

        data = json.loads(r.text)
        if "error" in data:
            self.destTextEdit.setPlainText("%s\n\n%s" % (data["error"]["message"], text))
        else:
            self.destTextEdit.setPlainText(data["contents"]["translated"])


if __name__ == "__main__":
    app = QApplication(sys.args)
    window = MainWindow()
    app.exec()
