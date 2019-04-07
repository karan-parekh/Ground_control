
sprites = {
    "B747": "B747.png"
}

taxiway_color = "red"
taxiway_width = 2
runway_width = 8
# TODO: yet to add offsets
oy = 0  # oy is to set offset vertically. set -ve to move up and +ve to move down
ox = 0  # ox is to set offset horizontally. set -ve to move left and +ve to move right
airport1 = {
    "0927": (50, 140, 450, 140, taxiway_color, runway_width),
    "A": (100, 350, 400, 350, taxiway_color, taxiway_width),
    "M": (100, 350, 100, 250, taxiway_color, taxiway_width),
    "N": (400, 350, 400, 250, taxiway_color, taxiway_width),
    "W": (50, 140, 100, 250, taxiway_color, taxiway_width),
    "X": (100, 250, 200, 140, taxiway_color, taxiway_width),
    "Y": (400, 250, 300, 140, taxiway_color, taxiway_width),
    "Z": (400, 250, 450, 140, taxiway_color, taxiway_width),
    "G1": (200, 400, 200, 350, taxiway_color, taxiway_width),
    "G2": (300, 400, 300, 350, taxiway_color, taxiway_width),
}

ramp = [k for k in airport1.keys()]
keywords = []
# keywords = ["GATE", "PUSHBACK", "FACE", "TAXI", "HOLD SHORT", "HOLD POSITION", "CONTACT", "TOWER", "RAMP", "EXIT",
#             "FREQ", "APPROVED", "AFFIRM", "NEGATIVE"]
keywords.extend(ramp)

manual = {
        "pushback": (200, 400, 200, 350)
    }

# manual = {
#         "pushback": ((airport1[last_pos][0], airport1[last_pos][1]),
#                      (airport1[last_pos][2], airport1[last_pos][3]))
#     }


def get_next_pos(instruction, last_pos):
    instruction = instruction.upper().split(' ')
    words = []
    for keyword in keywords:
        if keyword in instruction:
            words.append(keyword)
    # nxt = []
    for word in words:
        nxt = airport1[word][:4]
    nxt = [(nxt[0], nxt[1]), (nxt[2], nxt[3])]
    last_pos = airport1["G1"][:4]
    last_pos = [(last_pos[0], last_pos[1]), (last_pos[2], last_pos[3])]
    line1 = get_constants(nxt[0], nxt[1])
    line2 = get_constants(last_pos[0], last_pos[1])
    return get_intersection_point(line1, line2)


def get_constants(p1, p2):
    a = (p1[1] - p2[1])
    b = (p2[0] - p1[0])
    c = (p1[0] * p2[1] - p2[0] * p1[1])
    return a, b, -c


def get_intersection_point(l1, l2):
    d = l1[0] * l2[1] - l1[1] * l2[0]
    dx = l1[2] * l2[1] - l1[1] * l2[2]
    dy = l1[0] * l2[2] - l1[2] * l2[0]
    if d != 0:
        x = dx / d
        y = dy / d
        return x, y
    else:
        print("Lines do not intersect")
        return False

#
# inst = "pushback on a face w"
# lp = (200, 400)
# np = get_next_pos(inst, lp)
# print(np)
