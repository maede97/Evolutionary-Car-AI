import os
import pygame
import numpy as np
import math

from . import utils

class Track:
    def __init__(self, filename):
        self.filename = filename

        self.image = None
        self.data = []

        self.thickness = utils.THICKNESS

    def set_data(self, data):
        self.data = data
    
    def set_thickness(self, thickness):
        self.thickness = thickness

    def set_image(self, image):
        self.image = image

    def add_point(self, x, y):
        # adds a point to the track
        if len(self.data) > 0:
            # prevent twice the same point
            if self.data[-1][0] == x and self.data[-1][1] == y:
                return
        self.data.append((x,y))

    def remove_point(self):
        if len(self.data) > 0:
            self.data.pop()

    def load(self):
        self.image = pygame.image.load(os.path.join(utils.TRACKS_PATH, self.filename + ".png"))
        self.data = np.loadtxt(os.path.join(utils.TRACKS_PATH, self.filename + ".txt"))

        # angle for first line
        if(len(self.data) < 2):
            print("Error: Track not valid.")
            quit(1)

        dx = self.data[1][0] - self.data[0][0]
        dy = self.data[1][1] - self.data[0][1]
        if dx == 0:
            self.init_angle = 180
        else:
            self.init_angle = -int(math.degrees(math.atan(-dy/dx))) + 90

    def get_start_info(self):
        if self.image:
            return self.data[0], self.init_angle
        else:
            print("Error: Not yet loaded")
            return None, None

    def save(self):
        pygame.image.save(self.image, os.path.join(utils.TRACKS_PATH, self.filename + ".png"))
        np.savetxt(os.path.join(utils.TRACKS_PATH, self.filename + ".txt"), self.data)

    def get_length(self):
        if len(self.data) > 2:
            return 0.0
        else:
            ret = 0.0
            sx,sy = self.data[0]
            for cx,cy in self.data[1:]:
                ret += math.sqrt((sx-cx)**2 + (sy-cy)**2)
                sx,sy = cx,cy
            return ret
                            
    def get_fitness(self, x, y):
        # calculates current distance to start of the track from the given position

        if self.data == []:
            print("Error: Data not set.")
            return 0.0

        # get closest point on track
        start_pos_line = self.data[0]

        score = 0.0

        # Iterate over all remaining line points
        for line_point in self.data[1:]:
            lineDir = line_point[0] - start_pos_line[0], line_point[1] - start_pos_line[1]
            line_length = math.sqrt(lineDir[0] ** 2 + lineDir[1] ** 2)
            lineDir = lineDir[0] / line_length, lineDir[1] / line_length

            v = x - start_pos_line[0], y - start_pos_line[1]
            d = v[0] * lineDir[0] + v[1] * lineDir[1]

            # clip d
            if d < 0:
                d = 0
            if d > line_length:
                d = line_length

            # point on line:
            pt = start_pos_line[0] + lineDir[0] * d, start_pos_line[1] + lineDir[1] * d

            dist = math.sqrt((x-pt[0]) ** 2 + (y-pt[1]) ** 2)
            if dist <= self.thickness:
                # we have found the closest line, calculate fitness and return:
                return score + d
            else:
                # add line length to score and keep going
                score += math.sqrt((line_point[0] - start_pos_line[0]) ** 2 + (line_point[1] - start_pos_line[1]) ** 2)
                start_pos_line = line_point[0], line_point[1]
        
        # no point on a line was found, return 0 (car was out of track)
        return 0.0