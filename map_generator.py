import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import utils

if __name__ == "__main__":
    pygame.init()

    window = pygame.display.set_mode(utils.SIZE)
    pygame.display.set_caption("Draw map")

    objects = []

    finish = False

    radius = 15

    start_pos = None
    direction = None

    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    finish = True
                elif event.key == ord('s'):
                    pygame.image.save(window, os.path.join(os.path.dirname(os.path.abspath(__file__)), utils.DRAW_RACETRACK))
        if pygame.mouse.get_pressed()[0]:
            # draw white line on black screen
            cx,cy = pygame.mouse.get_pos()
            objects.append((cx,cy,radius))
            if len(objects) == 1:
                # set start position
                start_pos = (cx,cy)
            if direction == None and abs(start_pos[0] - cx) ** 2 + abs(start_pos[1] - cy) ** 2 > 5:
                direction = cx,cy

        if pygame.mouse.get_pressed()[2]:
            # Pop objects from white buffer
            if len(objects) == 0:
                pass
            else:
                objects.pop()
                # remove start position as well
                if len(objects) == 0:
                    start_pos = None
                if len(objects) == 99:
                    direction = None

        window.fill((0,0,0))

        for cx, cy, dim in objects:
            pygame.draw.circle(window, utils.COL_WHITE, (cx,cy), dim)

        if start_pos == None:
            pass
        else:
            # draw a green circle, start position
            window.set_at(start_pos, utils.COL_GREEN)
        if direction == None:
            pass
        else:
            window.set_at(direction, utils.COL_BLUE)
        
        pygame.display.flip()
    pygame.quit()