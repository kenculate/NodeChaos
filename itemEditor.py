from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from nodeData import Item


class ItemEditor(QWidget):
    def __init__(self, parent):
        super(ItemEditor, self).__init__(parent=parent)
        self.resize(QSize(400, 400))

        self.setStyleSheet('''
                background-color:
                qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(173, 173, 173), stop:1 rgb(131, 131, 131));
                color:rgb(255, 255, 255);
                ''')
        self.graph_view = parent
        self.layout = QVBoxLayout(self)
        self.list_view = QListView(self)
        self.pb_add = QPushButton('add')
        self.pb_add.clicked.connect(self.add_item)
        self.layout.addWidget(self.pb_add)
        self.layout.addWidget(self.list_view)
        self.pb_close = QPushButton('close')
        self.layout.addWidget(self.pb_close)
        self.model = QStandardItemModel()
        self.pb_close.clicked.connect(self.close)
        self.list_view.setModel(self.model)

    def add_item(self):
        text, result = QInputDialog.getText(self, 'adding item', 'enter item name to add')
        if result:
            row = QStandardItem(text)
            row.setCheckable(True)
            self.model.insertRow(self.model.rowCount(), row)
            item = Item()
            item.name = text
            self.graph_view.node_data.items.append(item)
