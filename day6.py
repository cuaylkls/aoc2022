with open("input-data/day6-input.txt", "r") as f:
    pos = 4
    current4 = f.read(4)
    current14 = current4
    # cont = True

    while True:

        c = f.read(1)

        if c == '':
            break

        if len(current4) == len(set(current4)):
            comm_start = pos
        else:
            current4 = current4[1:] + c

        if len(current14) < 14:
            pass
        elif len(current14) == len(set(current14)):
            msg_start = pos
            break

        pos += 1

        if len(current14) < 14:
            current14 = current14 + c
        else:
            current14 = current14[1:] + c


print(msg_start)
