from PySide2.QtWidgets import *
from graphicView import ChaosGraphicView
from node import ChaosNode
from lib import *
import json


class NodeChaosEditor(QMainWindow):
    def __init__(self):
        super(NodeChaosEditor, self).__init__()
        self.ui()

    def ui(self):
        self.setFixedSize(900, 700)
        menu = QMenu('File', self)
        save_action = QAction('Save', self)
        menu.addAction(save_action)
        save_action.triggered.connect(self.save)

        load_action = QAction('Load', self)
        menu.addAction(load_action)
        load_action.triggered.connect(self.load)

        self.menuBar().addMenu(menu)
        self.layout = QVBoxLayout(self)
        self.layout.setMargin(0)
        self.graph_view = ChaosGraphicView(parent=self)
        self.graph_view.setAcceptDrops(True)
        self.graph_view.setStyleSheet('border:2px')
        self.graph_view.show()
        self.layout.addWidget(self.graph_view)
        self.setCentralWidget(self.graph_view)
        #
        self.show()
        self.setup_scene()

    def save(self):
        from lib import to_json
        file_name, result = QFileDialog.getSaveFileName()
        if result:
            file = open(file_name, 'w')
            file.write(json.dumps(self.graph_view.node_data, default=to_json, indent=2))
            file.close()

    def load(self):
        self.graph_view.node_data.nodes.clear()
        for item in self.graph_view.scene.items():
            self.graph_view.scene.removeItem(item)
            del item
        file_name, result = QFileDialog.getOpenFileName()
        if result:
            file = open(file_name, 'r')
            data = json.load(file)
            for d in data:
                node = ChaosNode.FromJson(d)
                self.graph_view.node_data.nodes.append(node)
                self.graph_view.add_node(node)
            self.graph_view.update()
            self.graph_view.scene.update()

    def setup_scene(self):
        pass


app = QApplication()
editor = NodeChaosEditor()
app.exec_()
