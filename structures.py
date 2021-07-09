import typing
import copy

class Vec:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vec({self.x}, {self.y})'

    def __add__(self, other: Vec):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec):
        return Vec(self.x - other.x, self.y - other.y)

    def len2(self):
        return self.x * self.x + self.y * self.y


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
                 epsilon=0):
        self.hole = copy.deepcopy(hole)
        self.figure = copy.deepcopy(figure)
        self.epsilon = epsilon

    def read_json(self, data):
        self.epsilon = data['epsilon']
        self.figure.read_json(data['figure'])
        self.hole.read_json(data['hole'])

    def __repr__(self):
        return f'Input(hole={self.hole}, figure={self.figure}, epsilon={self.epsilon})'
