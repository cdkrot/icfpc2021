from structures import Vec
import typing


def on_segment(p: Vec, a: Vec, b: Vec):
    return Vec.cross(a - p, a - b) == 0 and Vec.dot(p - a, p - b) <= 0


def dist(p: Vec, a: Vec, b: Vec):
    if Vec.dot(b - a, p - a) < 0:
        return (p - a).len()
    
    if Vec.dot(a - b, p - b) < 0:
        return (p - b).len()

    return abs((a - p).cross(b - p)) / (a - b).len()


def inside_polygon(p: Vec, polygon: typing.List[Vec]):
    for i in range(len(polygon)):
        if on_segment(p, polygon[i], polygon[(i + 1) % len(polygon)]):
            return True

    count = 0
    for i in range(len(polygon)):
        a = polygon[i]
        b = polygon[(i + 1) % len(polygon)]

        if a.y == b.y:
            continue

        if p.y < min(a.y, b.y) or p.y > max(a.y, b.y):
            continue
        
        if a.y > b.y:
            a, b = b, a

        if Vec.cross(p - a, b - a) < 0:
            count += 1

    return count % 2 == 1
