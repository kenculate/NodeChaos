from PySide2.QtWidgets import *
from graphicView import ChaosGraphicView
from node import Node, Connection, KnobType
import json
from inventoryEditor import InventoryEditor
from nodeChaosEditor_UI import Ui_MainWindow
from nodeChaosPlayer import NodeChaosPlayer


class NodeChaosEditor(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(NodeChaosEditor, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Node Chaos')
        self.graph_view = ChaosGraphicView(parent=self)
        self.item_editor = InventoryEditor(parent=self.graph_view)
        self.player = NodeChaosPlayer(self.graph_view)
        self.player.setFixedWidth(0)
        self.horizontalLayout.insertWidget(0, self.graph_view)
        self.horizontalLayout.addWidget(self.item_editor)
        self.horizontalLayout.addWidget(self.player)
        self.item_editor.setMaximumWidth(400)
        self.action_save.triggered.connect(self.save)
        self.action_load.triggered.connect(self.load)
        self.actionPlay.triggered.connect(self.play)

        self.showMaximized()

    def play(self):
        self.player.setFixedWidth(400)
        self.player.play(self.graph_view.node_data.nodes[0])

    def save(self):
        from lib import to_json
        file_name, result = QFileDialog.getSaveFileName()
        if result:
            file = open(file_name, 'w')
            file.write(json.dumps(self.graph_view.node_data, default=to_json, indent=2))
            file.close()

    def load(self):
        from data import Item
        self.graph_view.node_data.clear_nodes()
        for item in self.graph_view.scene.items():
            if item != self.graph_view.path:
                self.graph_view.scene.removeItem(item)
                del item
        file_name, result = QFileDialog.getOpenFileName()
        if result:
            file = open(file_name, 'r', encoding='utf-8')
            data = json.load(file)
            # items
            items = data.get('items', [])
            for item in items:
                self.graph_view.node_data.add_item(Item.FromJson(item))
            self.item_editor.load(self.graph_view.node_data.items)
            # nodes
            nodes = data.get('nodes', [])
            for n in nodes:
                node = Node.FromJson(n)
                self.graph_view.node_data.add_node(node)
                self.graph_view.add_node(node)
            for node in nodes:
                source_node = [
                    n for n in self.graph_view.node_data.nodes
                    if n.id == node.get('id', 0)
                ]
                source_node[0].setup_connection(node, self.graph_view.node_data.nodes, self.graph_view.scene)


    def setup_scene(self):
        pass


app = QApplication()
editor = NodeChaosEditor()
app.exec_()
