
import random


class Length(float):
    """Defines a length int he World"""
    def __init__(self, x):
        self.x = x


class Position():
    """Defines a position in the World."""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class World():
    """Defines the environment where the game happens.
    px_size: Canvas area available in pixels
    
    to_px: Converter from World dimension to pixels. Assumes that ratio is the same on both axis."""
    def __init__(self, px_size):
        self.px_size = px_size  # e.g. 1000
        self.size = px_size  # e.g. 5000
    
    def to_px(self, x):
        return round(x*self.px_size[0]/self.size[0])
    
    def make_nest(self):
        return (
            Position(
                random.randint(round(self.size[0]*0.1), int(self.size[0]*0.9)), 
                random.randint(round(self.size[1]*0.1), int(self.size[1]*0.9))
            ),
            Length(round(self.size[0]*0.1))
        )


class Nest():
    """Defines where the colony of Ant One lives"""
    def __init__(self, position, radius_max):
        self.position = position
        self.radius = random.randint(
            round(radius_max*0.05),
            round(radius_max*0.6)
        )
    
    @property
    def x(self):
        return self.position.x
    
    @property
    def y(self):
        return self.position.y    


class Ant():
    """Defines ants"""
    pass


class Colony():
    """Defines the colony of ants that Ant One leads"""
    pass


class Resource():
    """Defines a resource"""
    pass


class Food(Resource):
    """Defines food"""
    pass


class ConstructionMaterial(Resource):
    """Defines construction materials"""
    pass
