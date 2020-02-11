from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from lib import *
from nodeData import *
from chaosGraphicScene import ChaosGraphicScene
from chaosNode import ChaosNode
import math

_ZOOM_STEP = 1.1

class ChaosGraphicView(QGraphicsView):
    def __init__(self, parent):
        super(ChaosGraphicView, self).__init__(parent)
        self.scene = ChaosGraphicScene()
        self.hscrol = V2d(self.horizontalScrollBar().minimum(), self.horizontalScrollBar().maximum())
        self.vscrol = V2d(self.verticalScrollBar().minimum(), self.verticalScrollBar().maximum())
        self.setScene(self.scene)
        self.setFixedSize(900, 700)
        self.scene.setSceneRect(self.geometry())
        self.scene.addItem(ChaosNode(V2d(100, 100)))
        self.__panning = False
        self.__last_pos = QPointF()
        self.__current_zoom = 1
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # self.centerOn(self.sceneRect().center())
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    # def resizeEvent(self, event:QResizeEvent):
    #     if self.scene.sceneRect().width() == 100:
    #         rect = self.geometry()
    #     else:
    #         rect = self.scene.sceneRect()
    #         rect.setLeft(rect.left()+self.hscrol.x)
    #         rect.setRight(rect.right()+self.hscrol.y)
    #         rect.setTop(rect.top()+self.vscrol.x)
    #         rect.setBottom(rect.bottom()+self.vscrol.y)
    #     self.scene.setSceneRect(rect)
    #     self.centerOn(self.scene.sceneRect().center())
    #     super(ChaosGraphicView, self).resizeEvent(event)
    #     event.accept()

    def wheelEvent(self, event:QWheelEvent):
        zoom = _ZOOM_STEP if event.delta() >= 0 else 1.0/_ZOOM_STEP
        self.scale(zoom, zoom)
        self.__current_zoom = self.transform().m11()
        rect = self.scene.sceneRect()
        rect.setLeft(rect.left() + (rect.width() * 0.1 * math.copysign(1, event.delta())))
        rect.setRight(rect.right() + (rect.width() * -0.1 * math.copysign(1, event.delta())))
        rect.setTop(rect.top() + (rect.height() * 0.1 * math.copysign(1, event.delta())))
        rect.setBottom(rect.bottom() + (rect.height() * -0.1 * math.copysign(1, event.delta())))

        self.scene.setSceneRect(rect)
        # self.centerOn(self.scene.sceneRect().center())
        print(rect, (event.delta()/event.delta()))

    def mousePressEvent(self, event:QMouseEvent):
        self.__panning = False
        if event.button() == Qt.MiddleButton:
            self.__panning = True
            self.__last_pos = event.pos()
            self.setCursor(Qt.SizeAllCursor)
        super(ChaosGraphicView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event:QMouseEvent):
        self.__panning = False
        self.setCursor(Qt.ArrowCursor)
        super(ChaosGraphicView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event:QMouseEvent):
        if self.__panning:
            delta = (
                (self.mapToScene(event.pos()) * self.__current_zoom)
                - (self.mapToScene(self.__last_pos) * self.__current_zoom))*-1.0
            length = (delta.x() + delta.y()) / 2
            if length != 0:
                center = QPoint(self.viewport().width() / 2 + delta.x(),
                                self.viewport().height() / 2 + delta.y())
                self.centerOn(self.mapToScene(center))
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
                self.__last_pos = event.pos()
                rect = self.scene.sceneRect()
                if delta.x() < 0:
                    if self.horizontalScrollBar().value() <= self.horizontalScrollBar().minimum():
                        self.horizontalScrollBar().setMinimum(self.horizontalScrollBar().minimum() + delta.x())
                        rect.setLeft(rect.left() + delta.x())
                elif delta.x() > 0:
                    if self.horizontalScrollBar().value() >= self.horizontalScrollBar().maximum():
                        self.horizontalScrollBar().setMaximum(self.horizontalScrollBar().maximum() + delta.x())
                        rect.setRight(rect.right() + delta.x())
                if delta.y() < 0:
                    if self.verticalScrollBar().value() <= self.verticalScrollBar().minimum():
                        self.verticalScrollBar().setMinimum(self.verticalScrollBar().minimum() + delta.y())
                        rect.setTop(rect.top() + delta.y())
                elif delta.y() > 0:
                    if self.verticalScrollBar().value() >= self.verticalScrollBar().maximum():
                        self.verticalScrollBar().setMaximum(self.verticalScrollBar().maximum() + delta.y())
                        rect.setBottom(rect.bottom() + delta.y())
                self.scene.setSceneRect(rect)
                return
        super(ChaosGraphicView, self).mouseMoveEvent(event)
