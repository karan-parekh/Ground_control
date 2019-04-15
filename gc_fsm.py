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
