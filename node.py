from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from lib import *
from enum import Enum
import random
import uuid
from data import NodeDetail

_KNOB_OFFSET = 40
_KNOB_SIZE = 20
_NODE_BORDER = 10


class KnobType(Enum):
    Input = 1
    Output = 2

    def json(self):
        return self.value


class Node(QGraphicsItem):

    @staticmethod
    def FromJson(data):
        name = data.get('name', '')
        position = V2d.FromJson(data.get('position', V2d()))
        node = Node(position, name=name)
        node.id = data.get('id', 0)
        detail = NodeDetail.FromJson(node, data.get('detail', {}))
        node.detail = detail
        knobs = data.get('knobs', [])
        for i in range(len(knobs)):
            node.knobs[i].id = knobs[i]['id']
        return node

    def json(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'position': self.position,
            'detail': self.detail,
            'knobs': self.knobs,
            'connections': [c for c in self.connections]
        }

    def __init__(self, position=V2d(0, 0), size=V2d(200, 200), name='Node'):
        super(Node, self).__init__()
        self.id = uuid.uuid1()
        self.setPos(position.pointf())
        self.name = name
        self.position = position
        self.size = size
        self.detail = NodeDetail(self)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setCursor(Qt.SizeAllCursor)
        self.knobs: [Knob] = []
        self.knobs.append(Knob(self, KnobType.Input))
        self.knobs.append(Knob(self, KnobType.Output))
        self.connections: [Connection] = []
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

    def delete(self):
        self.scene().removeItem(self)
        del self

    def setup_connection(self, node, nodes, scene):
        for connection in node.get('connections', []):
            source_knob = [
                kn for kn in self.knobs
                if kn.id == connection.get('source', {}).get('id', 0)
            ]
            if connection.get('source', {}).get('knob_type', 0) == 1:
                destination_node = [
                    n for n in nodes
                    if n.id == connection.get('destination', {}).get('node', None)
                ]
                destination_knob = [
                    kn for kn in destination_node[0].knobs
                    if kn.id == connection.get('destination', {}).get('id', 0)
                ]
                self.add_connection(scene, source_knob[0], destination_knob[0])

    def add_connection(self, scene, source_knob, destination_knob):
        destination_knob.node.connections.append(Connection(destination_knob, source_knob, False))
        self.connections.append(Connection(source_knob, destination_knob, True))
        scene.addItem(self.connections[-1].path_item)

    def remove_connection(self, connection):
        self.connections.remove(connection)

    def rect(self):
        return QRect(self.position.x, self.position.y, self.size.x, self.size.y)

    def boundingRect(self):
        return QRect(0, 0, self.size.x, self.size.y)

    def scale_rect(self, rect, x, y):
        return QRect(rect.x()+x, rect.y()+y, rect.width()-(x*2), rect.height()-(y*2))

    def paint(self, painter:QPainter, option, widget):
        self.position.setxy(self.pos().x(), self.pos().y())
        if self.isSelected():
            pen = painter.pen()
            brush = painter.brush()
            painter.setBrush(Qt.white)
            painter.setPen(QPen(Qt.white, 5))
            painter.drawRoundedRect(self.scale_rect(self.boundingRect(), (_KNOB_SIZE / 2)-2, -2), 10, 10)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.setBrush(QBrush(self.selected_gradient))
        else:
            painter.setBrush(QBrush(self.default_gradient))

        painter.drawRoundedRect(self.scale_rect(self.boundingRect(), _KNOB_SIZE / 2, 0), 10, 10)
        painter.drawLine(_KNOB_SIZE/2, 30, self.size.x-_KNOB_SIZE/2, 30)
        painter.setPen(Qt.white)
        if not self.detail.title:
            painter.drawText(20, 20, f'{self.name} : {len(self.connections)}')
        else:
            painter.drawText(20, 20, self.detail.title)

        if self.detail.text:
            painter.setPen(Qt.black)
            painter.drawText(self.scale_rect(self.boundingRect(), _KNOB_SIZE, 50), self.detail.text)
        for connection in self.connections:
            connection.update_path()


class Knob(QGraphicsRectItem):
    @staticmethod
    def FromJson(node, data):
        knob = Knob(node)
        knob.id = data.get('id', 0)
        knob.index = data.get('index', 0)
        knob.knob_type = data.get('knob_type', KnobType.Input)
        return knob

    def json(self):
        return {
            'id': str(self.id),
            'knob_type': self.knob_type,
            'index': self.index,
            'node': str(self.node.id)
        }

    def __init__(self, node: Node, knob_type=KnobType.Input):
        super(Knob, self).__init__()
        self.id = uuid.uuid1()
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.node = node
        self.knob_type = knob_type
        self.index = len([n for n in node.knobs if n.knob_type == knob_type]) + 1
        if knob_type == KnobType.Input:
            self.setBrush(QColor(44, 78, 133))
            self.setRect(node.boundingRect().width() - _KNOB_SIZE,
                         self.index * _KNOB_OFFSET,
                         _KNOB_SIZE, _KNOB_SIZE)
        else:
            self.setBrush(QColor(147, 175, 219))
            self.setRect(0,
                         self.index * _KNOB_OFFSET,
                         _KNOB_SIZE, _KNOB_SIZE)

    def itemChange(self, change, value):
        return super(Knob, self).itemChange(change, value)


class Edge(QGraphicsPathItem):
    def __init__(self, connection, node):
        super(Edge, self).__init__()
        self.node = node
        self.connection = connection

    def delete(self):
        self.scene().removeItem(self)
        other_connection = self.connection.destination_connection()
        if other_connection:
            other_connection.delete()
        self.connection.delete()
        # self.node.remove_connection(self.connection)
        del self

    def rect(self):
        return self.boundingRect()


class Connection:
    @staticmethod
    def FromJson(source_node, destination_node, data):
        source = Knob.FromJson(source_node, data.get('source', {}))
        destination = Knob.FromJson(destination_node, data.get('destination', {}))
        connection = Connection(source, destination, source.knob_type == KnobType.Input)
        return connection

    def json(self):
        return {
            'source': self.source,
            'destination': self.destination
        }

    def __init__(self, source: Knob, destination: Knob, has_path):
        self.source = source
        self.destination = destination
        self.path_item = None
        if has_path:
            self.path_item = Edge(self, source.node)
            self.path_item.setFlag(QGraphicsItem.ItemIsSelectable)
            self.path_item.setZValue(-1)
            self.path_item.setPen(QPen(QColor(66, 135, 245), 15))
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

    def destination_connection(self):
        connection = [c for c in self.destination.node.connections if c.destination == self.source]
        if connection:
            return connection[0]

    def update_path(self):
        if self.path_item:
            src = self.source.mapToScene(self.source.rect().center())
            dest = self.destination.mapToScene(self.destination.rect().center())
            self.path.setElementPositionAt(0, src.x(), src.y())
            y = 0 if src.x() < dest.x() else -((abs(dest.y()-src.y())/10)+250)
            x = 50 if src.x() < dest.x() else ((abs(dest.x()-src.x())/10)+250)
            self.path.setElementPositionAt(1, src.x() + x, src.y()+y)
            self.path.setElementPositionAt(2, dest.x() - x, dest.y()+y)
            self.path.setElementPositionAt(3, dest.x(), dest.y())
            self.path_item.setPath(self.path)
            if self.path_item.isSelected():
                self.path_item.setPen(QPen(QColor(255, 255, 255), 20))
            else:
                self.path_item.setPen(QPen(QColor(66, 135, 245), 15))

    def delete(self):
        self.source.node.remove_connection(self)
