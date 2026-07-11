import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView

HOME_PAGE = "https://www.google.com"

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Browser")
        self.setMinimumSize(900, 600)
        self.updating_urlbar = False

        # Web view
        self.view = QWebEngineView()
        self.view.setUrl(QUrl(HOME_PAGE))
        self.setCentralWidget(self.view)

        # Navigation toolbar
        self.create_toolbar()

        # update URL bar when page changes
        self.view.urlChanged.connect(self.update_urlbar)

    def create_toolbar(self):
        """Create and configure the navigation toolbar"""
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        # Back button
        back_btn = QAction("◀", self)
        back_btn.setStatusTip("Back")
        back_btn.triggered.connect(self.view.back)
        navtb.addAction(back_btn)

        # Forward button
        forward_btn = QAction("▶", self)
        forward_btn.setStatusTip("Forward")
        forward_btn.triggered.connect(self.view.forward)
        navtb.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("⟲", self)
        reload_btn.setStatusTip("Reload")
        reload_btn.triggered.connect(self.view.reload)
        navtb.addAction(reload_btn)

        # Home button
        home_btn = QAction("🏠", self)
        home_btn.setStatusTip("Home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        # URL bar
        self.urlbar = QLineEdit()
        self.urlbar.setPlaceholderText("Enter URL or search (e.g. example.com or hello world) — Press Enter")
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        # Go button
        go_btn = QAction("Go", self)
        go_btn.triggered.connect(self.navigate_to_url)
        navtb.addAction(go_btn)

        # Keyboard shortcut: Ctrl+L to focus urlbar
        shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        shortcut.activated.connect(self.focus_urlbar)

    def navigate_home(self):
        """Navigate to home page"""
        self.view.setUrl(QUrl(HOME_PAGE))

    def navigate_to_url(self):
        """Navigate to URL or search based on user input"""
        text = self.urlbar.text().strip()
        if text == "":
            return
        
        url = self.process_input(text)
        self.view.setUrl(QUrl(url))

    def process_input(self, text):
        """Process user input and return appropriate URL"""
        if " " in text:
            # Treat as search
            return "https://www.google.com/search?q=" + text.replace(" ", "+")
        
        if text.startswith("http://") or text.startswith("https://"):
            return text
        
        if "." in text:
            return "http://" + text
        
        return "https://www.google.com/search?q=" + text

    def update_urlbar(self, q: QUrl):
        """Update URL bar when page changes"""
        self.updating_urlbar = True
        self.urlbar.setText(q.toString())
        self.updating_urlbar = False

    def focus_urlbar(self):
        """Focus and select all text in URL bar"""
        self.urlbar.setFocus()
        self.urlbar.selectAll()

def main():
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()