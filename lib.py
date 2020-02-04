class V2d:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def setxy(self, x, y):
        self.x = x
        self.y = y

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