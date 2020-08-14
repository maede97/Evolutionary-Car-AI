import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math

from evolutional_ai import utils
from evolutional_ai import track

if __name__ == "__main__":
    pygame.init()

    track = track.Track(utils.DRAW_TRACK)

    window = pygame.display.set_mode(utils.SIZE)
    pygame.display.set_caption("Draw map")

    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    finish = True
                elif event.key == ord('s'):
                    track.set_image(window)
                    track.save()
                    #pygame.image.save(window, os.path.join(os.path.dirname(os.path.abspath(__file__)), utils.DRAW_RACETRACK))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    track.add_point(event.pos[0], event.pos[1])
                elif event.button == 3:
                    track.remove_point()
        
        window.fill((0,0,0))

        # for now: draw circles from tracks data
        if track.data:
            if len(track.data) == 1:
                pygame.draw.circle(window, utils.COL_WHITE, track.data[0], track.thickness)
            # get first data point
            ax,ay = track.data[0]
            for cx, cy in track.data[1:]:
                # calculate direction
                lineDir = cx - ax, cy - ay
                line_length = math.sqrt(lineDir[0] ** 2 + lineDir[1] ** 2)
                lineDir = lineDir[0] / line_length, lineDir[1] / line_length
                for i in range(int(math.sqrt((ax-cx)**2 + (ay-cy)**2))):
                    pygame.draw.circle(window, utils.COL_WHITE, (ax+int(i*lineDir[0]), ay + int(i * lineDir[1])), track.thickness)

                ax,ay = cx,cy

        pygame.display.flip()
    pygame.quit()