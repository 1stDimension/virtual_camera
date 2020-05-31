import numpy as np
from primitives import Triangle
from methods import draw_triangle, implicit_plane_function


class BSPTree(object):
    def __init__(self, triangle: Triangle):
        self.minus: BSPTree = None
        self.plus: BSPTree = None
        self.this: Triangle = triangle

    def draw(self, eye, matrix, screen):
        if self.empty():
            return
        p = implicit_plane_function(eye, self.this)
        if p < 0:
            print(f"p < 0; p = {p}")
            self.plus.draw(eye, matrix, screen)
            draw_triangle(screen, matrix, self.this)
            self.minus.draw(eye, matrix, screen)
        else:
            print(f"p > 0; p = {p}")
            self.minus.draw(eye, matrix, screen)
            draw_triangle(screen, matrix, self.this)
            self.plus.draw(eye, matrix, screen)

    def add(self, triangle: Triangle):
        nodes = triangle.nodes()
        f_a = implicit_plane_function(nodes[0].coordinates[:3], triangle)
        f_b = implicit_plane_function(nodes[1].coordinates[:3], triangle)
        f_c = implicit_plane_function(nodes[2].coordinates[:3], triangle)
        if abs(f_a) < np.finfo(float).eps:
            f_a = 0
        if abs(f_b) < np.finfo(float).eps:
            f_b = 0
        if abs(f_c) < np.finfo(float).eps:
            f_c = 0
        if f_a <= 0 and f_b <= 0 and f_c <= 0:
            print("eye before plain")
            if self.minus is None:
                self.minus = BSPTree(triangle)
            else:
                self.minus.add(triangle)
        elif f_a >= 0 and f_b >= 0 and f_c >= 0:
            print("points behind plain")
            if self.plus is None:
                self.plus = BSPTree(triangle)
            else:
                self.plus.add(triangle)
        else:
            # cut triangles
            print("plains intersect")

    def empty(self):
        return self.this is None
