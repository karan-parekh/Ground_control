from game_data import *
from pygame_functions import *


class DepAircraft:
    def __init__(self, call_sign, model, gate_no):
        self.call_sign = call_sign.upper()
        self.model = model.upper()
        self.gate_no = gate_no.upper()
        self.generate_craft()

    def generate_craft(self):
        craft = self.get_sprite(self.model)
        self.move_to_gate(craft, self.gate_no)
        showSprite(craft)
        
    def move_to_gate(self, craft, gate_no):
        gate_pos = gates[gate_no]
        moveSprite(craft, *gate_pos)

    def get_sprite(self, model):
        craft = makeSprite(sprites[model])
        transformSprite(craft, -90, 0.08)
        return craft

    def destroy_craft(self):
        pass

    def evaluate_instrcutions(self, craft, instruction):
        if instruction == "taxi":
            for x in range(300, 50, -1):
                moveSprite(craft, x, 50, True)
                # drawLine(*taxiway)
                pause(25)


def request_command(wordbox):
    instruction = textBoxInput(wordbox)
    readback = makeLabel(instruction, 25, 10, 700)
    showLabel(readback)
    return instruction


def place_command_box():
    wordbox = makeTextBox(10, 750, 300, 0, "Enter instructions", 0, 24)
    showTextBox(wordbox)
    return wordbox
