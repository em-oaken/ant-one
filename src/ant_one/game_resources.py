
import logging
import math
import random


class Length(float):
    """Defines a length int he World"""
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


class World():
    """Defines the environment where the game happens.
    tau: Time engine handling objects and events
    px_size: Canvas area available in pixels
    
    to_px: Converter from World dimension to pixels. Assumes that ratio is the same on both axis."""
    def __init__(self, tau, px_size):
        self.tau = tau
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
    
    def provide_newborn_position(self):
        return Position(
                random.randint(round(self.size[0]*0.1), int(self.size[0]*0.9)), 
                random.randint(round(self.size[1]*0.1), int(self.size[1]*0.9))
            )
    
    def make_position_around(self, point: Position, radius=0):
        theta = 2*math.pi*random.random()
        x = point.x + radius * math.cos(theta)
        y = point.y + radius * math.sin(theta)
        return Position(x, y, theta)


class Nest():
    """Defines where the colony of Ant One lives"""
    def __init__(self, world):
        self.world = world
        position, radius_max = self.world.make_nest()
        self.position = position
        self.radius = random.randint(
            round(radius_max*0.05),
            round(radius_max*0.10)
        )
    
    def give_newborn_position(self):
        """Generates a newborn position around the nest"""
        return self.world.make_position_around(
            point=self.position,
            radius=self.radius
        )
    
    @property
    def x(self):
        return self.position.x
    
    @property
    def y(self):
        return self.position.y    


class Ant():
    """Defines ants"""
    def __init__(self, colony):
        self.colony = colony
        self.position = self.colony.nest.give_newborn_position()
        self.colony.nest.world.tau.add_object(self)  # Add the ant to the monitored objects
    
    def live(self):
        """Called frequently by Tau"""
        self.position.x += random.randint(-10, 10)
        self.position.y += random.randint(-10, 10)
    
    @property
    def x(self):
        return self.position.x
    
    @property
    def y(self):
        return self.position.y
    
    @property
    def o(self):
        return self.position.o
    


class Colony():
    """Defines the colony of ants that Ant One leads"""
    def __init__(self, nest):
        self.nest = nest
        self.population = []

    def populate(self, n_ants):
        newborns = [Ant(self) for _ in range(n_ants)]
        self.population.extend(newborns)


class Resource():
    """Defines a resource"""
    pass


class Food(Resource):
    """Defines food"""
    pass


class ConstructionMaterial(Resource):
    """Defines construction materials"""
    pass
