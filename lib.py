from PySide2.QtCore import QPointF


def to_json(obj):
    try:
        return obj.json()
    except Exception as err:
        print('ERROR TO JSON', obj, err)

class V2d:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    @staticmethod
    def FromJson(data):
        v = V2d()
        v.x = data.get('x', 0.0)
        v.y = data.get('y', 0.0)
        return v

    def xy(self):
        return (self.x, self.y)

    def setxy(self, x, y):
        self.x = x
        self.y = y

    def pointf(self):
        return QPointF(self.x, self.y)

    def ix(self):
        return int(self.x)

    def iy(self):
        return int(self.y)

    def __add__(self, other):
        return V2d(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        return V2d(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'({self.x},{self.y})'

    def json(self):
        return {'x': self.x, 'y': self.y}