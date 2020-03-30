from primitives import Node, Edge
import pygame as pg
import numpy as np

### BEGIN SQUARE
n0 = Node([0, 0, 0, 1])
n1 = Node([50, 0, 0, 1])
n2 = Node([50, 50, 0, 1])
n3 = Node([0, 50, 0, 1])

e0_1 = Edge(n0, n1)
e1_2 = Edge(n1, n2)
e2_3 = Edge(n2, n3)
e3_0 = Edge(n3, n0)

n4 = Node([0, 0, 50, 1])
n5 = Node([50, 0, 50, 1])
n6 = Node([50, 50, 50, 1])
n7 = Node([0, 50, 50, 1])

e4_5 = Edge(n4, n5)
e5_6 = Edge(n5, n6)
e6_7 = Edge(n6, n7)
e7_4 = Edge(n7, n4)

e0_4 = Edge(n0, n4)
e1_5 = Edge(n1, n5)
e2_6 = Edge(n2, n6)
e3_7 = Edge(n3, n7)

edges = [e0_1, e1_2, e2_3, e3_0, e4_5, e5_6, e6_7, e7_4, e0_4, e1_5, e2_6, e3_7]
nodes = [n0, n1, n2, n3, n4, n5, n6, n7]
### END SQUARE

dimensions = (width, height) = (600, 600)
# matrix multiplication
canonical_to_pixel = np.array(
    [
        [width / 2, 0, 0, (width - 1) / 2],
        [0, -height / 2, 0, (height - 1) / 2],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)

print("Canonical")
print(canonical_to_pixel)
print()
### orthographic view volume
l = -100
r = 100

b = -100
t = 100
n = 100
f = -100
model = np.array(
    [
        [2 / (r - l), 0, 0, 0],
        [0, 2 / (t - b), 0, 0],
        [0, 0, 2 / (n - f), 0],
        [0, 0, 0, 1],
    ]
) @ np.array(
    [
        [1, 0, 0, -(l + r) / 2],
        [0, 1, 0, -(b + t) / 2],
        [0, 0, 1, -(n + f) / 2],
        [0, 0, 0, 1],
    ]
)

print("Model")
print(model)
print()
###
eye_position = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
print("Eye position")
print(eye_position)
print()
##
object_matrix = canonical_to_pixel @ model
print("Object matrix")
print(object_matrix)
print()
print("Canonical")
print(canonical_to_pixel)
print()

###
def multi(x):
    return x


gen = list(map(multi, nodes))
# print("GEN")
# print(gen)
# print("nodes")
# print(nodes)
screen = pg.display.set_mode(dimensions)
for edge in edges:
    begin = object_matrix @ edge.begin.coordinates
    end = object_matrix @ edge.end.coordinates
    pg.draw.aaline(screen, 255, begin[:2], end[:2], 0)
    # print(edge)
    print(f"begin = {begin} end ={end}")

pg.display.flip()


running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
