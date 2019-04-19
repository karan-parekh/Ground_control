from transitions import Machine
from transitions import State


class DepAircraft:
    @staticmethod
    def readback():
        print("Reading back")

    dark = State('dark')
    pushback = State('pushback', on_enter=['readback'])
    taxi = State('taxi', on_enter=['readback'])
    hold_position = State('hold_position', on_enter=['readback'])
    hold_short = State('hold_short', on_enter=['readback'])
    take_off = State('take_off', on_enter=['readback'])

    states = [dark, pushback, taxi, hold_short, hold_position, take_off]

    transitions = [
        ['pb', dark, pushback],
        ['txi', pushback, taxi],
        ['hs', taxi, hold_short],
        ['tkf', hold_short, take_off],
        ['hp', '*', hold_position]
    ]

    def __init__(self, callsign):
        self.callsign = callsign
        self.machine = Machine(model=self, states=DepAircraft.states, transitions=DepAircraft.transitions, initial=DepAircraft.dark)

    taxiways = ['A', 'M', 'N', 'W', 'X', 'Y', 'Z']
    keywords = ['PB', 'TXW', 'FCN', 'TXI', 'VIA', 'HS', 'RNW', 'HP', 'CNT', 'TWR', 'FRQ', 'NORTH', 'SOUTH', 'EAST', 'WEST',
                'NEG', 'AFFIRM', '09', '27', '123.9']
    
    def evaluate_instructions(self):
        print(self.state)
        cmd = input("Enter Instructions: ").upper()
        cmd = cmd.split(' ')
        inst = []
        for i in cmd:
            if i in self.keywords or i in self.taxiways:
                inst.append(i)
        transition = inst[0].lower()
        taxiway = inst[1]
        print(inst)
        print(transition)
        self.trigger(transition)
        print(self.state)
        print(taxiway)
        print(inst.index(taxiway))
    

if __name__ == '__main__':
    AI123 = DepAircraft("AI123")
    AI123.evaluate_instructions()
