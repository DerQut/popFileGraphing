import pygame

pygame.display.init()
pygame.font.init()

SF_Pro_Medium_24 = pygame.font.Font("assets/SFPRODISPLAYMEDIUM.OTF", 24)
SF_Pro_Medium_20 = pygame.font.Font("assets/SFPRODISPLAYMEDIUM.OTF", 20)
SF_Pro_Medium_18 = pygame.font.Font("assets/SFPRODISPLAYMEDIUM.OTF", 18)

SF_Pro_Light_42 = pygame.font.Font("assets/SFNSDisplay-Thin.otf", 42)
SF_Pro_Light_16 = pygame.font.Font("assets/SFNSDisplay-Thin.otf", 16)

bg_colour = (36, 24, 22)
bg_colour_inactive = (33, 26, 26)
bg_border = (0, 0, 0)

button_colour_glowing = (150, 147, 147)
button_colour_light = (102, 97, 97)
button_colour_dark = (68, 61, 61)

orange = (247, 159, 13)
dark_orange = (190, 106, 10)

blue = (37, 87, 226)
dark_blue = (42, 58, 119)

text_colour = (255, 255, 255)
