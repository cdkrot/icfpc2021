from structures import *


class Physics(Transformation):
    def __init__(cls, k=1):
        Transformation.__init__(cls)
        cls.k = k

    def apply(self, data: Input) -> VerticesList:
        forces = [Vec() for _ in data.figure.vertices.vertices]
        vertices = []

        for i, e in enumerate(data.figure.edges):
            forces[e[0]] += self.k * (e[1] - e[0])

        for i, v in enumerate(data.figure.vertices.vertices):
            vertices += v + forces[i]

        return VerticesList(vertices)
