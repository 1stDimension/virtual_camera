import numpy as np
from primitives import Triangle, Node
from methods import draw_triangle, implicit_plane_function, normal, d_of_plane_equation


def compute_A(a, c, triangle):
    D = d_of_plane_equation(triangle)
    n = normal(triangle)
    if n @ (c - a) == 0:
        print(f"c = {c}, a = {a}")
        print(f"c - a = {c - a}")
        print(f"n = {n}")
    t = -(n @ a + D) / (n @ (c - a))
    A = a + t * (c - a)
    return A


class BSPTree(object):
    def __init__(self, triangle: Triangle):
        self.minus: BSPTree = None
        self.plus: BSPTree = None
        self.this: Triangle = triangle

    def draw(self, eye, matrix, screen):
        p = implicit_plane_function(eye, self.this)
        # print(f"eye = {eye}, p = {p}")
        if p < 0:
            # print(f"p < 0; p = {p}")
            if self.plus is not None:
                self.plus.draw(eye, matrix, screen)
            draw_triangle(screen, matrix, self.this)
            if self.minus is not None:
                self.minus.draw(eye, matrix, screen)
        else:
            # print(f"p > 0; p = {p}")
            if self.minus is not None:
                self.minus.draw(eye, matrix, screen)
            draw_triangle(screen, matrix, self.this)
            if self.plus is not None:
                self.plus.draw(eye, matrix, screen)

    def add(self, triangle: Triangle):
        nodes = triangle.nodes()
        a = nodes[0]  # .coordinates
        b = nodes[1]  # .coordinates
        c = nodes[2]  # .coordinates
        f_a = implicit_plane_function(a.coordinates[:3], self.this)
        f_b = implicit_plane_function(b.coordinates[:3], self.this)
        f_c = implicit_plane_function(c.coordinates[:3], self.this)
        if abs(f_a) < np.finfo(float).eps:
            f_a = 0
        if abs(f_b) < np.finfo(float).eps:
            f_b = 0
        if abs(f_c) < np.finfo(float).eps:
            f_c = 0
        if f_a <= 0 and f_b <= 0 and f_c <= 0:
            # print("eye before plain")
            if self.minus is None:
                self.minus = BSPTree(triangle)
            else:
                self.minus.add(triangle)
        elif f_a >= 0 and f_b >= 0 and f_c >= 0:
            # print("points behind plain")
            if self.plus is None:
                self.plus = BSPTree(triangle)
            else:
                self.plus.add(triangle)
        else:
            # cut triangles
            if f_a * f_c >= 0:
                f_b, f_c = f_c, f_b
                b, c = c, b
                f_a, f_b = f_b, f_a
                a, b = b, a
            elif f_b * f_c >= 0:
                f_a, f_c = f_c, f_a
                a, c = c, a
                f_a, f_b = f_b, f_a
                a, b = b, a
            # Compute A
            A = compute_A(a.coordinates[:3], c.coordinates[:3], self.this)
            A = np.append(A, 1)
            nodeA = Node(A)
            # Compute B
            B = compute_A(b.coordinates[:3], c.coordinates[:3], self.this)
            B = np.append(B, 1)
            nodeB = Node(B)
            T1 = Triangle(a, b, nodeA, colour=triangle.colour)
            T2 = Triangle(b, nodeB, nodeA, colour=triangle.colour)
            T3 = Triangle(nodeA, nodeB, c, colour=triangle.colour)
            if f_c >= 0:
                if self.minus is None:
                    self.minus = BSPTree(T1)
                else:
                    self.minus.add(T1)
                self.minus.add(T2)
                if self.plus is None:
                    self.plus = BSPTree(T3)
                else:
                    self.plus.add(T3)
            else:
                if self.plus is None:
                    self.plus = BSPTree(T1)
                else:
                    self.plus.add(T1)
                self.plus.add(T2)
                if self.minus is None:
                    self.minus = BSPTree(T3)
                else:
                    self.minus.add(T3)

    def empty(self):
        return self.this is None
