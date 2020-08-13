import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

import car
import utils

if __name__ == "__main__":
    pygame.init()
    background, start_point, direction = utils.loadBackgroundImage(True)
    window = pygame.display.set_mode(utils.SIZE)

    car = car.Car(start_point, direction, background)

    if utils.DEMO_BRAIN == "":
        print("Error: Please set the file to load inside the configuration.")
    else:
        car.model.load_from_file(utils.DEMO_BRAIN)

    finished = False
    restart = False

    while not finished:
        window.fill(utils.COL_BLACK)
        if restart:
            car.reset(start_point, direction)
            restart = False
        
        # Consume all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    finished = True
        window.blit(background, (0,0))

        if car.crashed:
            restart = True
        car.perform_autonomous_action()
        car.update()
        car.draw(window, True)

        pygame.display.flip()

    pygame.quit()