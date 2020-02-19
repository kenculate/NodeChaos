from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from lib import *


_GRID_STEP = 2000
_GRID_SUB_STEP = 200


class ChaosGraphicScene(QGraphicsScene):

    def drawBackground(self, painter:QPainter, rect:QRectF):
        self.painter = painter
        painter.setBrush(QColor(200, 200, 200))
        painter.drawRect(self.sceneRect())
        self.draw_grid(painter)

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
