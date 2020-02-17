from PySide2.QtWidgets import *
from graphicView import ChaosGraphicView
from node import Node
import json
from itemEditor import ItemEditor
from nodeChaosEditor_UI import Ui_MainWindow


class NodeChaosEditor(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(NodeChaosEditor, self).__init__()
        self.setupUi(self)
        self.graph_view = ChaosGraphicView(parent=None)
        self.item_editor = ItemEditor(parent=self.graph_view)
        self.horizontalLayout.insertWidget(0, self.graph_view)
        self.horizontalLayout.addWidget(self.item_editor)
        self.item_editor.setMaximumWidth(400)
        self.action_save.triggered.connect(self.save)
        self.action_load.triggered.connect(self.load)
        self.showMaximized()

    def save(self):
        from lib import to_json
        file_name, result = QFileDialog.getSaveFileName()
        if result:
            file = open(file_name, 'w')
            file.write(json.dumps(self.graph_view.node_data, default=to_json, indent=2))
            file.close()

    def load(self):
        from nodeData import Item
        self.graph_view.node_data.nodes.clear()
        for item in self.graph_view.scene.items():
            self.graph_view.scene.removeItem(item)
            del item
        file_name, result = QFileDialog.getOpenFileName()
        if result:
            file = open(file_name, 'r')
            data = json.load(file)
            # nodes
            nodes = data.get('nodes', [])
            for n in nodes:
                node = Node.FromJson(n)
                self.graph_view.node_data.nodes.append(node)
                self.graph_view.add_node(node)
            for node in nodes:
                for connection in node.get('connections', []):
                    _node = [n for n in self.graph_view.node_data.nodes if n.id == node['id']]
                    if _node:
                        _node = _node[0]
                        _source_knob = [kn for kn in _node.knobs if kn.id == connection['source']['id']]
                        _destination_node = [n for n in self.graph_view.node_data.nodes if n.id == connection['destination']['node']]
                        _destination_knob = [kn for kn in _destination_node[0].knobs if kn.id == connection['destination']['id']]
                        _node.add_connection(self.graph_view.scene, _source_knob[0], _destination_knob[0])
            # items
            items = data.get('items', [])
            for item in items:
                self.graph_view.node_data.items.append(Item.FromJson(item))

    def setup_scene(self):
        pass


app = QApplication()
editor = NodeChaosEditor()
app.exec_()
