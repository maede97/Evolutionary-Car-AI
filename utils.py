import numpy as np
import os
import pygame
import configparser
import math

config = configparser.ConfigParser()
config.read('config.ini')

# Read all configurations
CARS_PER_GEN = config.getint("General", "CARS_PER_GEN", fallback=32)
MAX_ITERATIONS = config.getint("General", "MAX_ITERATIONS", fallback=100)
AUTO_SAVE_BEST_GENOME = config.getboolean("General", "AUTO_SAVE_BEST_GENOME_EVERY_GEN", fallback=True)
AUTO_SAVE_FILENAME = config.get("General", "AUTO_SAVE_FILEPATH", fallback="all_time.txt")
RACETRACK = config.get("General", "RACETRACK", fallback="racemap.png")

SIZE = config.getint("Display", "SIZE_X", fallback=800), config.getint("Display", "SIZE_Y", fallback=600)

CAR_WIDTH = config.getint("Car", "CAR_WIDTH", fallback=6)
CAR_LENGTH = config.getint("Car", "CAR_HEIGHT", fallback=12)
MAX_DIST = config.getint("Car", "MAX_DIST", fallback=100)
MAX_TURN_VELOCITY = config.getfloat("Car", "MAX_TURN_VELOCITY", fallback=5.0)

CROSS_OVER_PROB = config.getfloat("Brain", "CROSS_OVER_PROB", fallback=0.2)
MUTATION_PROB = config.getfloat("Brain", "MUTATION_PROB", fallback=0.5)

DEMO_BRAIN = config.get("Demo", "BRAIN_TO_LOAD", fallback="")
DEMO_RACETRACK = config.get("Demo", "RACETRACK", fallback="racemap.png")

DRAW_RACETRACK = config.get("Draw", "RACETRACK", fallback="racemap.png")

# Color definitions
COL_BLACK = pygame.color.Color(0,0,0)
COL_RED = pygame.color.Color(255,0,0)
COL_GREEN = pygame.color.Color(0,255,0)
COL_BLUE = pygame.color.Color(0,0,255)
COL_WHITE = pygame.color.Color(255,255,255)

def save_genome(filename, genome):
    np.savetxt(os.path.join(os.path.dirname(os.path.abspath(__file__)),filename), genome)

def load_genome(filename):
    return np.loadtxt(os.path.join(os.path.dirname(os.path.abspath(__file__)),filename))

def loadBackgroundImage(demo=False):
    if demo:
        map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DEMO_RACETRACK)
    else:
        map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), RACETRACK)
    image = pygame.image.load(map_path)

    start_point = None
    direction_point = None

    found = 0

    for x in range(SIZE[0]):
        if found == 2:
                break
        for y in range(SIZE[1]):
            if found == 2:
                break
            if image.get_at((x,y)) == COL_GREEN:
                start_point = (x,y)
                found += 1
            elif image.get_at((x,y)) == COL_BLUE:
                direction_point = (x,y)
                found += 1
    # Compute direction as an angle from the two points
    dy = direction_point[1] - start_point[1]
    dx = direction_point[0] - start_point[0]
    if dx == 0:
        direction = 90
    else:
        direction = -int(math.degrees(math.atan(-dy/dx)))
    direction += 90

    # set pixels back to white
    image.set_at(start_point, COL_WHITE)
    image.set_at(direction_point, COL_WHITE)

    return image, start_point, direction

if __name__ == "__main__":
    print("Do not run this directly.")