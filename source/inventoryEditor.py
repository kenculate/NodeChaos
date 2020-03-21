from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from source.data import Item
from source.data import Data


class InventoryEditor(QWidget):
    def __init__(self, parent):
        super(InventoryEditor, self).__init__(parent=parent)
        self.resize(QSize(400, 400))

        self.setStyleSheet('''
                QWidget{background-color:
                qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(173, 173, 173), stop:1 rgb(131, 131, 131));
                color:rgb(255, 255, 255);
                }
                ''')
        self.layout = QVBoxLayout(self)
        self.layout.setMargin(0)
        self.list_view = QListView(self)
        self.pb_add = QPushButton('add')
        self.pb_add.clicked.connect(self.add_item)
        self.layout.addWidget(self.pb_add)
        self.layout.addWidget(self.list_view)
        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)

    def load(self, items):
        for item in items:
            row = QStandardItem(item.name)
            row.setCheckable(True)
            row.setData(item, Qt.UserRole)
            self.model.insertRow(self.model.rowCount(), row)
        self.list_view.repaint()

    def add_item(self):
        text, result = QInputDialog.getText(self, 'adding item', 'enter item name to add')
        if result:
            item = Item()
            item.name = text
            Data.add_item(item)
            row = QStandardItem(text)
            row.setCheckable(True)
            row.setData(item, Qt.UserRole)
            self.model.appendRow(row)

    def found_item(self, item):
        for row in range(self.model.rowCount()):
            row_item = self.model.itemFromIndex(self.model.index(row, 0))
            if row_item:
                if row_item.data(Qt.UserRole).id == item.id:
                    row_item.setCheckState(Qt.Checked)

    def reset_items(self):
        for row in range(self.model.rowCount()):
            row_item = self.model.itemFromIndex(self.model.index(row, 0))
            row_item.setCheckState(Qt.Unchecked)