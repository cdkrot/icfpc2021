from structures import *


class Physics(Transformation):

    def __init__(self, k=0.05):
        super(Transformation, self).__init__()
        self.k = k

    def apply(self, data: Input, cur: VerticesList) -> VerticesList:
        print(data)
        print(cur)
        
        forces = [Vec() for _ in cur]
        vertices = []

        for i, e in enumerate(data.figure.edges):
            a, b = data.figure.vertices[e[0]], data.figure.vertices[e[1]]
            a_cur, b_cur = cur[e[0]], cur[e[1]]
            delta = Vec.dist(a, b) - Vec.dist(a_cur, b_cur)
            forces[e[0]] += self.k * delta * (a_cur - b_cur).norm()
            forces[e[1]] += self.k * delta * (b_cur - a_cur).norm()

        for i, v in enumerate(cur):
            vertices.append(v + forces[i])

        print(vertices)
        print()
        return VerticesList(vertices)
