import pygame

import program


def main():

    clock = pygame.time.Clock()

    while program.program_window.running:

        clock.tick(150)

        program.program_window.run()


if __name__ == "__main__":
    main()
