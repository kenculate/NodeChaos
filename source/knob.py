from PySide2.QtWidgets import *
from PySide2.QtGui import *
from source.knobType import KnobType
import uuid
_KNOB_OFFSET = 40
_KNOB_SIZE = 20


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

    def __init__(self, node, knob_type=KnobType.Input):
        super(Knob, self).__init__()
        self.id = uuid.uuid1()
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptDrops(True)
        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.node = node
        self.knob_type = knob_type
        self.index = len([n for n in node.knobs if n.knob_type == knob_type]) + 1
        if knob_type == KnobType.Output:
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
