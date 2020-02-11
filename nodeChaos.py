from chaosGraphicView import ChaosGraphicView
from nodeData import *


class NodeChaosEditor(QWidget):
    def __init__(self):
        super(NodeChaosEditor, self).__init__()
        self.node_data = NodeData()
        self.ui()

    def ui(self):
        self.setFixedSize(900, 700)
        self.layout = QVBoxLayout(self)
        self.layout.setMargin(0)
        self.graph_view = ChaosGraphicView(parent=self)
        self.graph_view.setAcceptDrops(True)
        self.graph_view.setStyleSheet('border:2px')
        self.graph_view.show()

        self.layout.addWidget(self.graph_view)
        self.show()
        self.setup_scene()

    def setup_scene(self):
        pass
app = QApplication()
editor = NodeChaosEditor()
app.exec_()
