from pygame_functions import *
from gc_functions import *
import pygame

pixels = 512
screenSize(pixels, pixels)
pygame.display.set_caption("Ground control")
setBackgroundColour("grey")


def main():
    draw_airport(airport1)
    wordbox = place_command_box()
    b747 = DepAircraft("AI117", "B747", "G1")
    b747.generate_craft()
    while True:
        instructions = request_command(wordbox)
        b747.evaluate_instructions(instructions)
        draw_airport(airport1)
        tick(30)


if __name__ == '__main__':
    main()
