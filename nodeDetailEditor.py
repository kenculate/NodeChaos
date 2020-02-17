from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class NodeDetailEditor(QDialog):
    def __init__(self, node, parent):
        super(NodeDetailEditor, self).__init__(parent=parent)
        self.resize(QSize(400, 400))
        self.setStyleSheet('''
        background-color:
        qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(173, 173, 173), stop:1 rgb(131, 131, 131));
        color:rgb(255, 255, 255);
        ''')
        self.layout = QVBoxLayout(self)
        self.lbl_title = QLabel('title:')
        self.lbl_title.setStyleSheet('background-color: transparent')
        self.txt_title = QLineEdit()
        self.lbl_text = QLabel('text:')
        self.lbl_text.setStyleSheet('background-color: transparent')
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

    def open(self, node):
        self.txt_text.setPlainText(node.detail.text)
        self.txt_title.setText(node.detail.title)
        self.node = node
        self.exec_()

    def save(self):
        self.node.detail.title = self.txt_title.text()
        self.node.detail.text = self.txt_text.toPlainText()
        self.close()

