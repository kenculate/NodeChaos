from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

_GRID_STEP = 2000
_GRID_SUB_STEP = 200


class ChaosGraphicScene(QGraphicsScene):

    def drawBackground(self, painter:QPainter, rect:QRectF):
        painter.setBrush(QColor(200, 200, 200))
        painter.drawRect(self.sceneRect())
        self.draw_grid(painter)
        painter.setPen(Qt.black)
        painter.drawText(rect.left()+20, rect.bottom()-20, 'N to add node, F to frame selection')

    def drawForeground(self, painter, rect):
        super(ChaosGraphicScene, self).drawForeground(painter, rect)

    def draw_grid(self, painter):
        painter.setPen(Qt.black)
        for x in range(0, int(self.sceneRect().width()), _GRID_STEP):
            painter.drawLine(
                self.sceneRect().left() + x,
                self.sceneRect().top(),
                self.sceneRect().left() + x,
                self.sceneRect().bottom()
            )
        for y in range(0, int(self.sceneRect().height()), _GRID_STEP):
            painter.drawLine(
                self.sceneRect().left(),
                self.sceneRect().top() + y,
                self.sceneRect().right(),
                self.sceneRect().top() + y
            )
        painter.setPen(Qt.darkGray)
        for x in range(0, int(self.sceneRect().width()), _GRID_SUB_STEP):
            if x % _GRID_STEP != 0:
                painter.drawLine(
                    self.sceneRect().left() + x,
                    self.sceneRect().top(),
                    self.sceneRect().left() + x,
                    self.sceneRect().bottom()
                )
        for y in range(0, int(self.sceneRect().height()), _GRID_SUB_STEP):
            if y % _GRID_STEP != 0:
                painter.drawLine(
                    self.sceneRect().left(),
                    self.sceneRect().top() + y,
                    self.sceneRect().right(),
                    self.sceneRect().top() + y
                )
