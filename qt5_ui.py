from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen

import argparse
import sys
import net


class ICFPCPainter(QWidget):
    POINT_RADIUS = 4
    WIDTH = 700
    HEIGHT = 700
    MARGIN = 50

    def __init__(self, input):
        super(QWidget, self).__init__()
        self.setGeometry(0, 0, ICFPCPainter.WIDTH, ICFPCPainter.HEIGHT)
        self.hole = input.hole
        self.figure = input.figure
        self.dragging = False
        self.init_cds()
        self.show()

    def init_cds(self):
        xs = list(map(lambda x: x.x, self.hole.vertices + self.figure.vertices.vertices))
        ys = list(map(lambda x: x.y, self.hole.vertices + self.figure.vertices.vertices))
        self.min_x, self.max_x = min(xs), max(xs)
        self.min_y, self.max_y = min(ys), max(ys)

    def scale(self, p):
        x, y = p.x, p.y
        mgn = ICFPCPainter.MARGIN
        nx = (x - self.min_x) / (self.max_x - self.min_x) * (ICFPCPainter.WIDTH - 2 * mgn) + mgn
        ny = (y - self.min_y) / (self.max_y - self.min_y) * (ICFPCPainter.HEIGHT - 2 * mgn) + mgn
        return nx, ny

    def unscale(self, p):
        x, y = p
        mgn = ICFPCPainter.MARGIN
        nx = (x - mgn) / (ICFPCPainter.WIDTH - 2 * mgn) * (self.max_x - self.min_x) + self.min_x
        ny = (y - mgn) / (ICFPCPainter.HEIGHT - 2 * mgn) * (self.max_y - self.min_y) + self.min_y
        return net.Vec(nx, ny)

    def paintEvent(self, e):
        self.draw_input()

    def draw_input(self):
        self.qp = QPainter()
        self.qp.begin(self)
        self.draw_hole()
        self.draw_figure()
        self.qp.end()

    def draw_hole(self):
        self.qp.setPen(QPen(Qt.black, Qt.SolidLine))
        for i in range(len(self.hole.vertices)):
            self.draw_line(self.hole.vertices[i - 1], self.hole.vertices[i])

    def draw_figure(self):
        self.qp.setPen(QPen(Qt.red, Qt.SolidLine))
        self.qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        for v in self.figure.vertices.vertices:
            self.draw_point(v)
        for u, v in self.figure.edges:
            self.draw_line(self.figure.vertices.vertices[u], self.figure.vertices.vertices[v])

    def draw_point(self, point):
        r = ICFPCPainter.POINT_RADIUS
        self.qp.drawEllipse(QPoint(*self.scale(point)), r, r)

    def draw_line(self, a, b):
        self.qp.drawLine(QPoint(*self.scale(a)), QPoint(*self.scale(b)))

    def mousePressEvent(self, e):
        self.dragging = True
        print("mouse press", e)

    def mouseMoveEvent(self, e):
        if self.dragging:
            print("mouse move", e)

    def mouseReleaseEvent(self, e):
        self.dragging = True
        print("mouse release", e)


class Figure:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('problem', type=str, help="Problem id")
    args = argparser.parse_args()
    problem_input = net.load(args.problem)
    app = QApplication(sys.argv)
    window = ICFPCPainter(problem_input)
    app.exec_()


if __name__ == "__main__":
    main()
