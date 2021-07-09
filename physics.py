from structures import *


class Physics(Transformation):

    def __init__(self, k=0.5):
        super(Transformation, self).__init__()
        self.k = k

    def apply(self, data: Input, cur: VerticesList) -> VerticesList:
        forces = [Vec() for _ in cur]
        vertices = []

        for i, e in enumerate(data.figure.edges):
            a, b = data.figure.vertices[e[0]], data.figure.vertices[e[1]]
            a_cur, b_cur = cur[e[0]], cur[e[1]]
            delta = (Vec.dist(a, b) - Vec.dist(a_cur, b_cur)) / Vec.dist(a, b)
            forces[e[0]] += self.k * delta * (a - b)
            forces[e[1]] += self.k * delta * (b - a)

        for i, v in enumerate(data.figure.vertices):
            vertices.append(v + forces[i])

        return VerticesList(vertices)
