from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from lib import *

from nodeData import *

_KNOB_OFFSET = 20
_KNOB_SIZE = 10
_NODE_BORDER = 10


class ChaosGraphicScene(QGraphicsScene):
    def __init__(self, view, node_data:NodeData):
        super(ChaosGraphicScene, self).__init__()
        self.view = view
        self.dragging = False
        self.mouse_pos = QPointF()
        self.mouse_press_pos = QPointF()
        self.background_color = Qt.gray
        self.grid_size = V2d(50, 50)
        self.painter : QPainter = None
        self.node_data = node_data
        for node in node_data.nodes:
            self.addItem(node)
        self.selecting = False
        self.selection_rect = QRect()

    def drawBackground(self, painter:QPainter, rect:QRectF):
        self.painter = painter
        painter.setBrush(QColor(150, 150, 150))
        painter.drawRect(self.sceneRect().left()+50
                         , self.sceneRect().top()
                         , self.sceneRect().right()-100
                         , self.sceneRect().bottom())
        painter.setPen(QColor(100, 100, 100, 100))

        for x in range(0, int(rect.width()), self.grid_size.ix()):
            painter.drawLine(rect.x() + x, rect.y(), rect.x() + x, int(rect.bottom()))
        for y in range(0, int(rect.width()), self.grid_size.ix()):
            painter.drawLine(rect.x(), rect.y() + y, rect.right(), rect.y() + y)

        if self.dragging:
            painter.setPen(Qt.white)
            painter.setBrush(QColor(255, 255, 255, 50))
            painter.drawRect(self.rect())
        super(ChaosGraphicScene, self).drawForeground(painter, rect)
        self.update()

    def rect(self):
        return QRectF(self.mouse_press_pos.x(),
                      self.mouse_press_pos.y(),
                      self.mouse_pos.x() - self.mouse_press_pos.x(),
                      self.mouse_pos.y() - self.mouse_press_pos.y())

    def mousePressEvent(self, event):
        super(ChaosGraphicScene, self).mousePressEvent(event)
        if not self.itemAt(event.scenePos(), self.view.transform()):
            self.clearSelection()
            self.dragging = True
        else:
            self.dragging = False
        self.mouse_pos = event.scenePos()
        self.mouse_press_pos = event.scenePos()
        # event.accept()
        self.update()

    def mouseReleaseEvent(self, event):
        super(ChaosGraphicScene, self).mouseReleaseEvent(event)
        self.dragging = False
        for item in self.items():
            if self.rect().contains(item.selection_rect):
                item.setSelected(True)
        self.update()
        # event.accept()

    def mouseMoveEvent(self, event):
        super(ChaosGraphicScene, self).mouseMoveEvent(event)
        self.mouse_pos = event.scenePos()
        self.update()
        # event.accept()

    def dragMoveEvent(self, event:QGraphicsSceneDragDropEvent):
        super(ChaosGraphicScene, self).dragMoveEvent(event)
        # event.accept()
        print('scene drag')