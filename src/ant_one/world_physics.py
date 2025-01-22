

class Length(float):
    """Defines a length in the World"""
    def __init__(self, x):
        self.x = x


class Position():
    """Defines a position in the World.
    May also define orientation of a body (designed for ants representation)"""
    def __init__(self, x, y, orientation=0):
        self.x = x
        self.y = y
        self.orientation = orientation  # alias = o
    
    @property
    def o(self):
        return self.orientation
    
    @o.setter
    def o(self, value):
        self.orientation = value

    def __repr__(self):
        return f'Position (X={self.x:.0f}, Y={self.y:.0f}, o={self.o:.2f})'