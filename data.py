from primitives import *
import copy
import numpy as np


def move_z_triangle(x: Triangle):
    for node in x.nodes:
        move_z(node)
    return x


def flip_x_triangle(x: Triangle):
    for node in x.nodes:
        flip_x(node)
    return x


def move_z(x):
    tmp = np.identity(4)
    tmp[:-1, -1] = np.array([0, 0, -80])
    x.coordinates = tmp @ x.coordinates
    return x


def flip_x(x):
    tmp = np.identity(4)
    tmp[0, 0] = -1
    x.coordinates = tmp @ x.coordinates
    return x


def init() -> List[Type[Node]]:
    ### BEGIN SQUARE

    n0 = Node([10, -25, 50, 1])
    n1 = Node([50, -25, 50, 1])
    n2 = Node([50, 25, 50, 1])
    n3 = Node([10, 25, 50, 1])

    n4 = Node([10, -25, 75, 1])
    n5 = Node([50, -25, 75, 1])
    n6 = Node([50, 25, 75, 1])
    n7 = Node([10, 25, 75, 1])

    # Front plane of square first
    t0 = Triangle(n0, n1, n2)
    t1 = Triangle(n2, n3, n0)

    # Back plane of square second
    t2 = Triangle(n4, n5, n6)
    t3 = Triangle(n6, n7, n4)

    # Top plane

    t4 = Triangle(n3, n2, n6)
    t5 = Triangle(n6, n7, n3)

    # Bottom plane

    t6 = Triangle(n0, n1, n5)
    t7 = Triangle(n5, n2, n0)

    # Left plane
    t8 = Triangle(n0, n4, n7)
    t9 = Triangle(n7, n3, n0)

    # right plane

    t10 = Triangle(n1, n5, n6)
    t11 = Triangle(n6, n2, n1)

    right_first_building = [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11]

    right_second_building: list = copy.deepcopy(right_first_building)
    list(map(move_z_triangle, right_second_building))
    left_second_building = copy.deepcopy(right_second_building)

    list(map(flip_x_triangle, left_second_building))
    left_first_building = copy.deepcopy(right_first_building)
    list(map(flip_x_triangle, left_first_building))

    r0 = Node([5, -25, 75, 1])
    r1 = Node([5, -25, -75, 1])
    r2 = Node([-5, -25, -75, 1])
    r3 = Node([-5, -25, 75, 1])

    triangleRoad0 = Triangle(r0, r1, r2)
    triangleRoad1 = Triangle(r2, r3, r0)

    road = [triangleRoad0, triangleRoad1]
    # return nodes and triangles

    triangles = []
    all_nodes = []
    triangles.extend(right_first_building)
    triangles.extend(right_second_building)
    triangles.extend(left_second_building)
    triangles.extend(left_first_building)
    triangles.extend(road)

    for triangle in triangles:
        all_nodes.extend(triangle.nodes)

    return all_nodes, triangles
