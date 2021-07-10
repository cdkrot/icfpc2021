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
        self.is_pinned = [False for x in self.figure.vertices]
        self.dragging = False
        self.init_cds()
        self.show()

    def init_cds(self):
        xs = list(map(lambda x: x.x, self.hole.vertices + self.figure.vertices.vertices))
        ys = list(map(lambda x: x.y, self.hole.vertices + self.figure.vertices.vertices))
        self.center = 0.5 * Vec(min(xs) + max(xs), min(ys) + max(ys))
        self.scale_factor = max(max(xs) - min(xs), max(ys) - min(ys)) * 1.5
        self.user_scale = 1.0

    def scale(self, p):
        transformed = (self.user_scale / self.scale_factor) * (p - self.center) + Vec(0.5, 0.5)
        return transformed.x * ICFPCPainter.HEIGHT, transformed.y * ICFPCPainter.HEIGHT

    def unscale(self, transformed):
        transformed = Vec(transformed[0], transformed[1])
        transformed = (1 / ICFPCPainter.HEIGHT) * transformed
        transformed -= Vec(0.5, 0.5)
        transformed *= self.scale_factor / self.user_scale

        return transformed + self.center

    def paintEvent(self, e):
        self.draw_input()

    def draw_input(self):
        self.qp = QPainter()
        self.qp.begin(self)
        self.draw_hole()
        self.draw_figure()
        self.qp.end()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_S:
            try:
                rounded = VerticesList([Vec(round(p.x), round(p.y)) for p in self.figure.vertices])
                net.check_and_submit(self.input, rounded)
            except Exception as ex:
                print(ex)
        elif e.key() == Qt.Key_I:
            rounded = VerticesList([Vec(round(p.x), round(p.y)) for p in self.figure.vertices])
            self.figure.vertices = rounded
            self.update()
        elif e.key() == Qt.Key_P:
            state = self.figure.vertices

            for go in [0.1, 0.05, 0.001]:
                physics = Physics(go, self.is_pinned)
                for steps in range(int(1e3)):
                    state = physics.apply(self.input, state)
                    self.figure.vertices = state
                    self.update()
        elif e.key() == Qt.Key_Plus:
            self.user_scale *= 1.1
            self.update()
        elif e.key() == Qt.Key_Minus:
            self.user_scale /= 1.1
            self.update()
        elif e.key() == Qt.Key_Left:
            self.center.x -= (ICFPCPainter.HEIGHT / 40) / self.user_scale
            self.update()
        elif e.key() == Qt.Key_Right:
            self.center.x += (ICFPCPainter.HEIGHT / 40) / self.user_scale
            self.update()
        elif e.key() == Qt.Key_Up:
            self.center.y -= (ICFPCPainter.HEIGHT / 40) / self.user_scale
            self.update()
        elif e.key() == Qt.Key_Down:
            self.center.y += (ICFPCPainter.HEIGHT / 40) / self.user_scale
            self.update()
        else:
            self.figure.vertices = Physics(is_pinned=self.is_pinned).apply(self.input, self.figure.vertices)
            self.update()

    def draw_hole(self):
        self.qp.setPen(QPen(Qt.black, Qt.SolidLine))
        for i in range(len(self.hole.vertices)):
            self.draw_line(self.hole.vertices[i - 1], self.hole.vertices[i])

    def draw_figure(self):
        from fractions import Fraction

        for u, v in self.figure.edges:
            new_d = self.figure.vertices.vertices[u] - self.figure.vertices.vertices[v]
            old_d = self.input.figure.vertices.vertices[u] - self.input.figure.vertices.vertices[v]
            correct_coef = Fraction(self.input.epsilon / 10 ** 6)
            coef = Fraction((new_d.x * new_d.x + new_d.y * new_d.y) / (old_d.x * old_d.x + old_d.y * old_d.y) - 1)
            if abs(coef) > correct_coef:
                if (coef > 0):
                    pen = QPen(Qt.blue, Qt.SolidLine)
                else:
                    pen = QPen(Qt.red, Qt.SolidLine)
            else:
                pen = QPen(Qt.darkGreen, Qt.SolidLine)

            pen.setWidth(3)
            self.qp.setPen(pen)
            self.draw_line(self.figure.vertices.vertices[u], self.figure.vertices.vertices[v])

        self.qp.setPen(QPen(Qt.green, Qt.SolidLine))
        for (pin, v) in zip(self.is_pinned, self.figure.vertices.vertices):
            if pin:
                self.qp.setBrush(QBrush(Qt.darkRed, Qt.SolidPattern))
            else:
                self.qp.setBrush(QBrush(Qt.darkGreen, Qt.SolidPattern))
            self.draw_point(v)

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
        
        if mndist > ICFPCPainter.DRAG_THRESHOLD:
            return

        if e.buttons() & Qt.RightButton:
            self.is_pinned[mndist_id] = not self.is_pinned[mndist_id]
            self.update()
        else:
            if not self.is_pinned[mndist_id]:
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
