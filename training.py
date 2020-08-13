import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math

# all imports from these files
import car
import utils
import brain

if __name__ == "__main__":
    pygame.init()
    font = pygame.font.Font(pygame.font.get_default_font(), 12)

    background, start_point, direction = utils.loadBackgroundImage()

    window = pygame.display.set_mode(utils.SIZE)

    # Init cars
    cars = []
    for i in range(utils.CARS_PER_GEN):
        cars.append(car.Car(start_point, direction, background))
    
    finished = False
    restart = False
    iterations = 0
    generation = 1

    # Overall
    best_fitness = 0
    best_fitness_genome = None

    # This generation
    curr_best_fitness = 0
    curr_best_fitness_i = None

    while not finished:
        pygame.display.set_caption(f"Generation {generation} - Fitness: {best_fitness}")
        window.fill(utils.COL_BLACK)

        if restart:
            # save best fitness
            if utils.AUTO_SAVE_BEST_GENOME:
                utils.save_genome(utils.AUTO_SAVE_FILENAME, best_fitness_genome)

            generation += 1
            
            utils.MAX_ITERATIONS += 10
            if generation > 20 and iterations == utils.MAX_ITERATIONS:
                utils.MAX_ITERATIONS += 100
            iterations = 0
            # sort vector of cars based on fitness
            cars_sorted = sorted(cars, key=lambda c: -c.fitness)

            # best cars at the front, use first half + mutated for second one
            half = len(cars) // 2

            for i in range(0, half, 2):
                g1, g2 = brain.cross_over(cars_sorted[0].model.get_weights(), cars_sorted[1].model.get_weights())
                cars_sorted[half + i].model.set_weights(g1)
                cars_sorted[half + i + 1].model.set_weights(g2)
            cars_sorted[-1].model.__init__() # create a random car

            # reset all cards
            for i,c in enumerate(cars_sorted):
                c.reset(start_point, direction)
                c.model.set_weights(brain.mutate(c.model.get_weights())) # mutate genes
            cars = cars_sorted
            restart = False
            curr_best_fitness = 0
            curr_best_fitness_i = None

        # consume all pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE:
                    finished = True
                elif event.key == ord('s'):
                    if not curr_best_fitness_i == None:
                        utils.save_genome(cars[curr_best_fitness_i].model.get_weights())

        # add background to window
        window.blit(background, (0,0))

        # Update all cars
        crashed = 0
        for i,c in enumerate(cars):
            if c.crashed:
                # skip crashed cars
                crashed += 1
                if crashed == len(cars):
                    restart = True
                    break
            # calculate fitness
            dx = start_point[0] - c.position[0]
            dy = start_point[1] - c.position[1]
            c.fitness = math.sqrt(dx ** 2 + dy ** 2) # distance to start point

            if c.fitness > best_fitness:
                best_fitness = c.fitness
                best_fitness_genome = c.model.get_weights()

            if c.fitness > curr_best_fitness:
                curr_best_fitness = c.fitness
                if curr_best_fitness_i == None:
                    pass
                else:
                    # set this color back to red
                    cars[curr_best_fitness_i].setRed()
                curr_best_fitness_i = i
                cars[i].setGreen()

            c.perform_autonomous_action()
            c.update()
            if not i == curr_best_fitness_i:
                c.draw(window)
        if not curr_best_fitness_i == None:
            cars[curr_best_fitness_i].draw(window, True) # draw best car on top and with lines

            # Get inputs for this car as well
            inp = cars[curr_best_fitness_i].compute_input_vector()
            text1 = font.render("Inputs: {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}".format(*inp[0]), True, utils.COL_WHITE)
            window.blit(text1, (500,15))

            text2 = font.render("Velocity: {:.3f}, Angle Velocity: {:.3f}".format(cars[curr_best_fitness_i].velocity, cars[curr_best_fitness_i].angle_velocity), True, utils.COL_WHITE)
            window.blit(text2, (500, 30))

        iterations += 1

        # Force restart after MAX_ITERATIONS iterations
        if iterations == utils.MAX_ITERATIONS:
            restart = True
        pygame.display.flip()

    # Quit
    pygame.quit()