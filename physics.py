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

        def sign(a):
            if a < 0:
                return -1
            if a > 0:
                return +1
            return 0

        deltas = []
        dists = []
        for i, e in enumerate(data.figure.edges):
            a, b = data.figure.vertices[e[0]], data.figure.vertices[e[1]]
            a_cur, b_cur = cur[e[0]], cur[e[1]]
            import math
            delta = sign(Vec.dist(a, b) - Vec.dist(a_cur, b_cur)) * abs(Vec.dist(a, b) - Vec.dist(a_cur, b_cur)) ** 2
            forces[e[0]] += self.k * delta * (a_cur - b_cur).norm()
            forces[e[1]] += self.k * delta * (b_cur - a_cur).norm()
            deltas.append(delta)
            dists.append((Vec.dist(a, b), Vec.dist(a_cur, b_cur)))

        print(deltas)
        print(dists)
        print(forces)
        for i, v in enumerate(cur):
            vertices.append(v + forces[i])

        print(vertices)
        print()
        return VerticesList(vertices)
