from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLineEdit, QStackedWidget
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #variables
        self.search = ""
        self.tab_count = 1
        self.web_views = []
        self.stack = QStackedWidget()
        self.tab_layout_widget = QWidget()
        self.tabs = []
        self.tab_widgets = []
        self.tab_widgets.append(self.tab_layout_widget)

        # Window settings
        self.setWindowTitle("WEB")
        self.setFixedSize(800, 600)

        # Widgets

        self.back = QPushButton("back")
        self.forward = QPushButton("forward")
        self.reload = QPushButton("reload")
        self.tab = QPushButton("google.com")
        self.close_tab = QPushButton("×")
        self.tabs.append(self.tab)
        self.tab.setFixedHeight(20)
        self.add_tab = QPushButton("+")
        self.add_tab.setFixedHeight(20)
        self.add_tab.setFixedWidth(40)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("ADDRESS BAR")

        self.search_button = QPushButton("search")

        self.web_view = QWebEngineView()
        self.web_views.append(self.web_view)

        #widget setup setup
        self.back.clicked.connect(lambda: self.back_click())
        self.forward.clicked.connect(lambda: self.forward_click())
        self.reload.clicked.connect(lambda: self.reload_click())
        self.search_button.clicked.connect(lambda: self.search_clicked())
        self.search_bar.returnPressed.connect(lambda: self.search_clicked())
        self.web_view.urlChanged.connect(lambda: self.url_changed(self.web_view))
        self.add_tab.clicked.connect(self.added_tab)
        self.tab.clicked.connect(lambda: self.tab_select(self.web_view))
        self.close_tab.clicked.connect(lambda: self.tab_closed(self.web_view))

        # Central widget
        self.central_widget = QWidget()

        # Layout
        self.layout = QVBoxLayout()
        layout2 = QHBoxLayout()
        self.layout3 = QHBoxLayout()
        self.tab_layout = QHBoxLayout()
        self.layout.addLayout(self.layout3)
        self.layout.addLayout(layout2)
        self.stack.addWidget(self.web_view)      
        self.tab_layout_widget.setLayout(self.tab_layout)

        #widgets being shown
        self.layout.addWidget(self.stack)

        layout2.addWidget(self.back)
        layout2.addWidget(self.forward)
        layout2.addWidget(self.reload)
        layout2.addWidget(self.search_bar)
        layout2.addWidget(self.search_button)

        self.layout3.addWidget(self.tab_layout_widget)

        self.tab_layout.addWidget(self.tab)
        self.tab_layout.addWidget(self.close_tab)
        self.layout3.addWidget(self.add_tab)

        #layout settings
        self.layout.setContentsMargins(10,10,10,10)
        layout2.setContentsMargins(0,0,0,0)
        self.layout3.setContentsMargins(0,0,0,0)

        # Connect layout to central widget
        self.central_widget.setLayout(self.layout)
        # Put central widget into main window
        self.setCentralWidget(self.central_widget)

    def back_click(self):
        self.web_views[self.stack.currentIndex()].back()

    def forward_click(self):
        self.web_views[self.stack.currentIndex()].forward()
    
    def reload_click(self):
        self.web_views[self.stack.currentIndex()].reload()
    
    def search_clicked(self):
        self.search = self.search_bar.text()
        self.current_view = self.stack.currentIndex()
        if ".com" in self.search or ".org" in self.search:
            if "https://" in self.search or "http://" in self.search:
                self.url = QUrl(self.search)
            else:
                self.url = QUrl("https://" + self.search)
        else:
            self.url = QUrl("https://www.google.com/search?q=" + self.search)

        self.web_views[self.current_view].load(self.url)
    
    def url_changed(self,  view):
        index = self.web_views.index(view)
        self.display_url = view.url().toString()
        self.tabs[index].setText(self.display_url)

    def added_tab(self):
        self.new_tab_layout = QHBoxLayout()
        self.new_tab_layout_widget = QWidget()
        self.tab_widgets.append(self.new_tab_layout_widget)

        self.new_tab_layout_widget.setLayout(self.new_tab_layout)

        self.new_tab = QPushButton("new tab")
        self.new_close = QPushButton("x")

        self.new_tab_layout.addWidget(self.new_tab)
        self.new_tab_layout.addWidget(self.new_close)

        self.layout3.insertWidget(self.layout3.count() - 1, self.new_tab_layout_widget)

        self.new_view = QWebEngineView()
        self.web_views.append(self.new_view)
        self.tabs.append(self.new_tab)
        self.stack.addWidget(self.new_view)
        self.stack.setCurrentWidget(self.new_view)
        view = self.new_view
        self.new_tab.clicked.connect(lambda: self.tab_select(view))
        self.new_view.urlChanged.connect(lambda: self.url_changed(view))
        self.new_close.clicked.connect(lambda: self.tab_closed(view))

    def tab_select(self, view):
        self.stack.setCurrentWidget(view)

    def tab_closed(self, view):
        if len(self.web_views) == 1:
            return

        index = self.web_views.index(view)

        self.stack.removeWidget(view)

        widget = self.tab_widgets[index]
        self.layout3.removeWidget(widget)

        self.web_views.pop(index)
        self.tabs.pop(index)
        self.tab_widgets.pop(index)

        widget.deleteLater()
        view.deleteLater()

        new_index = min(index, self.stack.count() - 1)
        self.stack.setCurrentIndex(new_index)

app = QApplication()
window = MyWindow()

window.show()
app.exec()
