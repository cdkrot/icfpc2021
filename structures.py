import typing
import copy

class Vec:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Figure:
    def __init__(self, points: typing.List[Vec] = [],
                 edges: typing.List[typing.Tuple[int, int]]):
        self.points = copy.deepcopy(points)
        self.edges = copy.deepcopy(edges)
        

class Input:
    def __init__(self, hole: typing.List[Vec] = [],
                 figure: Figure = Figure(),
                 epsilon=0):

        self.hole = copy.deepcopy(hole)
        self.figure = copy.deepcopy(hole)
        self.epsilon = epsilon

