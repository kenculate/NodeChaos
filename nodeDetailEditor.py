from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class NodeDetailEditor(QDialog):
    def __init__(self, node, parent):
        self.graph_view = parent
        super(NodeDetailEditor, self).__init__(parent=parent)
        self.resize(QSize(800, 400))
        self.setStyleSheet('''
        QWidget{
        background-color:
        qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(173, 173, 173), stop:1 rgb(131, 131, 131));
        color:rgb(255, 255, 255);
        QLabel{
            background-color:transparent
        }
        }
        QLabel{
            background-color:transparent
        }
        QListView{
        background-color:lightGray
        }
        ''')
        self.h_layout = QHBoxLayout(self)
        self.layout = QVBoxLayout(self)
        self.v_layout1 = QVBoxLayout(self)
        self.v_layout2 = QVBoxLayout(self)
        self.h_layout.addLayout(self.layout)
        self.h_layout.addLayout(self.v_layout1)
        self.h_layout.addLayout(self.v_layout2)
        self.list_required_item = QListView()
        self.list_item = QListView()
        self.lbl_item = QLabel('acquire items')
        self.list_item.setMaximumWidth(200)
        self.lbl_item.setMaximumWidth(200)
        self.lbl_required_item = QLabel('required items')
        self.list_required_item.setMaximumWidth(200)
        self.lbl_required_item.setMaximumWidth(200)
        self.v_layout1.addWidget(self.lbl_item)
        self.v_layout1.addWidget(self.list_item)
        self.v_layout2.addWidget(self.lbl_required_item)
        self.v_layout2.addWidget(self.list_required_item)

        self.lbl_title = QLabel('title:')
        self.txt_title = QLineEdit()
        self.lbl_text = QLabel('text:')
        self.txt_text = QPlainTextEdit()
        self.pb_save = QPushButton('save')
        self.pb_close = QPushButton('close')
        self.layout.addWidget(self.lbl_title)
        self.layout.addWidget(self.txt_title)
        self.layout.addWidget(self.lbl_text)
        self.layout.addWidget(self.txt_text)
        self.layout.addWidget(self.pb_save)
        self.layout.addWidget(self.pb_close)
        self.node = node
        self.pb_close.clicked.connect(self.close)
        self.pb_save.clicked.connect(self.save)
        self.item_model = QStandardItemModel()
        self.required_item_model = QStandardItemModel()
        self.list_required_item.setModel(self.required_item_model)
        self.list_item.setModel(self.item_model)

    def open(self, node):
        self.item_model.clear()
        self.required_item_model.clear()
        # adding acquire items
        for item in self.parent().node_data.items:
            row = QStandardItem(item.name)
            row.setData(item, Qt.UserRole)
            row.setCheckable(True)
            if item.id in [i.id for i in node.detail.items]:
                row.setCheckState(Qt.Checked)
            self.item_model.appendRow(row)
        # adding require items
        for item in self.parent().node_data.items:
            row = QStandardItem(item.name)
            row.setData(item, Qt.UserRole)
            row.setCheckable(True)
            if item.id in [i.id for i in node.detail.required_items]:
                row.setCheckState(Qt.Checked)
            self.required_item_model.appendRow(row)

        self.txt_text.setPlainText(node.detail.text)
        self.txt_title.setText(node.detail.title)
        self.node = node
        self.exec_()

    def save(self):
        self.node.detail.title = self.txt_title.text()
        self.node.detail.text = self.txt_text.toPlainText()
        for row in range(self.item_model.rowCount()):
            index = self.item_model.index(row, 0)
            row_item = self.item_model.itemFromIndex(index)
            if row_item.checkState() == Qt.Checked:
                if row_item.data(Qt.UserRole) not in self.node.detail.items:
                    self.node.detail.add_item(row_item.data(Qt.UserRole))
            else:
                if row_item.data(Qt.UserRole) in self.node.detail.items:
                    self.node.detail.remove_item(row_item.data(Qt.UserRole))
        for row in range(self.required_item_model.rowCount()):
            index = self.required_item_model.index(row, 0)
            row_item = self.required_item_model.itemFromIndex(index)
            if row_item.checkState() == Qt.Checked:
                if row_item.data(Qt.UserRole) not in self.node.detail.required_items:
                    self.node.detail.add_required_item(row_item.data(Qt.UserRole))
            else:
                if row_item.data(Qt.UserRole) in self.node.detail.required_items:
                    self.node.detail.remove_required_item(row_item.data(Qt.UserRole))


        self.close()

