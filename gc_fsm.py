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


def expected_inst(prev_state):
    instructions = {
        'dark': 'pb',
        'pushback': 'taxi',
        'taxi': 'hs'
    }
    return instructions[prev_state]


taxiways = ['A', 'M', 'N', 'W', 'X', 'Y', 'Z']
keywords = ['PB', 'TXW', 'FC', 'TXI', 'VIA', 'HS', 'RNW', 'HP', 'CNT', 'TWR', 'FRQ', 'NORTH', 'SOUTH', 'EAST', 'WEST',
            '09', '27', '123.9']


def evaluate_instructions(obj):
    print(obj.state)
    cmd = input("Enter Instructions: ").upper()
    cmd = cmd.split(' ')
    inst = []
    for i in cmd:
        if i in (keywords or taxiways):
            inst.append(i)
    print(inst)
    # just a comment


if __name__ == '__main__':
    AI123 = DepAircraft("AI123")
    evaluate_instructions(AI123)

