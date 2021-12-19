from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from source.lib import *
import uuid
from source.nodeDetail import NodeDetail
from source.knobType import KnobType
from source.knob import Knob
from source.knob import _KNOB_SIZE
from source.connection import Connection

_NODE_BORDER = 10


class Node(QGraphicsItem):

    @staticmethod
    def FromJson(data):
        name = data.get('name', '')
        position = V2d.FromJson(data.get('position', {}))
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
            'connections': [c for c in self.connections if c.path_item]
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

    def contextMenuEvent(self, event):
        menu = QMenu()
        menu.addAction("set story begin", self.set_initial)
        menu.exec_(QCursor.pos())

    def set_initial(self):
        print('intial')

    def delete(self):
        self.scene().removeItem(self)
        del self

    def setup_connection(self, node, nodes, scene):
        for connection in node.get('connections', []):
            source_knob = [
                kn for kn in self.knobs
                if kn.id == connection.get('source', {}).get('id', 0)
            ]
            # if connection.get('source', {}).get('knob_type', 0) == 1:
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
            painter.drawText(20, 20, f'{self.detail.title} {self.detail.description}')

        if self.detail.text:
            painter.setPen(Qt.black)
            painter.drawText(self.scale_rect(self.boundingRect(), _KNOB_SIZE, 50), self.detail.text)
        for connection in self.connections:
            connection.update_path()




