import numpy as np
from primitives import Triangle
from methods import draw_triangle, implicit_plane_function


class BSPTree(object):
    def __init__(self):
        self.minus: BSPTree = None
        self.plus: BSPTree = None
        self.this: Triangle = None

    def draw(self, eye):
        if self.empty():
            return
        p = implicit_plane_function(eye, self.this)
        if p < 0:
            print(f"p < 0; p = {p}")
            self.plus.draw(eye)
            ## rasterize ?
            self.minus.draw(eye)
        else:
            print(f"p > 0; p = {p}")
            self.minus.draw(eye)
            ## rasterize ?
            self.plus.draw(eye)

    def add(self, Triangle):
        print("Adding triangle")

    def empty(self):
        return self.this is None
