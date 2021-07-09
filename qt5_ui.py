from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen

import argparse
import sys
import net

from structures import *
from physics import Physics

class ICFPCPainter(QWidget):
    POINT_RADIUS = 4
    WIDTH = 700
    HEIGHT = 700
    MARGIN = 50
    DRAG_THRESHOLD = 9

    def __init__(self, input):
        super(QWidget, self).__init__()
        self.setGeometry(0, 0, ICFPCPainter.WIDTH, ICFPCPainter.HEIGHT)
        self.hole = input.hole
        self.input = input
        self.figure = copy.deepcopy(input.figure)
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

    def keyPressEvent(self, e):
        self.figure = Figure(Physics().apply(self.input, self.figure.vertices), self.input.figure.edges)
        self.update()

    def draw_hole(self):
        self.qp.setPen(QPen(Qt.black, Qt.SolidLine))
        for i in range(len(self.hole.vertices)):
            self.draw_line(self.hole.vertices[i - 1], self.hole.vertices[i])

    def draw_figure(self):
        self.qp.setPen(QPen(Qt.green, Qt.SolidLine))
        self.qp.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        for v in self.figure.vertices.vertices:
            self.draw_point(v)

        for u, v in self.figure.edges:
            new_d = self.figure.vertices.vertices[u] - self.figure.vertices.vertices[v]
            old_d = self.input.figure.vertices.vertices[u] - self.input.figure.vertices.vertices[v]
            coef = (self.input.epsilon / 10**6)
            if abs((new_d.x * new_d.x + new_d.y * new_d.y) /
                   (old_d.x * old_d.x + old_d.y * old_d.y) - 1) > coef:
                self.qp.setPen(QPen(Qt.red, Qt.SolidLine))

            self.draw_line(self.figure.vertices.vertices[u], self.figure.vertices.vertices[v])
            self.qp.setPen(QPen(Qt.green, Qt.SolidLine))
    def draw_point(self, point):
        r = ICFPCPainter.POINT_RADIUS
        self.qp.drawEllipse(QPoint(*self.scale(point)), r, r)

    def draw_line(self, a, b):
        self.qp.drawLine(QPoint(*self.scale(a)), QPoint(*self.scale(b)))

    def mousePressEvent(self, e):
        self.dragging = None
        pos = self.unscale((e.pos().x(), e.pos().y()))
        mndist_id = 0
        mndist = 1e18
        for i in range(len(self.figure.vertices.vertices)):
            new_mndist = (self.figure.vertices.vertices[i] - pos).len2()
            if new_mndist < mndist:
                mndist = new_mndist
                mndist_id = i
        if mndist <= ICFPCPainter.DRAG_THRESHOLD:
            self.dragging = mndist_id

    def mouseMoveEvent(self, e):
        if self.dragging is not None:
            self.figure.vertices.vertices[self.dragging] = self.unscale((e.pos().x(), e.pos().y()))
            self.update()

    def mouseReleaseEvent(self, e):
        self.dragging = None


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
