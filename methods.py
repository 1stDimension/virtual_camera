from primitives import Node, Edge
from data import init
from config import WIDTH, HEIGHT
import pygame as pg
import numpy as np


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def normal(triangle):
    # nodes = triangle.nodes()
    edgeOne = triangle.two.coordinates[:3] - triangle.one.coordinates[:3]
    edgeTwo = triangle.tree.coordinates[:3] - triangle.one.coordinates[:3]
    # posible place of error
    return normalize(np.cross(edgeOne, edgeTwo))


def d_of_plane_equation(triangle):
    return -1 * normal(triangle) @ triangle.one.coordinates[:3]


def implicit_plane_function(point, triangle):
    n = normal(triangle)
    # Possible errors
    return n @ (point - triangle.one.coordinates[:3])


def homogenize(vector):
    return vector / vector[-1]


def draw_triangle(screen, matrix, triangle):
    current_triangle_nodes = triangle.nodes()
    screen_cordinates = list(
        map(lambda x: homogenize(matrix @ x.coordinates), current_triangle_nodes,)
    )
    colour = triangle.colour
    # wrong should be if outside of canonical volume
    if (
        screen_cordinates[0][2] > 0
        or screen_cordinates[1][[2]] > 0
        or screen_cordinates[2][2] > 0
    ):
        return
    coordinates = list(map(lambda x: x[:2], screen_cordinates))
    pg.draw.polygon(screen, colour, coordinates, 0)
    pg.draw.polygon(screen, (255, 255, 255), coordinates, 1)


def draw(screen, object_m, projection, camera, view, nodes, triangles, tree):
    matrix_o_p_v = object_m @ projection @ np.linalg.inv(camera) @ view
    screen.fill(0)
    # print("Camera")
    # print(camera)
    # for node in nodes:
    # print(f"w_begin = {begin}, w_end = {end}")
    # coordinates = node.coordinates
    # coordinates = homogenize(matrix_o_p_v @ coordinates)
    # if begin[2] > 0 or end[2] > 0:
    # continue

    print(camera)
    # eye_position = camera[:3, -1]
    eye_position = np.array([0, 0, 150])
    print(f"eye_position = {eye_position}")

    tree.draw(eye_position, matrix_o_p_v, screen)
    # for triangle in triangles:
    # draw_triangle(screen, matrix_o_p_v, triangle)
    # print(f"begin = {begin}, end = {end}")
    # pg.draw.circle(screen, (255, 0, 0), begin[:2].astype(int), 3)
    # pg.draw.circle(screen, (255,0,0), end[:2].astype(int),3)
    # pg.draw.aaline(screen, (255, 255, 255), begin[:2], end[:2], 0)
    # print(edge)
    # print(f"begin = {begin} end ={end}")
    pg.draw.circle(screen, (255, 0, 0), (WIDTH // 2, HEIGHT // 2), 10, 1)
    pg.display.flip()


def close_on_exit(event):
    if event.type == pg.QUIT:
        raise Exception
        pg.quit()
