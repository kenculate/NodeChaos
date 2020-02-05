from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from lib import *
from nodeData import *


class ChaosGraphicView(QGraphicsView):

    def __init__(self, parent):
        super(ChaosGraphicView, self).__init__(parent)
        self.zoom = 0
        self.zoom_scale = 1
        self.panning = False
        self.last_mouse_pos = QPoint()
        # self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        # self.setDragMode(QGraphicsView.NoDrag)

    # def dragMoveEvent(self, event:QDragMoveEvent):
    #     if self.itemAt(event.pos()):
    #         event.ignore()
    #         return
    #     super(ChaosGraphicView, self).dragMoveEvent(event)
    #     event.accept()

    def wheelEvent(self, event:QWheelEvent):
        # self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.zoom = 1.1 if event.angleDelta().y() > 0 else 0.9
        self.zoom_scale *= self.zoom
        self.scale(self.zoom, self.zoom)
        self.scene().setSceneRect(self.rect_scale(self.sceneRect(), self.zoom_scale))
        # self.centerOn(self.sceneRect().center())
        super(ChaosGraphicView, self).wheelEvent(event)
        event.accept()


    def rect_scale(self, rect, scale):
        dx = rect.width()*scale - rect.width()
        dy = rect.height()*scale - rect.height()
        scaled = QRectF(rect.x()+dx, rect.y()+dy, rect.width()-dx, rect.height()-dy)
        print(scaled)
        return scaled


    def mousePressEvent(self, event:QMouseEvent):
        print(event.button())

        if event.button() == Qt.MiddleButton:
            self.panning = True
            self.last_mouse_pos = event.pos()
            # self.setDragMode(QGraphicsView.ScrollHandDrag)
            # _event = QMouseEvent(QEvent.MouseButtonPress, QPointF(event.pos()), Qt.LeftButton, event.buttons(),
            #                              Qt.KeyboardModifiers())
            # self.mousePressEvent(_event)

        super(ChaosGraphicView, self).mousePressEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event:QMouseEvent):
        self.panning = False

        # if event.button() == Qt.MiddleButton:

            # self.setDragMode(QGraphicsView.NoDrag)
            # _event = QMouseEvent(QEvent.MouseButtonRelease, QPointF(event.pos()), Qt.LeftButton, event.buttons(),
            #                      Qt.KeyboardModifiers())
            # self.mouseReleaseEvent(_event)
        super(ChaosGraphicView, self).mouseReleaseEvent(event)
        event.accept()

    def mouseMoveEvent(self, event:QMouseEvent):
        if self.panning:
            rect = self.sceneRect()
            rect.setX(rect.x() + event.pos().x() - self.last_mouse_pos.x())
            rect.setY(rect.y() + event.pos().y() - self.last_mouse_pos.y())
            self.scene().setSceneRect(rect)
            self.setSceneRect(rect)
            # self.translate(
            #     rect.x() + event.pos().x() - self.last_mouse_pos.x(),
            #     rect.y() + event.pos().y() - self.last_mouse_pos.y()
            # )
            self.update()
            self.scene().update()

        super(ChaosGraphicView, self).mouseMoveEvent(event)
        self.last_mouse_pos = event.pos()
        event.accept()
