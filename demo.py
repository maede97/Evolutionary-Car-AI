import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from evolutional_ai import car
from evolutional_ai import utils
from evolutional_ai import track

if __name__ == "__main__":
    pygame.init()

    font = pygame.font.Font(pygame.font.get_default_font(), 12)

    track = track.Track(utils.DEMO_TRACK)
    track.load() # load the track from disk

    start_point, direction = track.get_start_info()

    window = pygame.display.set_mode(utils.SIZE)

    car = car.Car(start_point, direction, track.image)

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
        window.blit(track.image, (0,0))

        if car.crashed:
            restart = True
        car.perform_autonomous_action()
        car.update()

        car.draw(window, True)

        text = font.render("Velocity: {:.3f}, Angle Velocity: {:.3f}, Fitness: {:.3f}".format(car.velocity, car.angle_velocity, track.get_fitness(car.position[0], car.position[1])), True, utils.COL_WHITE)
        window.blit(text, (480, 15))

        pygame.display.flip()

    pygame.quit()