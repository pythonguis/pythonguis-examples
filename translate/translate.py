from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from MainWindow import Ui_MainWindow

try:
    from googletrans import Translator
    GOOGLE_TRANSLATE_AVAILABLE = True

except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

import json
from urllib import parse
import requests

LANGUAGES = {
    '<Detect language>': None,
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Arabic': 'ar',
    'Azerbaijani': 'az',
    'Basque': 'eu',
    'Bengali': 'bn',
    'Belarusian': 'be',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Chinese Simplified': 'zh-CN',
    'Chinese Traditional': 'zh-TW',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Filipino': 'tl',
    'Finnish': 'fi',
    'French': 'fr',
    'Galician': 'gl',
    'Georgian': 'ka',
    'German': 'de',
    'Greek': 'el',
    'Gujarati': 'gu',
    'Haitian Creole': 'ht',
    'Hebrew': 'iw',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Kannada': 'kn',
    'Korean': 'ko',
    'Latin': 'la',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Macedonian': 'mk',
    'Malay': 'ms',
    'Maltese': 'mt',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Yiddish': 'yi'
}


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.translator = Translator()

        self.destTextEdit.setReadOnly(True)

        if GOOGLE_TRANSLATE_AVAILABLE:
            self.srcLanguage.addItems(LANGUAGES.keys())
            self.srcLanguage.currentTextChanged[str].connect(self.update_src_language)
            self.srcLanguage.setCurrentText('English')
        else:
            self.srcLanguage.hide()

        self.translateButton.pressed.connect(self.translate)

        self.show()

    def update_src_language(self, l):
        self.language_src = LANGUAGES[l]

    def google_translate(self, text):
        params = dict(
            dest='en',
            text=text
        )

        if self.language_src:
            params['src'] = self.language_src

        try:
            tr = self.translator.translate(**params)

        except Exception:
            self.destTextEdit.setPlainText('Google translate error :(. Try translating from English')
            return False

        else:
            return tr.text

    def translate(self):
        # Perform pre-translation to English via Google Translate.
        if self.language_src != 'en':
            text = self.google_translate(self.srcTextEdit.toPlainText())
            if not text:
                return False

        # Already in English.
        else:
            text = self.srcTextEdit.toPlainText()

        # Perform translation to piraat.
        r = requests.get(
            'http://api.funtranslations.com/translate/pirate.json?%s' %
            parse.urlencode({'text': text})
        )

        data = json.loads(r.text)
        if 'error' in data:
            self.destTextEdit.setPlainText("%s\n\n%s" % (data['error']['message'], text))
        else:
            self.destTextEdit.setPlainText(data['contents']['translated'])



if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()