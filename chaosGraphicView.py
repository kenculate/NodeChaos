from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from lib import *
from chaosGraphicScene import ChaosGraphicScene
from chaosNode import *
import math

_ZOOM_STEP = 1.1


class NodeData:
    def __init__(self):
        self.nodes: [ChaosNode] = []
        self.nodes.append(ChaosNode(V2d(100, 100), name='Node1'))
        self.nodes.append(ChaosNode(V2d(350, 100), name='Node2'))


class ChaosGraphicView(QGraphicsView):
    def __init__(self, parent):
        super(ChaosGraphicView, self).__init__(parent)
        self.scene = ChaosGraphicScene()
        self.node_data = NodeData()
        self.hscrol = V2d(self.horizontalScrollBar().minimum(), self.horizontalScrollBar().maximum())
        self.vscrol = V2d(self.verticalScrollBar().minimum(), self.verticalScrollBar().maximum())
        self.setScene(self.scene)
        self.setFixedSize(900, 700)
        self.scene.setSceneRect(self.geometry())

        self.path = QGraphicsPathItem()
        self.path.setFlag(QGraphicsItem.ItemIsSelectable, False)
        # self.path.setZValue(1)
        self.path.setPen(QPen(Qt.red, 5))
        self.scene.addItem(self.path)
        self.selected_knob =None
        for node in self.node_data.nodes:
            self.scene.addItem(node)
            for knob in node.knobs:
                self.scene.addItem(knob)
                knob.setParentItem(node)

        self.__panning = False
        self.__last_pos = QPointF()
        self.__current_zoom = 1
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # self.centerOn(self.sceneRect().center())
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def paintEvent(self, event):
        super(ChaosGraphicView, self).paintEvent(event)
        self.update()
        self.scene.update()

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
            self.setDragMode(QGraphicsView.NoDrag)
            self.__panning = True
            self.__last_pos = event.pos()
            self.setCursor(Qt.SizeAllCursor)

        item = self.itemAt(event.pos())
        if item:
            print('item', item)
            if type(item) == Knob:
                if self.selected_knob:
                    if item.node == self.selected_knob:
                        self.selected_knob = None
                        self.path.setVisible(False)
                    else:
                        self.selected_knob.node.add_connection(self.scene, self.selected_knob, item)
                else:
                    self.selected_knob = item
                    self.path.setVisible(True)
                    self.draw_current_edge(event.pos())
            else:
                self.selected_knob = None
                self.path.setVisible(False)
        else:
            self.selected_knob = None
            self.path.setVisible(False)

        super(ChaosGraphicView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event:QMouseEvent):
        self.__panning = False
        self.setCursor(Qt.ArrowCursor)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        super(ChaosGraphicView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event:QMouseEvent):
        self.draw_current_edge(event.pos())
        if self.pan(event.pos()):
            return
        super(ChaosGraphicView, self).mouseMoveEvent(event)

    def pan(self, pos):
        if self.__panning:
            delta = (
                (self.mapToScene(pos) * self.__current_zoom)
                - (self.mapToScene(self.__last_pos) * self.__current_zoom))*-1.0
            length = (delta.x() + delta.y()) / 2
            if length != 0:
                center = QPoint(self.viewport().width() / 2 + delta.x(),
                                self.viewport().height() / 2 + delta.y())
                self.centerOn(self.mapToScene(center))
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
                self.__last_pos = pos
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
                return True
        return False

    def draw_current_edge(self, pos):
        pos = self.mapToScene(pos)
        if self.selected_knob:
            maped = self.selected_knob.mapToScene(self.selected_knob.rect().center())
            t1 = QPointF(50, 0)
            t2 = QPointF(-50, 0)
            if self.selected_knob.knobType == KnobType.Output:
                t1 = QPointF(-50, 0)
                t2 = QPointF(50, 0)
            path = QPainterPath()
            path.moveTo(maped)
            path.cubicTo(
                maped.x() + t1.x(),
                maped.y() + t1.y(),
                pos.x() + t2.x(),
                pos.y() + t2.y(),
                pos.x(),
                pos.y())
            self.path.setPath(path)
            self.update()