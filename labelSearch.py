from PyQt5.QtWidgets import (QApplication, QLineEdit,  QWidget, QPushButton,
                             QLineEdit, QCompleter, QVBoxLayout, QHBoxLayout,
                             QFrame)
from PyQt5.QtCore import pyqtSlot


import sys

__appname__ = 'labelSearch'
__datadir__ = None

class SearchWindow(QWidget):
    class SearchArea(QFrame):
        class TagButton(QPushButton):
            def __init__(self, tag, controller):
                QPushButton.__init__(self)
                self.tag = tag
                self.setText(tag)
                self.clicked.connect(lambda: controller.delete_tag(tag))

        def __init__(self, controller):
            QFrame.__init__(self)
            self.controller = controller
            self.search_bar = QLineEdit()
            font = self.search_bar.font()
            font.setPointSize(16)
            self.search_bar.setFont(font)

            self.search_tag_container = QFrame()
            self.search_tag_container.setFrameShape(QFrame.StyledPanel)
            self.search_tag_container.setLayout(QHBoxLayout())

            self.hbox_search = QHBoxLayout()
            self.hbox_search.addWidget(self.search_bar, stretch=1)
            self.hbox_search.addWidget(self.search_tag_container, stretch=2)

            self.setLayout(self.hbox_search)
            self.tag_btns = []

        def add_tag_btn(self, tag):
            for b in self.tag_btns:
                if b.tag == tag:
                    return
            button = self.TagButton(tag, controller)
            self.search_tag_container.layout().addWidget(button)
            self.tag_btns.append(button)

        def remove_tag_btn(self, tag):
            to_remove = None
            for btn in self.tag_btns:
                if btn.tag == tag:
                    self.search_tag_container.layout().removeWidget(btn)
                    to_remove = btn
            if to_remove is not None:
                self.tag_btns.remove(to_remove)
                to_remove.deleteLater()


    def __init__(self, controller):
        QWidget.__init__(self)
        self.controller = controller

        window_geom = (300, 100, 600, 800)
        self.model = Model()
        self.init_layout(window_geom)


    def init_layout(self, window_geom):
        self.setWindowTitle(__appname__)
        self.setGeometry(*window_geom)

        self.search_area = self.SearchArea(self.controller)
        sb = self.search_area.search_bar
        sb.returnPressed.connect(
            lambda: self.controller.push_search_entry(self.get_search_entry()))
        vbox_root = QVBoxLayout()
        vbox_root.addWidget(self.search_area)

        self.setLayout(vbox_root)

    def get_search_entry(self):
        tag = self.search_area.search_bar.text()
        tag = tag.strip()
        self.search_area.search_bar.setText("")
        if len(tag) > 0:
            return tag
        else:
            return None
    
    def update_suggestions(self, suggestions):
        tag_completer = QCompleter(suggestions)
        self.search_area.search_bar.setCompleter(tag_completer)

    def add_tag(self, tag):
        self.search_area.add_tag_btn(tag)

    def remove_tag(self, tag):
        self.search_area.remove_tag_btn(tag)


class Model():
    def __init__(self):
        self.search_terms = []
        "Load all annotations into memory from datadir"
        "Recalculate search term statistics"
        pass

    def get_search_terms(self):
        return self.search_terms
    
    def add_tag_to_search(self, tag):
        self.search_terms.append(tag)
    
class AppController():
    def __init__(self):
        self.window = SearchWindow(self)
        self.window.show()
        self.model = Model()

    def push_search_entry(self, tag):
        if tag is None: return 
        self.model.add_tag_to_search(tag)
        self.window.add_tag(tag)
        self.window.update_suggestions(self.get_suggestions())

    def get_suggestions(self):
        search_terms = self.model.get_search_terms()
        if len(search_terms) < 1:
            return []
        else:
            return ["aaa"] # todo
        pass

    def delete_tag(self, tag):
        self.window.remove_tag(tag)

app = QApplication(sys.argv)
app.setStyle('Fusion')
controller = AppController()
sys.exit(app.exec_())