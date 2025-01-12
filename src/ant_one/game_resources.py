

class World():
    """Defines the environment where the game happens.
    px_size: Canvas area available in pixels"""
    def __init__(self, px_size):
        self.px_size = px_size
        self.size = px_size
    


class Ant():
    """Defines ants"""
    pass


class Colony():
    """Defines the colony of ants that Ant One leads"""
    pass


class Nest():
    """Defines where the colony of Ant One lives"""
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
