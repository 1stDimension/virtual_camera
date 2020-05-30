from primitives import Node, Edge
from data import init
from config import WIDTH, HEIGHT
import pygame as pg
import numpy as np


def homogenize(vector):
    return vector / vector[-1]


def drawTriangle(screen, object_m, projection, camera, view, edges):
    matrix_o_p_v = object_m @ projection @ np.linalg.inv(camera) @ view


def draw(screen, object_m, projection, camera, view, edges):
    matrix_o_p_v = object_m @ projection @ np.linalg.inv(camera) @ view
    screen.fill(0)
    # print("Camera")
    # print(camera)
    for edge in edges:
        begin = edge.begin.coordinates
        end = edge.end.coordinates
        # print(f"w_begin = {begin}, w_end = {end}")
        begin = matrix_o_p_v @ begin
        end = matrix_o_p_v @ end
        begin = homogenize(begin)
        end = homogenize(end)
        if begin[2] > 0 or end[2] > 0:
            continue
        # print(f"begin = {begin}, end = {end}")
        pg.draw.circle(screen, (255, 0, 0), begin[:2].astype(int), 3)
        # pg.draw.circle(screen, (255,0,0), end[:2].astype(int),3)
        pg.draw.aaline(screen, (255, 255, 255), begin[:2], end[:2], 0)
        # print(edge)
        # print(f"begin = {begin} end ={end}")
    pg.draw.circle(screen, (255, 0, 0), (WIDTH // 2, HEIGHT // 2), 10, 1)
    pg.display.flip()


def close_on_exit(event):
    if event.type == pg.QUIT:
        running = False
        pg.quit()
