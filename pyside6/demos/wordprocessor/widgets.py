import constants
import utils
from PySide6.QtGui import QFont, QImage, QTextDocument
from PySide6.QtWidgets import QTextEdit


class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setAutoFormatting(QTextEdit.AutoFormattingFlag.AutoAll)
        # Initialize default font size.
        font = QFont("Times", 12)
        self.setFont(font)
        # We need to repeat the size to init the current format.
        self.setFontPointSize(12)

    def canInsertFromMimeData(self, source):
        if source.hasImage():
            return True
        else:
            return super().canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        cursor = self.textCursor()
        document = self.document()

        if source.hasUrls():
            for u in source.urls():
                file_ext = utils.splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in constants.IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(
                        QTextDocument.ResourceType.ImageResource, u, image
                    )
                    cursor.insertImage(u.toLocalFile())

                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break

            else:
                # If all were valid images, finish here.
                return

        elif source.hasImage():
            image = source.imageData()
            uuid = utils.hexuuid()
            document.addResource(QTextDocument.ResourceType.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return

        super().insertFromMimeData(source)
