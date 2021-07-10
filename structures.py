import typing
import copy
from abc import ABCMeta, abstractmethod
from shapely.geometry import Polygon


class Vec:
    @staticmethod
    def dist2(a, b):
        return (a.x - b.x) ** 2 + (a.y - b.y) ** 2

    @staticmethod
    def dist(a, b):
        return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vec({self.x}, {self.y})'

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __imul__(self, k):
        self.x *= k
        self.y *= k
        return self

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __rmul__(self, k):
        return Vec(k * self.x, k * self.y)

    def len2(self):
        return self.x * self.x + self.y * self.y

    def len(self):
        return self.len2() ** 0.5

    @staticmethod
    def dot(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def cross(v1, v2):
        return v1.x * v2.y - v1.y * v2.x

    def norm(v):
        return Vec(v.x / v.len(), v.y / v.len())

    def __eq__(self, b):
        return self.x == b.x and self.y == b.y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def to_tuple(self):
        return (self.x, self.y)

# Hole
# solution
# Figure.vertices
class VerticesList:
    def __init__(self, vertices: typing.List[Vec] = []):
        self.vertices = copy.deepcopy(vertices)

    def read_json(self, data: typing.List[list]):
        self.vertices = [Vec(pt[0], pt[1]) for pt in data]

    def to_json(self):
        return [[vec.x, vec.y] for vec in self.vertices]

    def __repr__(self):
        return 'VerticesList([' + ','.join(repr(v) for v in self.vertices) + '])'

    def __getitem__(self, i):
        return self.vertices[i]

    def __setitem__(self, i, val):
        self.vertices[i] = val

    def __len__(self):
        return len(self.vertices)
    
    # interprets the vertices list as a shapley polygon
    def to_polygon(self):
        return Polygon([v.to_tuple() for v in self.vertices])


class Figure:
    def __init__(self, vertices: VerticesList = VerticesList(),
                 edges: typing.List[typing.Tuple[int, int]] = []):
        self.vertices = copy.deepcopy(vertices)
        self.edges = copy.deepcopy(edges)

    def read_json(self, data):
        self.vertices.read_json(data['vertices'])
        self.edges = [(pt[0], pt[1]) for pt in data['edges']]

    def __repr__(self):
        return f'Figure(vertices={self.vertices}, edges={self.edges})'


class Input:
    def __init__(self, hole: VerticesList = VerticesList(),
                 figure: Figure = Figure(),
                 epsilon=0,
                 problem_id=None):
        self.hole = copy.deepcopy(hole)
        self.hole_polygon = self.hole.to_polygon()
        self.figure = copy.deepcopy(figure)
        self.epsilon = epsilon
        self.problem_id = problem_id

    def read_json(self, data):
        self.epsilon = data['epsilon']
        self.figure.read_json(data['figure'])
        self.hole.read_json(data['hole'])

    def __repr__(self):
        return f'Input(hole={self.hole}, figure={self.figure}, epsilon={self.epsilon})'


class Transformation(object, metaclass=ABCMeta):

    def __init__(self):
        pass

    @staticmethod
    def apply_all(transformations, data: Input):
        vertices = copy.deepcopy(data.figure.vertices)
        for t in transformations:
            vertices = t.apply(data, vertices)
        return vertices

    @abstractmethod
    def apply(self, data: Input, cur: VerticesList) -> VerticesList:
        return data.figure.vertices
