from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from enum import Enum
from lib import *


_KNOB_OFFSET = 25
_KNOB_SIZE = 10
_NODE_BORDER = 10


class Node(QGraphicsRectItem):
    def __init__(self, position:V2d(), size=V2d(100, 100)):
        super(Node, self).__init__()
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.setRect(position.x, position.y, size.x, size.y)
        self.selection_rect = QRectF()
        self.name = 'node'
        self.knobs : [Knob] = []
        self.knobs = [
            Knob(self, KnobType.Input),
            Knob(self, KnobType.Output),
        ]

    def __str__(self):
        return str(self.position)

    def paint(self, painter:QPainter, option:QStyleOptionGraphicsItem, widget):
        if self.isSelected():
            painter.setBrush(Qt.lightGray)
        else:
            painter.setBrush(Qt.darkGray)
        painter.drawRect(self.rect())
        painter.drawText(self.rect().x()+5, self.rect().y()+15, self.name)
        painter.drawLine(self.rect().x(), self.rect().y()+20, self.rect().right(), self.rect().y()+15)
        for knob in self.knobs:
            if knob.type == KnobType.Input:
                painter.setBrush(QColor(0, 50, 255, 50))
                painter.drawEllipse(
                    self.rect().x() + _KNOB_SIZE,
                    self.rect().y() + knob.index * _KNOB_OFFSET,
                    _KNOB_SIZE, _KNOB_SIZE)
            else:
                painter.setBrush(QColor(0, 255, 0, 50))
                painter.drawEllipse(
                    self.rect().x() + self.rect().width() - _KNOB_SIZE*2,
                    self.rect().y() + knob.index * _KNOB_OFFSET,
                    _KNOB_SIZE, _KNOB_SIZE)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            self.selection_rect.setRect(value.x()+self.rect().x(), value.y()+self.rect().y(), 50, 50)
            return value
        return super(Node, self).itemChange(change, value)


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
        self.nodes.append(Node(V2d(150, 150)))
