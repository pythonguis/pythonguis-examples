import os
import sys

from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QShortcut
from PySide6.QtPrintSupport import QPrintPreviewDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
)


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        QBtn = QDialogButtonBox.StandardButton.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("MooseAche")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join("images", "ma-icon-128.png")))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 23.35.211.233232"))
        layout.addWidget(QLabel("Copyright 2015 MooseAche Inc."))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://google.com"))

        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        self.shortcut_open = QShortcut(QKeySequence("F5"), self)
        self.shortcut_open.activated.connect(self.browser.reload)

        back_btn = QAction(QIcon(os.path.join("images", "arrow-180.png")), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction(
            QIcon(os.path.join("images", "arrow-000.png")),
            "Forward",
            self,
        )
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction(
            QIcon(os.path.join("images", "arrow-circle-315.png")),
            "Reload",
            self,
        )
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join("images", "home.png")), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()  # Yes, really!
        self.httpsicon.setPixmap(QPixmap(os.path.join("images", "lock-nossl.png")))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(
            QIcon(os.path.join("images", "cross-circle.png")),
            "Stop",
            self,
        )
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(
            QIcon(os.path.join("images", "disk--arrow.png")),
            "Open file...",
            self,
        )
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(
            QIcon(os.path.join("images", "disk--pencil.png")),
            "Save Page As...",
            self,
        )
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(
            QIcon(os.path.join("images", "printer.png")),
            "Print...",
            self,
        )
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        about_action = QAction(
            QIcon(os.path.join("images", "question.png")),
            "About MooseAche",
            self,
        )
        about_action.setStatusTip("Find out more about MooseAche")  # Hungry!
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_mozarella_action = QAction(
            QIcon(os.path.join("images", "lifebuoy.png")),
            "MooseAche Homepage",
            self,
        )
        navigate_mozarella_action.setStatusTip("Go to MooseAche Homepage")
        navigate_mozarella_action.triggered.connect(self.navigate_mozarella)
        help_menu.addAction(navigate_mozarella_action)

        self.show()

        self.setWindowIcon(QIcon(os.path.join("images", "ma-icon-64.png")))

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - MooseAche" % title)

    def navigate_mozarella(self):
        self.browser.setUrl(QUrl("https://www.pythonguis.com/"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "Hypertext Markup Language (*.htm *.html);;" "All files (*.*)",
        )

        if filename:
            with open(filename, "r") as f:
                html = f.read()

            self.browser.setHtml(html)
            self.urlbar.setText(filename)

    def save_html(self, html):
        with open(self.save_file, "w") as f:
            f.write(html)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Page As",
            "",
            "Hypertext Markup Language (*.htm *html);;" "All files (*.*)",
        )

        if filename:
            self.save_file = filename
            self.browser.page().toHtml(self.save_html)

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):
        if q.scheme() == "https":
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join("images", "lock-ssl.png")))

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join("images", "lock-nossl.png")))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("MooseAche")
    app.setOrganizationName("MooseAche")
    app.setOrganizationDomain("MooseAche.org")

    window = MainWindow()

    app.exec()
