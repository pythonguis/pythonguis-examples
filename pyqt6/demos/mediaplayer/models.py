from PyQt6.QtCore import QAbstractListModel, Qt


class PlaylistModel(QAbstractListModel):
    def __init__(self, playlist):
        super().__init__()
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()
