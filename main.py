import pygame
import sys
import config
from simengine import Simulation
import fileio


def main():
    """Main application loop."""
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Digital Primordial Soup - Artificial Life")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    # --- CORRECTED INITIALIZATION LOGIC ---
    sim = Simulation()

    # 1. Try to load the previous state from the file.
    loaded_state = fileio.load_state()

    # 2. If loading was successful, populate the simulation with the data.
    if loaded_state and all(d is not None for d in loaded_state):
        sim.critters, sim.food, sim.generation = loaded_state
    # 3. Otherwise, reset to a brand new simulation.
    else:
        sim.reset()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    sim.reset()
                if event.key == pygame.K_f:
                    sim.add_food()
                if event.key == pygame.K_s:
                    fileio.save_state(sim.critters, sim.food, sim.generation)
                    running = False

        sim.update()

        screen.fill(config.BACKGROUND_COLOR)
        sim.draw(screen)

        stats_text = (
            f"Population: {len(sim.critters)} | "
            f"Food: {len(sim.food)} | "
            f"Generation: {sim.generation} | "
            f"FPS: {int(clock.get_fps())}"
        )
        controls_text = "Controls: [R] Reset | [F] Add Food | [S] Save & Quit"

        stats_surface = font.render(stats_text, True, config.FONT_COLOR)
        controls_surface = font.render(controls_text, True, config.FONT_COLOR)

        screen.blit(stats_surface, (10, 10))
        screen.blit(controls_surface, (10, config.SCREEN_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

