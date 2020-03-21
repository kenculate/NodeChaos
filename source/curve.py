from PySide2.QtWidgets import *


class Curve(QGraphicsPathItem):
    def __init__(self, connection, node):
        super(Curve, self).__init__()
        self.node = node
        self.connection = connection

    def delete(self):
        self.scene().removeItem(self)
        other_connection = self.connection.destination_connection()
        if other_connection:
            other_connection.delete()
        self.connection.delete()
        del self

    def rect(self):
        return self.boundingRect()
