from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from enum import Enum
from lib import *


_KNOB_OFFSET = 25
_KNOB_SIZE = 10
_NODE_BORDER = 10

class Node(QGraphicsObject):
    def __init__(self, position:V2d(), size=V2d(100, 100)):
        super(Node, self).__init__()
        self.setAcceptDrops(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        # self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.name = 'node'
        self.dragging = False
        self.position = position
        self.size = size
        self.drag_offset = V2d()
        self.knobs : [Knob] = []
        self.knobs = [
            Knob(self, KnobType.Input),
            Knob(self, KnobType.Output),
        ]

    def __str__(self):
        return str(self.position)

    def mousePressEvent(self, event:QGraphicsSceneMouseEvent):
        super(Node, self).mousePressEvent(event)
        self.scene().update()


    def mouseReleaseEvent(self, event:QGraphicsSceneMouseEvent):
        super(Node, self).mouseReleaseEvent(event)
        self.scene().update()


    def mouseMoveEvent(self, event:QGraphicsSceneMouseEvent):
        super(Node, self).mouseMoveEvent(event)
        self.scene().update()


    def boundingRect(self):
        return QRectF(self.position.x, self.position.y, self.size.x, self.size.y)

    def paint(self, painter:QPainter, option:QStyleOptionGraphicsItem, widget):
        # super(Node, self).paint(painter, option, x)
        if self.dragging:
            painter.setBrush(Qt.lightGray)
        else:
            painter.setBrush(Qt.darkGray)
        painter.drawRoundRect(self.boundingRect(), _NODE_BORDER)
        painter.drawText(self.position.ix()+5, self.position.iy()+15, self.name)
        painter.drawLine(self.position.ix(), self.position.iy()+20, self.boundingRect().right(), self.position.iy()+15)
        for knob in self.knobs:
            if knob.type == KnobType.Input:
                painter.setBrush(QColor(0, 50, 255, 50))
                painter.drawEllipse(
                    self.position.ix() + _KNOB_SIZE, 
                    self.position.iy()+ knob.index * _KNOB_OFFSET, 
                    _KNOB_SIZE, _KNOB_SIZE)
            else:
                painter.setBrush(QColor(0, 255, 0, 50))
                painter.drawEllipse(
                    self.position.ix() + self.size.ix() - _KNOB_SIZE*2, 
                    self.position.iy() + knob.index * _KNOB_OFFSET, 
                    _KNOB_SIZE, _KNOB_SIZE)

class KnobType(Enum):
    Input=1
    Output=2

class Knob:
    def __init__(self, node:Node, type=KnobType.Input):
        self.type = type
        self.index = len([n for n in node.knobs if n.type == type])+1



class NodeData:
    def __init__(self):
        self.nodes : [Node] = []
        self.nodes.append(Node(V2d(50, 50)))
        self.nodes.append(Node(V2d(50, 150)))
        self.nodes.append(Node(V2d(50, -50)))
        self.nodes.append(Node(V2d(50, 250)))
