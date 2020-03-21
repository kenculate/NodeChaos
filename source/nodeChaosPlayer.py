from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from source.data import Data


class NodeChaosPlayer(QWidget):
    def __init__(self, parent, item_editor):
        super(NodeChaosPlayer, self).__init__(parent=parent)
        self.setStyleSheet('''
                QWidget{background-color:
                qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(173, 173, 173), stop:1 rgb(131, 131, 131));
                color:rgb(255, 255, 255);
                }
                ''')
        self.item_editor = item_editor
        self.current_node = None
        self.graph_view = parent
        self.layout = QVBoxLayout(self)
        self.txt_text = QPlainTextEdit(self)
        self.list_view = QListView(self)
        self.layout.addWidget(self.txt_text)
        self.layout.addWidget(self.list_view)
        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)
        self.list_view.clicked.connect(self.item_clicked)
        self.items = []

    def play(self, node):
        self.items.clear()
        self.item_editor.reset_items()
        self.load_node(node)

    def load_node(self, node):
        self.current_node = node
        self.txt_text.setPlainText(node.detail.text)
        self.model.clear()
        node.setSelected(True)
        for item in node.detail.items:
            self.item_editor.found_item(item)
            self.items.append(item)
        for connection in node.connections:
            next_node = Data.get_node(connection.destination.node.id)
            if next_node:
                if connection.path_item:
                    title = next_node.detail.title
                    row = QStandardItem(title)
                    found_items = self.has_required_item(next_node.detail.required_items, self.items)
                    if not len(found_items):
                        title = f'(LOCKED){next_node.detail.title}'
                        row.setText(title)
                        row.setForeground(QBrush(Qt.red))
                    row.setData(next_node, Qt.UserRole)
                    self.model.appendRow(row)
                    connection.path_item.setSelected(True)
        self.graph_view.frame_selected(self.graph_view.scene.selectedItems())

    def has_required_item(self, require_items, items):
        if not require_items:
            return [True]
        return list(set([i.id for i in require_items]) & set([i.id for i in items]))

    def clear(self):
        self.current_node.setSelected(False)
        for connection in self.current_node.connections:
            if connection.path_item:
                connection.path_item.setSelected(False)

    def item_clicked(self, index):
        item = self.model.itemFromIndex(index)
        if '(LOCKED)' in item.text():
            return
        self.clear()
        node = item.data(Qt.UserRole)
        self.load_node(node)