from brain import Model
import utils
import math
import pygame
import numpy as np

class Car:
    def __init__(self, position, angle, raceTrack):
        self.surface = pygame.Surface((utils.CAR_WIDTH, utils.CAR_LENGTH))
        self.surface.fill(utils.COL_RED)
        self.surface.set_colorkey(utils.COL_BLACK)
        self.surface.set_alpha(120)

        self.raceTrack = raceTrack

        # create the model (random init)
        self.model = Model()

        self.reset(position, angle)

    def setGreen(self):
        self.surface.fill(utils.COL_GREEN)
        self.surface.set_alpha(255)

    def setRed(self):
        self.surface.fill(utils.COL_RED)
        self.surface.set_alpha(120)

    def reset(self, position, angle):
        self.position = [position[0], position[1]]
        self.angle = -angle + 180.0
        self.velocity = 1.0
        self.angle_velocity = 0.0
        self.crashed = False
        self.fitness = 0
        self.setRed()

    def check_collision(self):
        # check both front corners for a black pixel below them
        # if any of them has one, this car is crashed
        dx = math.sin(self.angle) * utils.CAR_WIDTH // 2
        dy = math.cos(self.angle) * utils.CAR_LENGTH // 2
        frontLeft = int(self.position[0] - dx), int(self.position[1] - dy)
        frontRight = int(self.position[0] + dx), int(self.position[1] - dy)

        if (frontLeft[0] < 0 or
            frontLeft[0] > utils.SIZE[0] or
            frontLeft[1] < 0 or
            frontLeft[1] > utils.SIZE[1] or
            frontRight[0] < 0 or
            frontRight[0] > utils.SIZE[0] or
            frontRight[1] < 0 or
            frontRight[1] > utils.SIZE[1] or
            self.raceTrack.get_at(frontLeft) == utils.COL_BLACK or
            self.raceTrack.get_at(frontRight) == utils.COL_BLACK):
            self.crashed = True

    def get_distance_in_direction(self, angle):
        # angle is relative to self.angle
        # retuns MAX_DIST if not wall is found closer
        for i in range(utils.MAX_DIST):
            x = self.position[0] + float(i) * math.sin(math.radians(-angle + self.angle))
            y = self.position[1] + float(i) * math.cos(math.radians(-angle + self.angle))

            if int(x) < 0 or int(x) >= utils.SIZE[0] or int(y) < 0 or int(y) >= utils.SIZE[1]:
                return float(i) / utils.MAX_DIST # return wall at this point
            if self.raceTrack.get_at((int(x), int(y))) == utils.COL_BLACK:
                return float(i) / utils.MAX_DIST
        return 1.0 # return MAX_DIST / MAX_DIST

    def compute_input_vector(self):
        # returns a vector of 5 values:
        # the distance to the next wall for 5 directions:
        # left, frontLeft, front, frontRight, right
        # if no wall is found, return MAX_DIST
        ret = np.zeros((1,5), dtype=float)
        ret[0,:] = self.get_distance_in_direction(-90), self.get_distance_in_direction(-45), self.get_distance_in_direction(0), self.get_distance_in_direction(45), self.get_distance_in_direction(90)
        return ret
    
    def perform_autonomous_action(self):
        action = self.model.predict(self.compute_input_vector())

        # first control controls speed
        self.velocity = action[0, 0]
        # second action controls angle velocity
        self.angle_velocity = (action[1, 0] - 0.5) * utils.MAX_TURN_VELOCITY
        #if abs(self.angle_velocity) > 10.0:
        #    self.angle_velocity = self.angle_velocity / abs(self.angle_velocity) * 10.0

    def update(self):
        # Update position
        self.check_collision()

        if not self.crashed:
            self.angle -= self.angle_velocity
            self.angle = self.angle % 360

            self.position[0] += self.velocity * math.sin(math.radians(self.angle))
            self.position[1] += self.velocity * math.cos(math.radians(self.angle))

        # Update surface (because of color change)
        self.draw_surface = pygame.transform.rotate(self.surface, self.angle)
        self.rect = self.draw_surface.get_rect()
        self.rect.center = (int(self.position[0]), int(self.position[1]))
        
    def draw(self, window, drawLines=False):
        window.blit(self.draw_surface, self.rect)
        if drawLines:
            inp = self.compute_input_vector()
            for i,angle in enumerate([-90, -45, 0, 45, 90]):
                xp = self.position[0] +inp[0,i] * utils.MAX_DIST * math.sin(math.radians(-angle + self.angle))
                yp = self.position[1] + inp[0,i] * utils.MAX_DIST * math.cos(math.radians(-angle + self.angle))
                pygame.draw.line(window, utils.COL_BLUE, self.position, (int(xp),int(yp)))            

if __name__ == "__main__":
    print("Do not run this directly.")