from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen
import sys


class ICFPCPainter(QWidget):
    POINT_RADIUS = 4
    WIDTH = 700
    HEIGHT = 700
    MARGIN = 50

    def __init__(self, hole, figure):
        super(QWidget, self).__init__()
        self.setGeometry(0, 0, ICFPCPainter.WIDTH, ICFPCPainter.HEIGHT)
        self.hole = hole
        self.figure = figure
        self.init_cds()
        self.show()

    def init_cds(self):
        xs = list(map(lambda x: x[0], self.hole + self.figure.vertices))
        ys = list(map(lambda x: x[1], self.hole + self.figure.vertices))
        self.min_x, self.max_x = min(xs), max(xs)
        self.min_y, self.max_y = min(ys), max(ys)

    def scale(self, x, y):
        mgn = ICFPCPainter.MARGIN
        nx = (x - self.min_x) / (self.max_x - self.min_x) * (ICFPCPainter.WIDTH - 2 * mgn) + mgn
        ny = (y - self.min_y) / (self.max_y - self.min_y) * (ICFPCPainter.HEIGHT - 2 * mgn) + mgn
        return nx, ny

    def paintEvent(self, e):
        self.qp = QPainter()
        self.qp.begin(self)
        self.draw_hole()
        self.draw_figure()
        self.qp.end()

    def draw_hole(self):
        self.qp.setPen(QPen(Qt.black, Qt.SolidLine))
        for i in range(len(self.hole)):
            self.draw_line(self.hole[i - 1], self.hole[i])

    def draw_figure(self):
        self.qp.setPen(QPen(Qt.red, Qt.SolidLine))
        self.qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        for v in self.figure.vertices:
            self.draw_point(v)
        for u, v in self.figure.edges:
            self.draw_line(self.figure.vertices[u], self.figure.vertices[v])

    def draw_point(self, point):
        r = ICFPCPainter.POINT_RADIUS
        self.qp.drawEllipse(QPoint(*self.scale(*point)), r, r)

    def draw_line(self, a, b):
        self.qp.drawLine(QPoint(*self.scale(*a)), QPoint(*self.scale(*b)))


class Figure:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges


def main():
    app = QApplication(sys.argv)
    hole = [[55, 80], [65, 95], [95, 95], [35, 5], [5, 5],
            [35, 50], [5, 95], [35, 95], [45, 80]]
    figure = Figure(
        [
            [20, 30], [20, 40], [30, 95], [40, 15], [40, 35], [40, 65],
            [40, 95], [45, 5], [45, 25], [50, 15], [50, 70], [55, 5],
            [55, 25], [60, 15], [60, 35], [60, 65], [60, 95], [70, 95],
            [80, 30], [80, 40]
        ],
        [
            [2, 5], [5, 4], [4, 1], [1, 0], [0, 8], [8, 3], [3, 7],
            [7, 11], [11, 13], [13, 12], [12, 18], [18, 19], [19, 14],
            [14, 15], [15, 17], [17, 16], [16, 10], [10, 6], [6, 2],
            [8, 12], [7, 9], [9, 3], [8, 9], [9, 12], [13, 9], [9, 11],
            [4, 8], [12, 14], [5, 10], [10, 15]
        ]
    )
    window = ICFPCPainter(hole, figure)
    app.exec_()


if __name__ == "__main__":
    main()