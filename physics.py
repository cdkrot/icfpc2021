from structures import *


class Physics(Transformation):
    def __init__(cls, k=0.5):
        Transformation.__init__(cls)
        cls.k = k

    def apply(self, data: Input, cur: VerticesList) -> VerticesList:
        forces = [Vec() for _ in cur]
        vertices = []

        for i, e in enumerate(data.figure.edges):
            a, b = data.figure.vertices[e[1]], data.figure.vertices[e[2]]
            a_cur, b_cur = cur[e[1]], cur[e[2]]
            delta = (Vec.dist(a, b) - Vec.dist(a_cur, b_cur)) / Vec.dist(a, b)
            forces[e[0]] += self.k * delta * (a - b)
            forces[e[1]] += self.k * delta * (b - a)

        for i, v in enumerate(data.figure.vertices):
            vertices += v + forces[i]

        return VerticesList(vertices)
