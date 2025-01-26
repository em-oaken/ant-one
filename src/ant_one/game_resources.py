
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
    
    def interact(self, object):
        if isinstance(object, Ant):
            if object.position.distance_from(object.colony.nest.position) < 10:
                logging.info(f'Ant {object.idno} near nest')
        else:
            logging.debug(f'Interaction with {object.__class__.__name__} not covered')
    
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
        self.attraction_radius = 10
    
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
        self.world = self.nest.world
        self.population = []
        self.ant_idno = 0

        self.stock_food = 5.5
        # Needs is the base to define what job will be given to ants
        self.needs = { need: 0 for need in ColonyNeed }
        self.world.add_life(self)

    def populate(self, n_ants: int) -> None:
        newborns = [Ant(self) for _ in range(n_ants)]
        self.population.extend(newborns)
    
    def give_job(self, ant: 'Ant'):
        if self.needs[ColonyNeed.GETFOOD] >= ant.colony_needs_thresholds[ColonyNeed.GETFOOD]:
            return Job.FORAGING
        return Job.JOBLESS
    
    def ant_birth(self) -> tuple[int, Position, 'Job']:
        self.ant_idno += 1
        idno = self.ant_idno
        position = self.nest.give_newborn_position()
        job = Job.JOBLESS
        return idno, position, job
    
    def live(self):
        # Colony looses 1 food unit per minute
        stockfood_decr = - (1/60) * self.world.tau.vt_loop_duration
        self.stock_food = max(0, self.stock_food + stockfood_decr)

        # Need to collect food increases by +0.1/min if stock of food below 5
        needgetfood_incr = 0 if self.stock_food>=5 else (0.1/60)*self.world.tau.vt_loop_duration
        self.needs[ColonyNeed.GETFOOD] = min(1, self.needs[ColonyNeed.GETFOOD]+needgetfood_incr)

        # logging.info(f'Colony has {self.stock_food:.2f} food with a need of {self.needs[ColonyNeed.GETFOOD]:.2f}')


class Job(Enum):
    FORAGING = 'Foraging'
    JOBLESS = 'Jobless'

class ColonyNeed(Enum):
    GETFOOD = 'Collect food'


class Ant():
    """Defines ants"""
    def __init__(self, colony: Colony) -> None:
        self.colony = colony
        self.world = self.colony.nest.world
        
        # Properties
        self.max_pace = 100  # In game-length-units per second
        self.colony_needs_thresholds = { need: random.uniform(0.4, 0.6) for need in ColonyNeed }

        # Status
        self.idno, self.position, self.job = self.colony.ant_birth()
        self.speed_factor_h = [0, 0]

        self.world.add_life(self)  # Allow the ant to be alive
        logging.info(f'Ant #{self.idno} born @({self.x:.0f}, {self.y:.0f}), {self.job.value}. '
                     f'Foraging threshold = {self.colony_needs_thresholds[ColonyNeed.GETFOOD]:.2f}')
    
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

        elif self.job == Job.JOBLESS:
            new_pos, speed_factor = self.gen_random_movement()
            new_pos_acceptable, closest_pos = self.world.validate_position(new_pos)
            if not new_pos_acceptable:
                new_pos = closest_pos
                speed_factor = 0
            
            # If ants goes away from nest, slow her down to bring them back
            curr_pos_dist = self.position.distance_from(self.colony.nest)
            new_pos_dist = new_pos.distance_from(self.colony.nest)
            if (new_pos_dist > 0.9*curr_pos_dist) and (curr_pos_dist >= self.colony.nest.attraction_radius):
                newpos_rel_dist = new_pos_dist / self.colony.nest.attraction_radius
                attraction_factor = newpos_rel_dist**1.5
                new_x = (new_pos.x + self.position.x*attraction_factor)/(1+attraction_factor)
                new_y = (new_pos.y + self.position.y*attraction_factor)/(1+attraction_factor)
                new_o = new_pos.o + random.gauss(0, 0.5)*math.pi/6
                new_pos = Position(new_x, new_y, new_o)
            self.speed_factor_h.append(speed_factor)
            self.speed_factor_h.pop(0)
            self.change_position(new_pos)

    def change_position(self, new_pos: Position) -> None:
        self.position.x = new_pos.x
        self.position.y = new_pos.y
        self.position.o = new_pos.o
        self.world.interact(self)

    def gen_random_movement(self) -> Position:
        # First go straight, then turn
        new_speed_factor = random.random()
        new_speed_factor_h = self.speed_factor_h + [new_speed_factor]
        speed_factor = sum(new_speed_factor_h) / 3
        max_distance = self.max_pace*self.world.tau.vt_loop_duration

        move_x = -round(max_distance*speed_factor*math.cos(self.o))
        move_y = -round(max_distance*speed_factor*math.sin(self.o))
        new_x = self.x + move_x
        new_y = self.y + move_y

        rotation_angle = random.gauss(sigma=6)*self.world.tau.vt_loop_duration
        rotation = max(0, 1-speed_factor*2) * rotation_angle  # The more speed, the less turning
        new_o = (self.o + rotation * math.pi)
        return Position(new_x, new_y, new_o), speed_factor

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
