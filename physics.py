from structures import *


class Physics(Transformation):
    def __init__(self, k):
        self.k = k

    def apply(self, data: Input) -> VerticesList:
        forces = [Vec() for _ in data.figure.vertices.vertices]
        vertices = []

        for i, e in enumerate(data.figure.edges):
            forces[e[0]]

        for v in data.figure.vertices.vertices:
            vertices += 0

        return VerticesList(vertices)
