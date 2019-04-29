from transitions import Machine
from transitions import State
from game_data import *
from pygame_functions import *
import math


def draw_airport(airport):
    for element in airport.values():
        drawLine(*element)
        # drawLine(element[0], element[1], element[2], element[3], (255, 0, 0, 255), element[5])
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
    txw = ''
    rnw = ''
    facing = ''
    inst = ''
    slope = 0

    def readback(self):
        print("Reading back")
        pass

    def pushback_(self):
        self.txw = self.inst[1]
        if 'FCN' in self.inst:
            self.facing = self.inst[self.inst.index('FCN') + 1]
        next_pos = get_next_pos(self.gate_no, self.txw)
        last_pos = get_coordinates(self.gate_no)
        last_pos = (last_pos[0][0], last_pos[0][1])
        finish = self.move_craft(last_pos, next_pos)
        if finish:
            if self.facing == 'WEST':
                print("Facing WEST")
                self.turn_craft(270)
            elif self.facing == 'EAST':
                print("Facing EAST")
                self.turn_craft(90)
            else:
                print("Cannot face " + self.facing)

    def taxi_(self):
        self.txw = list(self.txw)
        via = self.inst.index('VIA') + 1
        if 'HS' in self.inst:
            hs = self.inst.index('HS')
            self.txw.extend(self.inst[via:hs])
        else:
            self.txw.extend(self.inst[via:])
        if 'RNW' in self.inst:
            self.rnw = self.inst[self.inst.index('RNW') + 1]
        for t in range(len(self.txw)-1):
            finish = self.move_craft(self.txw[t], self.txw[t+1])
            if finish:
                self.turn_craft(math.degrees(math.atan(self.slope)))  # inverse tangent of slope in degrees

    def hold_short_(self):
        pass

    def hold_position_(self):
        pass

    def take_off_(self):
        pass

    dark = State('dark')
    pushback = State('pushback', on_enter=['pushback_'])
    taxi = State('taxi', on_enter=['taxi_'])
    hold_position = State('hold_position', on_enter=['hold_position_'])
    hold_short = State('hold_short', on_enter=['hold_short_'])
    take_off = State('take_off', on_enter=['take_off_'])

    states = [dark, pushback, taxi, hold_short, hold_position, take_off]

    transitions = [
        ['pb', [dark, hold_position], pushback, ],
        ['txi', [pushback, hold_position], taxi],
        ['hs', taxi, hold_short],
        ['tkf', hold_short, take_off],
        ['hp', '*', hold_position]
    ]

    def __init__(self, callsign, model, gate_no):
        self.callsign = callsign
        self.machine = Machine(model=self, states=DepAircraft.states, transitions=DepAircraft.transitions,
                               initial=DepAircraft.dark, after_state_change='readback')
        self.gate_no = gate_no.upper()
        self.model = model.upper()
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

    def get_sprite(self):
        craft = makeSprite(sprites[self.model])
        transformSprite(craft, self.angle, self.scale)
        return craft

    taxiways = ['A', 'M', 'N', 'W', 'X', 'Y', 'Z']
    keywords = ['PB', 'TXW', 'FCN', 'TXI', 'VIA', 'HS', 'RNW', 'HP', 'CNT', 'TWR', 'FRQ', 'NORTH', 'SOUTH', 'EAST', 'WEST',
                'NEG', 'AFFIRM', '09', '27', '123.9']
    
    def evaluate_instructions(self, inst):
        inst = inst.upper().split(' ')
        print(self.state)
        command = []
        for i in inst:
            if i in self.keywords or i in self.taxiways:
                command.append(i)
        self.inst = command
        trigger = command[0].lower()
        print(command)
        print(trigger)
        self.trigger(trigger)
        print(self.state)
        print(self.txw)

    def turn_craft(self, deg):
        transformSprite(self.craft, deg, self.scale)
        self.angle = deg

    def move_craft(self, last_pos, next_pos):
        # x, y = 0, 0
        if last_pos[0] == next_pos[0]:  # for vertical line
            direction = 1 if next_pos[1] > last_pos[1] else -1
            for y in range(int(last_pos[1]), int(next_pos[1]) - 1, direction):
                x = last_pos[0]  # equation of a vertical line
                moveSprite(self.craft, x, y, True)
                draw_airport(airport1)
                pause(25)
            finish = True if (x, y) == next_pos else False
            # self.angle = 180 if direction == 1 else 360
        elif last_pos[1] == next_pos[1]:  # for horizontal line
            direction = 1 if next_pos[0] > last_pos[0] else -1
            for x in range(last_pos[0], next_pos[0] + 1, direction):
                y = last_pos[1]  # equation of a horizontal line
                moveSprite(self.craft, x, y, True)
                draw_airport(airport1)
                pause(25)
            finish = True if (x, y) == last_pos else False
            # self.angle = 270 if direction == 1 else 90
        else:   # for inclined line
            af = [float(i) for i in last_pos]
            bf = [float(i) for i in next_pos]
            m = (bf[1] - af[1]) / (bf[0] - af[0])  # slope of line
            self.slope = m
            c = af[1] - m * af[0]  # constant
            direction = 1 if next_pos[0] > last_pos[0] else -1
            offset = 1 if m < 0 else -1
            for x in range(last_pos[0], next_pos[0] + offset, direction):
                y = m * x + c  # equation of a straight line
                moveSprite(self.craft, x, y, True)
                draw_airport(airport1)
                pause(25)
            finish = True if (x, y) == last_pos else False
        return finish

#
# def main():
#     # draw_airport(airport1)
#     wordbox = place_command_box()
#     AI123 = DepAircraft("AI123", "B747", "G1")
#     AI123.generate_craft()
#     while True:
#         instruction = request_command(wordbox).upper()
#         AI123.evaluate_instructions(instruction)
#         tick(30)
#
#
# if __name__ == '__main__':
#     main()
