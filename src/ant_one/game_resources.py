
import logging
import math
import random
from enum import Enum

from .tau import Tau
from .world_physics import Length, Position


class World():
    """Defines the environment where the game happens.
    tau: Time engine handling objects and events
    px_size: Canvas area available in pixels
    
    to_px: Converter from World dimension to pixels. Assumes that ratio is the same on both axis."""
    def __init__(self, tau: Tau, px_size: int) -> None:
        self.tau = tau
        self.px_size = px_size  # e.g. 1000
        self.size = px_size  # e.g. 5000
        self.no_go_border = 20  # In game units

        self.living_objects = []
    
    def add_life(self, object):
        self.living_objects.append(object)
    
    def to_px(self, x: Length) -> int:
        return round(x*self.px_size[0]/self.size[0])
    
    def make_nest(self) -> tuple[Position, Length]:
        return (
            Position(
                random.randint(round(self.size[0]*0.1), int(self.size[0]*0.9)), 
                random.randint(round(self.size[1]*0.1), int(self.size[1]*0.9))
            ),
            Length(round(self.size[0]*0.1))
        )
    
    def provide_newborn_position(self) -> Position:
        return Position(
                random.randint(round(self.size[0]*0.1), int(self.size[0]*0.9)), 
                random.randint(round(self.size[1]*0.1), int(self.size[1]*0.9))
            )
    
    def make_position_around(self, point: Position, radius: int=0) -> Position:
        theta = 2*math.pi*random.random()
        x = point.x + radius * math.cos(theta)
        y = point.y + radius * math.sin(theta)
        return Position(x, y, theta)
    
    def validate_position(self, position: Position) -> tuple[bool, Position]:
        validated = True
        new_x, new_y = None, None
        if position.x < self.no_go_border:
            validated = False
            new_x = self.no_go_border
        elif position.x > self.size[0]-self.no_go_border:
            validated = False
            new_x = self.size[0]-self.no_go_border
        if position.y < self.no_go_border:
            validated = False
            new_y = self.no_go_border
        elif position.y > self.size[1]-self.no_go_border:
            validated = False
            new_y = self.size[1]-self.no_go_border

        if validated:
            return True, position
        return (
            False,
            Position(
                new_x or position.x,
                new_y or position.y,
                position.o
            )
        )


class Nest():
    """Defines where the colony of Ant One lives"""
    def __init__(self, world: World) -> None:
        self.world = world
        position, radius_max = self.world.make_nest()
        self.position = position
        self.radius = random.randint(
            round(radius_max*0.05),
            round(radius_max*0.10)
        )
    
    def give_newborn_position(self) -> Position:
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


class Colony():
    """Defines the colony of ants that Ant One leads"""
    def __init__(self, nest: Nest) -> None:
        self.nest = nest
        self.population = []

    def populate(self, n_ants: int) -> None:
        newborns = [Ant(self) for _ in range(n_ants)]
        self.population.extend(newborns)
    
    def ant_birth(self):
        position = self.nest.give_newborn_position()
        job = Job.FORAGING
        return position, job


class Job(Enum):
    FORAGING = 'Foraging'


class Ant():
    """Defines ants"""
    def __init__(self, colony: Colony) -> None:
        self.colony = colony
        self.world = self.colony.nest.world
        
        # Properties
        self.max_pace = 100  # In game-length-units per second

        # Status
        self.position, self.job = self.colony.ant_birth()
        self.speed_factor_h = [0, 0]

        self.world.add_life(self)  # Allow the ant to be alive
    
    def live(self) -> None:
        """Called frequently by Tau"""
        if self.job == Job.FORAGING:
            new_pos, speed_factor = self.gen_random_movement()
            new_pos_acceptable, closest_pos = self.world.validate_position(new_pos)
            if not new_pos_acceptable:
                new_pos = closest_pos
                speed_factor = 0
            self.speed_factor_h.append(speed_factor)
            self.speed_factor_h.pop(0)
            self.change_position(new_pos)
    
    def gen_random_movement(self) -> Position:
        # First go straight, then turn
        new_speed_factor = random.random()
        new_speed_factor_h = self.speed_factor_h + [new_speed_factor]
        speed_factor = sum(new_speed_factor_h) / 3
        max_distance = self.max_pace*self.world.tau.loop_duration

        move_x = -round(max_distance*speed_factor*math.cos(self.o))
        move_y = -round(max_distance*speed_factor*math.sin(self.o))
        new_x = self.x + move_x
        new_y = self.y + move_y

        rotation_angle = random.gauss(sigma=6)*self.world.tau.loop_duration
        rotation = max(0, 1-speed_factor*2) * rotation_angle  # The more speed, the less turning
        new_o = (self.o + rotation * math.pi)
        return Position(new_x, new_y, new_o), speed_factor

    def change_position(self, new_pos: Position) -> None:
        self.position.x = new_pos.x
        self.position.y = new_pos.y
        self.position.o = new_pos.o

    @property
    def x(self):
        return self.position.x
    
    @property
    def y(self):
        return self.position.y
    
    @property
    def o(self):
        return self.position.o


class Resource():
    """Defines a resource"""
    pass


class Food(Resource):
    """Defines food"""
    pass


class ConstructionMaterial(Resource):
    """Defines construction materials"""
    pass
