from PySide2.QtWidgets import *
from PySide2.QtGui import *
from source.knobType import KnobType
from source.knob import Knob
from source.curve import Curve


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
            self.path_item = Curve(self, source.node)
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
            # print(f'source: {self.source.node.detail.title} {self.source.knob_type} dest: {self.destination.node.detail.title} {self.destination.knob_type}')
            src = self.source.mapToScene(self.source.rect().center())
            dest = self.destination.mapToScene(self.destination.rect().center())
            x = 50 if src.x() < dest.x() else ((abs(dest.x()-src.x())/10)+250)
            y = 0 if src.x() < dest.x() else -((abs(dest.y()-src.y())/10)+250)
            self.path.setElementPositionAt(0, src.x(), src.y())
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
