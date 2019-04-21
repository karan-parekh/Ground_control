from pygame_functions import *
# from gc_functions import *
from gc_fsm import *
import pygame

pixels = 512
screenSize(pixels, pixels)
pygame.display.set_caption("Ground control")
setBackgroundColour("grey")


def main():
    draw_airport(airport1)
    wordbox = place_command_box()
    AI123 = DepAircraft("AI123", "B747", "G1")
    AI123.generate_craft()
    while True:
        instructions = request_command(wordbox)
        AI123.evaluate_instructions(instructions)
        draw_airport(airport1)
        tick(30)


if __name__ == '__main__':
    main()
