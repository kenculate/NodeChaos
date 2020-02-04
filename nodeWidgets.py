from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from lib import *
from nodeData import *

_KNOB_OFFSET = 20
_KNOB_SIZE = 10
_NODE_BORDER = 10

class ChaosScene(QGraphicsScene):
    def __init__(self, node_data:NodeData):
        super(ChaosScene, self).__init__()
        self.background_color = Qt.gray
        self.grid_size = V2d(50, 50)
        self.painter : QPainter = None
        self.node_data = node_data
        self.addItem(node_data.nodes[0])
        self.addItem(node_data.nodes[1])
        self.addItem(node_data.nodes[2])
        self.addItem(node_data.nodes[3])
        self.selecting = False
        self.mpress_pos = V2d()
        self.mmove_pos = V2d()
        self.selection_rect = QRect()
        # self.text = self.addText('NODE CHAOS')

    def drawBackground(self, painter:QPainter, rect:QRectF):
        self.painter = painter
        super(ChaosScene, self).drawBackground(painter, rect)
        # self.text.setPos(rect.left(), rect.top())

        painter.setBrush(QColor(150, 150, 150))
        painter.drawRect(rect)
        painter.setPen(QColor(100, 100, 100, 100))
        for x in range(0, int(rect.width()), self.grid_size.ix()):
            painter.drawLine(rect.x() + x, rect.y(), rect.x() + x, int(rect.bottom()))
        for y in range(0, int(rect.width()), self.grid_size.ix()):
            painter.drawLine(rect.x(), rect.y() + y, rect.right(), rect.y() + y)
        if self.selecting:
            # print(self.selecting, self.mpress_pos, self.mmove_pos)
            painter.setPen(Qt.white)
            painter.setBrush(QColor(255, 255, 255, 30))
            # painter.drawRect(self.mpress_pos.x, self.mpress_pos.y, self.mmove_pos.x-self.mpress_pos.x, self.mmove_pos.y-self.mpress_pos.y)
            painter.drawRect(self.selection_rect)


    def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
        super(ChaosScene, self).mousePressEvent(event)
        if self.selectedItems():
            return
        self.selecting = True
        self.mpress_pos.setxy(event.scenePos().x(), event.scenePos().y())

    def mouseReleaseEvent(self, event:QGraphicsSceneMouseEvent):
        super(ChaosScene, self).mouseReleaseEvent(event)
        self.selecting = False
        self.update()
        self.selection_rect.setCoords(self.mpress_pos.x, self.mpress_pos.y, self.mmove_pos.x, self.mmove_pos.y)


    def mouseMoveEvent(self, event:QGraphicsSceneMouseEvent):
        super(ChaosScene, self).mouseMoveEvent(event)
        self.update()
        self.mmove_pos.setxy(event.scenePos().x(), event.scenePos().y())
        self.selection_rect.setCoords(self.mpress_pos.x, self.mpress_pos.y, self.mmove_pos.x, self.mmove_pos.y)


    def select_rect(self):
        for node in self.node_data.nodes:
            if self.selection_rect.contains(node.position.x, node.position.y):
                node.setSelected(True)
            else:
                node.setSelected(False)

            