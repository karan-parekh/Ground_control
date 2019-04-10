from game_data import *
from pygame_functions import *
import math


def draw_airport(airport):
    for element in airport.values():
        drawLine(*element)
    # for taxiway in airport.keys():
    #     label = makeLabel(taxiway, 30, 200, 200, "red")
    #     showLabel(label)


def request_command(wordbox):
    instruction = textBoxInput(wordbox)
    readback = makeLabel(instruction, 25, 10, 420)
    showLabel(readback)
    return instruction


def place_command_box():
    wordbox = makeTextBox(10, 460, 300, 0, "Enter instructions", 0, 24)
    showTextBox(wordbox)
    return wordbox


class DepAircraft:

    def __init__(self, call_sign, model, gate_no):
        self.call_sign = call_sign.upper()
        self.model = model.upper()
        self.gate_no = gate_no.upper()
        self.craft = None
        self.scale = 0.07
        self.x = 0
        self.y = 0
        self.angle = 180

    def generate_craft(self):
        gate_pos = airport1[self.gate_no][0], airport1[self.gate_no][1]
        self.craft = self.get_sprite()
        moveSprite(self.craft, *gate_pos)
        showSprite(self.craft)
        self.last_position(*gate_pos)

    def get_sprite(self):
        craft = makeSprite(sprites[self.model])
        transformSprite(craft, self.angle, self.scale)
        return craft

    def evaluate_instructions(self, instruction):
        last_pos = self.last_position(get=True)
        valid_instruction = True  # TODO: convert "valid_instruction" into a function to validate instruction
        if valid_instruction:
            next_pos = get_next_pos(instruction, last_pos)
            x, y = self.move_craft(last_pos, next_pos)
        deg = self.angle
        self.turn_craft(deg)
        self.last_position(x, y)

    def turn_craft(self, deg):
        diff = abs(self.angle - deg)  # if self.angle > deg else deg - self.angle  # gets the difference between angles
        transformSprite(self.craft, diff, self.scale)
        self.angle = deg

    def move_craft(self, last_pos, next_pos):
        x, y = 0, 0
        if last_pos[0] == next_pos[0]:
            direction = 1 if next_pos[1] > last_pos[1] else -1
            for y in range(int(last_pos[1]), int(next_pos[1]) - 1, direction):
                x = last_pos[0]  # equation of a vertical line
                moveSprite(self.craft, x, y, True)
                draw_airport(airport1)
                pause(25)
            self.angle = 180 if direction == 1 else 360
        elif last_pos[1] == next_pos[1]:
            direction = 1 if next_pos[0] > last_pos[0] else -1
            for x in range(last_pos[0], next_pos[0] + 1, direction):
                y = last_pos[1]  # equation of a horizontal line
                moveSprite(self.craft, x, y, True)
                draw_airport(airport1)
                pause(25)
            self.angle = 270 if direction == 1 else 90
        else:
            af = [float(i) for i in last_pos]
            bf = [float(i) for i in next_pos]
            m = (bf[1] - af[1]) / (bf[0] - af[0])  # slope of line
            c = af[1] - m * af[0]  # constant
            direction = 1 if next_pos[0] > last_pos[0] else -1
            offset = 1 if m < 0 else -1
            for x in range(last_pos[0], next_pos[0] + offset, direction):
                y = m * x + c  # equation of a staright line
                moveSprite(self.craft, x, y, True)
                draw_airport(airport1)
                pause(25)
            self.angle = math.degrees(math.atan(m))  # inverse tangent of slope in degrees
        return x, y

    def last_position(self, x=None, y=None, get=False):
        if get:
            return self.x, self.y
        else:
            # self.angle = angle
            self.x = x
            self.y = y
