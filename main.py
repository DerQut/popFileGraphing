import pygame


def main():

    clock = pygame.time.Clock()

    import program

    while program.program_window.running:

        clock.tick(150)

        program.program_window.run()


if __name__ == "__main__":
    main()
