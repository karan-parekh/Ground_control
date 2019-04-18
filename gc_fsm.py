from transitions import Machine
import enum


class States(enum.Enum):
    dark = 'dark'
    pushback = 'pushback'
    taxi = 'taxi'
    hold_position = 'hold_position'
    hold_short = 'hold_short'
    take_off = 'take_off'


globals().update(States.__members__)


class DepAircraft:
    states = [States.dark, States.pushback, States.taxi, States.hold_position, States.hold_short, States.take_off]
    transitions = [
        ['pushback', States.dark, States.pushback],
        ['taxi', 'pushback', 'taxi'],
        ['hold_short', 'taxi', 'hold_short'],
        ['take_off', 'hold_short', 'take_off'],
        ['hold_position', '*', 'hold_position'],
    ]

    def __init__(self, callsign):
        self.callsign = callsign
        self.machine = Machine(model=self, states=DepAircraft.states, transitions=DepAircraft.transitions, initial='dark')

    trans_dict = {
        'PB': 'pushback',
        'TXI': 'taxi',
        'HS': 'hold_short',
        'HP': 'hold_position',
        'TKF': 'take_off'
    }


def expected_inst(prev_state):
    instructions = {
        'dark': 'pb',
        'pushback': 'taxi',
        'taxi': 'hs'
    }
    return instructions[prev_state]


taxiways = ['A', 'M', 'N', 'W', 'X', 'Y', 'Z']
keywords = ['PB', 'TXW', 'FCN', 'TXI', 'VIA', 'HS', 'RNW', 'HP', 'CNT', 'TWR', 'FRQ', 'NORTH', 'SOUTH', 'EAST', 'WEST',
            'NEG', 'AFFIRM', '09', '27', '123.9']

def evaluate_instructions(obj):
    print(obj.state)
    cmd = input("Enter Instructions: ").upper()
    cmd = cmd.split(' ')
    inst = []
    for i in cmd:
        if i in keywords or i in taxiways:
            inst.append(i)
    transition = obj.trans_dict[inst[0]]
    taxiway = inst[1]
    print(inst)
    print(transition)
    obj.trigger(transition)
    print(obj.state)
    print(taxiway)
    print(inst.index(taxiway))


if __name__ == '__main__':
    AI123 = DepAircraft("AI123")
    evaluate_instructions(AI123)
    # print(States.dark)


