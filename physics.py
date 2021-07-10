from structures import *


class Physics(Transformation):
    def __init__(self, k=0.05, is_pinned=None):
        super(Transformation, self).__init__()
        self.k = k
        self.is_pinned = is_pinned

    def apply(self, data: Input, cur: VerticesList) -> VerticesList:
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
            delta = Vec.dist(a, b) - Vec.dist(a_cur, b_cur)
            
            forces[e[0]] += self.k * delta * (a_cur - b_cur).norm()
            forces[e[1]] += self.k * delta * (b_cur - a_cur).norm()

        if self.is_pinned:
            for i, val in enumerate(self.is_pinned):
                if val:
                    forces[i] = Vec()
            
        for i, v in enumerate(cur):
            vertices.append(v + forces[i])

        return VerticesList(vertices)
