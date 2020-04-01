from primitives import Node, Edge
from data import init
import pygame as pg
import numpy as np


TRANSLATION_STEP = 10
ROTATION_STEP = np.pi / 12

EDGES = init() 
# nodes = [n0, n1, n2, n3, n4, n5, n6, n7]
### END SQUARE

dimensions = (width, height) = (600, 600)
# matrix multiplication
canonical_to_pixel = np.array(
    [
        [-width / 2, 0, 0, (width - 1) / 2],
        [0, height / 2, 0, (height - 1) / 2],
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
### Eve
position = np.array([0, 0, 150])
gaze = np.array([0, 0, -1])
view_up = np.array([0, 1, 0])
w = -1 * gaze / np.linalg.norm(gaze)
cross = np.cross(view_up, w)
u = cross / np.linalg.norm(cross)
v = np.cross(w, u)
eye_rotation = np.identity(4)
eye_rotation[0, :-1] = u
eye_rotation[1, :-1] = v
eye_rotation[2, :-1] = w
eye_transform = np.identity(4)
eye_transform[:-1, -1] = -position

##
view_matrix = eye_rotation @ eye_transform

print("view_matrix")
print(view_matrix)
print()
###
projection_matrix = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, (n + f) / n, -f], [0, 0, 1 / n, 0],]
)

###
object_matrix = canonical_to_pixel @ model
print("Object matrix")
print(object_matrix)
print()
print("Canonical")
print(canonical_to_pixel)
print()

###
# object_view_matrix = object_matrix @ view_matrix
camera = np.identity(4)

### Move to the left
screen = pg.display.set_mode(dimensions)
def draw(screen, object_m, projection, camera, view, edges):
    matrix_o_p_v = object_m @ projection @ np.linalg.inv(camera)  @ view
    screen.fill(0)
    # print("Camera")
    # print(camera)
    for edge in edges:
        begin = edge.begin.coordinates
        end = edge.end.coordinates
        # print(f"w_begin = {begin}, w_end = {end}")
        begin = matrix_o_p_v @ begin
        end = matrix_o_p_v @ end
        begin = begin / begin[-1]
        end = end / end[-1]
        if (begin[2] > 0 or end[2] > 0):
            continue
        # print(f"begin = {begin}, end = {end}")
        pg.draw.circle(screen, (255, 0, 0), begin[:2].astype(int), 3)
        # pg.draw.circle(screen, (255,0,0), end[:2].astype(int),3)
        pg.draw.aaline(screen, (255,255,255), begin[:2], end[:2], 0)
        # print(edge)
        # print(f"begin = {begin} end ={end}")
    pg.draw.circle(screen, (255, 0, 0), (width//2, height//2), 10, 1)
    pg.display.flip()

draw(screen, object_matrix, projection_matrix, camera, view_matrix, EDGES)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
        if event.type == pg.KEYDOWN:
            shift = np.identity(4)
            if event.key == pg.K_w and pg.key.get_mods() & pg.KMOD_CTRL:
                print('w + CTRL')
                shift[1:3,1:3] = np.array([
                    [np.cos(ROTATION_STEP), -np.sin(ROTATION_STEP)],
                    [np.sin(ROTATION_STEP), np.cos(ROTATION_STEP)]
                ])
                camera = camera @ shift
            elif event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
                print('s + CTRL')
                shift[1:3,1:3] = np.array([
                    [np.cos(ROTATION_STEP), -np.sin(ROTATION_STEP)],
                    [np.sin(ROTATION_STEP), np.cos(ROTATION_STEP)]
                ])
                shift = np.linalg.inv(shift)
                camera = camera @ shift
            elif event.key == pg.K_a and pg.key.get_mods() & pg.KMOD_CTRL:
                print('a + CTRL')
                shift[0:3,0:3] = np.array([
                    [np.cos(ROTATION_STEP),0, np.sin(ROTATION_STEP)],
                    [0,1, 0],
                    [-np.sin(ROTATION_STEP),0,np.cos(ROTATION_STEP)]
                ])
                camera = camera @ shift
            elif event.key == pg.K_d and pg.key.get_mods() & pg.KMOD_CTRL:
                print('d + CTRL')
                shift[0:3,0:3] = np.array([
                    [np.cos(ROTATION_STEP),0, np.sin(ROTATION_STEP)],
                    [0,1, 0],
                    [-np.sin(ROTATION_STEP),0,np.cos(ROTATION_STEP)]
                ])
                shift = np.linalg.inv(shift)
                camera = camera @ shift
            elif event.key == pg.K_w and pg.key.get_mods() & pg.KMOD_SHIFT:
                print('w + shift')
                shift[:-1,3] = TRANSLATION_STEP * np.array([0,0,-1]);
                # camera = shift @ camera
                camera = camera @ shift
            elif event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_SHIFT:
                print('s + shift')
                shift[:-1,3] = TRANSLATION_STEP * np.array([0,0,1]);
                # camera = shift @ camera
                camera = camera @ shift
            elif event.key == pg.K_w:
                print("w")
                shift[:-1,3] = TRANSLATION_STEP * np.array([0,1,0]);
                # camera = shift @ camera
                camera = camera @ shift
            elif event.key == pg.K_s:
                print('s')
                shift[:-1,3] = TRANSLATION_STEP * np.array([0,-1,0]);
                # camera = shift @ camera
                camera = camera @ shift
            elif event.key == pg.K_a:
                print('a')
                shift[:-1,3] = TRANSLATION_STEP * np.array([-1,0,0]);
                # camera = shift @ camera
                camera = camera @ shift
            elif event.key == pg.K_d:
                print('d')
                shift[:-1,3] = TRANSLATION_STEP * np.array([1,0,0]);
                # camera = shift @ camera
                camera = camera @ shift
            elif event.key == pg.K_q:
                print('q')
                shift[0:2,0:2] = np.array([
                    [np.cos(ROTATION_STEP), -np.sin(ROTATION_STEP)],
                    [np.sin(ROTATION_STEP), np.cos(ROTATION_STEP)]
                ])
                camera = camera @ shift
            elif event.key == pg.K_e:
                print('e')
                shift[0:2,0:2] = np.array([
                    [np.cos(ROTATION_STEP), -np.sin(ROTATION_STEP)],
                    [np.sin(ROTATION_STEP), np.cos(ROTATION_STEP)]
                ])
                shift = np.linalg.inv(shift)
                camera = camera @ shift
            print(camera)
            draw(screen, object_matrix, projection_matrix, camera, view_matrix, EDGES)
