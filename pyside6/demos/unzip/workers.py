import os
import sys
import traceback
import zipfile

from PySide6.QtCore import (
    QObject,
    QRunnable,
    Signal,
    Slot,
)

EXCLUDE_PATHS = [
    "__MACOSX/",
]


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """

    finished = Signal()
    error = Signal(tuple)
    progress = Signal(float)


class UnzipWorker(QRunnable):
    """
    Worker thread for unzipping.
    """

    signals = WorkerSignals()

    def __init__(self, path):
        super().__init__()
        os.chdir(os.path.dirname(path))
        self.zipfile = zipfile.ZipFile(path)

    @Slot()
    def run(self):
        try:
            items = self.zipfile.infolist()
            total_n = len(items)

            for n, item in enumerate(items, 1):
                if not any(item.filename.startswith(p) for p in EXCLUDE_PATHS):
                    self.zipfile.extract(item)

                self.signals.progress.emit(n / total_n)

        except Exception:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
            return

        self.signals.finished.emit()
