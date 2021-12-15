import pygame
import numpy as np
from math import *

# GLOBALS


# COLORS


# SCREEN SETUP
pygame.init()
WIDTH, HEIGHT = 800, 800
root = pygame.display.set_mode((WIDTH, HEIGHT))
# icon = pygame.image.load( ICON PATH HERE )
# pygame.display.set_icon(icon)
TITLE = "Orthographic Projection"
pygame.display.set_caption(TITLE)
FPS = 30

# MUSIC
# audio = pygame.mixer.music.load( MP3 PATH HERE )
# pygame.mixer.music.play(loops=-1)
# pygame.mixer.music.set_volume(0.1)

# OBJECTS
points = [
    np.matrix([-1, -1, 1]).reshape(3, 1),
    np.matrix([1, -1, 1]).reshape(3, 1),
    np.matrix([1, -1, -1]).reshape(3, 1),
    np.matrix([-1, -1, -1]).reshape(3, 1),
    np.matrix([-1, 1, 1]).reshape(3, 1),
    np.matrix([1, 1, 1]).reshape(3, 1),
    np.matrix([1, 1, -1]).reshape(3, 1),
    np.matrix([-1, 1, -1]).reshape(3, 1),
]

angle = 0

projected_points = [[] for _ in points]


def rotation(point, angle, type="x"):
    if type == "x":
        Rx = np.matrix(
            [
                [1, 0, 0],
                [0, cos(angle), -sin(angle)],
                [0, sin(angle), cos(angle)],
            ]
        )
        return np.dot(Rx, point)
    elif type == "y":
        Ry = np.matrix(
            [
                [cos(angle), 0, sin(angle)],
                [0, 1, 0],
                [-sin(angle), 0, cos(angle)],
            ]
        )
        return np.dot(Ry, point)
    elif type == "z":
        Rz = np.matrix(
            [
                [cos(angle), -sin(angle), 0],
                [sin(angle), cos(angle), 0],
                [0, 0, 1],
            ]
        )
        return np.dot(Rz, point)


def projection(point):
    P = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
    return np.dot(P, point)


def pointConnector(i, j, point_list):
    pygame.draw.line(root, "white", (point_list[i]), (point_list[j]), width=1)


# ANIMATIONS
def draw():
    global angle

    root.fill("black")

    for index, point in enumerate(points):
        rotatedY = rotation(point, angle, "y")
        rotatedX = rotation(rotatedY, 60, "x")
        projected = projection(rotatedX)
        x = int(projected[0] * 200) + WIDTH // 2
        y = int(projected[1] * 200) + HEIGHT // 2

        projected_points[index] = [x, y]
        pygame.draw.circle(root, "white", (x, y), 1)

    for i in range(4):
        pointConnector(i, (i + 1) % 4, projected_points)
        pointConnector(i + 4, (i + 1) % 4 + 4, projected_points)
        pointConnector(i, i + 4, projected_points)

    angle += 0.05

    pygame.display.update()


# MAIN LOOP
def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
            ):
                running = False

        draw()


if __name__ == "__main__":
    main()
    pygame.quit()
