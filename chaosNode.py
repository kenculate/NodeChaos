from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from lib import *
from enum import Enum
import random

_KNOB_OFFSET = 40
_KNOB_SIZE = 20
_NODE_BORDER = 10


class KnobType(Enum):
    Input = 1
    Output = 2


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
        self.knobs.append(Knob(self, KnobType.Output))
        self.connections : [Connection] = []
        self.default_gradient = QLinearGradient(QPointF(0, 0), QPointF(0, self.size.y))
        self.default_gradient.setColorAt(0, Qt.gray)
        self.default_gradient.setColorAt(30.0 / self.size.y, Qt.darkGray)
        self.default_gradient.setColorAt(30.1 / self.size.y, Qt.lightGray)
        self.default_gradient.setColorAt(1, Qt.darkGray)

        self.selected_gradient = QLinearGradient(QPointF(0, 0), QPointF(0, self.size.y))
        self.selected_gradient.setColorAt(0, Qt.lightGray)
        self.selected_gradient.setColorAt(30.0 / self.size.y, Qt.gray)
        self.selected_gradient.setColorAt(30.1 / self.size.y, Qt.white)
        self.selected_gradient.setColorAt(1, Qt.gray)

    def add_connection(self, scene, source_knob, destination_knob):
        self.connections.append(Connection(source_knob, destination_knob))
        scene.addItem(self.connections[-1].path_item)

    def boundingRect(self):
        return QRect(0, 0, self.size.x, self.size.y)

    def scaleRect(self, rect, x, y):
        return QRect(rect.x()+x, rect.y()+y, rect.width()-(x*2), rect.height()-(y*2))

    def paint(self, painter:QPainter, option, widget):
        if self.isSelected():
            painter.setBrush(QBrush(self.selected_gradient))
        else:
            painter.setBrush(QBrush(self.default_gradient))

        painter.drawRoundedRect(self.scaleRect(self.boundingRect(), _KNOB_SIZE/2, 0), 10, 10)
        painter.drawLine(_KNOB_SIZE/2, 30, self.size.x-_KNOB_SIZE/2, 30)
        painter.setPen(Qt.white)
        painter.drawText(20, 20, f'{self.name} : {len(self.connections)}')
        for connection in self.connections:
            connection.update_path(self.scene())


class Knob(QGraphicsRectItem):
    def __init__(self, node: ChaosNode, knob_type=KnobType.Input):
        super(Knob, self).__init__()
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.node = node
        self.knobType = knob_type
        self.index = len([n for n in node.knobs if n.knobType == knob_type]) + 1
        if knob_type == KnobType.Input:
            self.setBrush(QColor(50, 200, 200))
            self.setRect(node.boundingRect().width() - _KNOB_SIZE,
                         self.index * _KNOB_OFFSET,
                         _KNOB_SIZE, _KNOB_SIZE)
        else:
            self.setBrush(QColor(50, 100, 100))
            self.setRect(0,
                         self.index * _KNOB_OFFSET,
                         _KNOB_SIZE, _KNOB_SIZE)

    def itemChange(self, change, value):
        return super(Knob, self).itemChange(change, value)


class Connection:
    def __init__(self, source: Knob, destination: Knob):
        self.source = source
        self.destination = destination
        self.path_item = QGraphicsPathItem()
        self.path_item.setPen(QPen(Qt.blue, 5))
        self.path = QPainterPath()
        self.path.moveTo(source.rect().center())
        self.path.cubicTo(
            source.rect().center().x() + 50,
            source.rect().center().y(),
            destination.rect().center().x() - 50,
            destination.rect().center().y(),
            destination.rect().center().x(),
            destination.rect().center().y()
        )
        self.path_item.setPath(self.path)

    def update_path(self, scene):
        self.path.setElementPositionAt(0, self.source.mapToScene(self.source.rect().center()).x(),
                                         self.source.mapToScene(self.source.rect().center()).y())
        self.path.setElementPositionAt(1, self.source.mapToScene(self.source.rect().center()).x() + 50,
            self.source.mapToScene(self.source.rect().center()).y())
        self.path.setElementPositionAt(2, self.destination.mapToScene(self.destination.rect().center()).x() - 50,
            self.destination.mapToScene(self.destination.rect().center()).y())
        self.path.setElementPositionAt(3, self.destination.mapToScene(self.destination.rect().center()).x(),
            self.destination.mapToScene(self.destination.rect().center()).y())
        self.path_item.setPath(self.path)
