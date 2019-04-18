from transitions import Machine


class DepAircraft:
    states = ['dark', 'pushback', 'taxi', 'hold_position', 'hold_short', 'take_off']
    transitions = [
        ['pushback', 'dark', 'pushback'],
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
    obj.trigger(transition)
    print(obj.state)
    print(taxiway)
    print(inst.index(taxiway))


if __name__ == '__main__':
    AI123 = DepAircraft("AI123")
    evaluate_instructions(AI123)

