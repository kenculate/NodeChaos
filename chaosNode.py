from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from lib import *
from enum import Enum
import random

_KNOB_OFFSET = 40
_KNOB_SIZE = 20
_NODE_BORDER = 10


class ChaosNode(QGraphicsItem):

    def __init__(self, position=V2d(0, 0), size=V2d(200, 200), name='Node'):
        super(ChaosNode, self).__init__()
        self.setPos(position.pointf())
        self.name = name
        self.position = position
        self.size = size
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setCursor(Qt.SizeAllCursor)
        self.knobs: [Knob] = []
        self.knobs.append(Knob(self, KnobType.Input))
        self.knobs.append(Knob(self, KnobType.Input))
        self.knobs.append(Knob(self, KnobType.Output))

    def boundingRect(self):
        return QRect(0, 0, self.size.x, self.size.y)

    def paint(self, painter:QPainter, option, widget):
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, self.size.y))
        gradient.setColorAt(0, Qt.gray)
        gradient.setColorAt(30.0 / self.size.y, Qt.darkGray)
        gradient.setColorAt(30.1 / self.size.y, Qt.lightGray)
        gradient.setColorAt(1, Qt.darkGray)
        if self.isSelected():
            painter.setBrush(QBrush(gradient))
        else:
            painter.setBrush(QBrush(gradient))
            # painter.setBrush(Qt.darkGray)

        painter.drawRoundedRect(self.boundingRect(), 10, 10)
        painter.drawLine(0, 30, self.size.x, 30)
        painter.setPen(Qt.white)
        painter.drawText(20, 20, self.name)
        painter.setPen(Qt.black)

        for knob in self.knobs:
            if knob.type == KnobType.Input:
                painter.setBrush(QColor(0, 50, 255, 50))
                painter.drawRect(
                    5,
                    knob.index * _KNOB_OFFSET,
                    _KNOB_SIZE, _KNOB_SIZE
                )
                # painter.drawEllipse(
                #     5,
                #     knob.index * _KNOB_OFFSET,
                #     _KNOB_SIZE, _KNOB_SIZE)
            else:
                painter.setBrush(QColor(0, 255, 0, 50))
                painter.drawEllipse(
                    self.boundingRect().width() - _KNOB_SIZE -5,
                    knob.index * _KNOB_OFFSET,
                    _KNOB_SIZE, _KNOB_SIZE)


class KnobType(Enum):
    Input = 1
    Output = 2


class Knob:
    def __init__(self, node: ChaosNode, type=KnobType.Input):
        self.type = type
        self.index = len([n for n in node.knobs if n.type == type]) + 1
