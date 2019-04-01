from pygame_functions import *
from gc_functions import *
import pygame

pixels = 800
screenSize(pixels, pixels)
pygame.display.set_caption("Ground control")
setBackgroundColour("grey")


def main():
    wordbox = place_command_box()
    B747 = DepAircraft("AI117", "B747", "G1")
    instrcutions = request_command(wordbox)
    evaluate_instrcutions()
    endWait()


if __name__ == '__main__':
    main()
