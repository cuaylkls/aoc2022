import re

stacks_sim1 = {}
stacks_sim2 = {}

movements = []

stack_item_lines = []
stack_list_line = ""


def get_movement_info(movement_line):
    # extract movement info from movement line
    regex = r"^move (\d+) from (\d+) to (\d+)$"
    m = re.match(regex, movement_line)

    return {
        'from': m.group(2),
        'to': m.group(3),
        'total': int(m.group(1)),
        'string': m.group(0)
    }


def fixed_width_split_string(string, size):
    # break string into fixed width chunks
    ret_list = []
    pos = 0

    while pos < len(string):
        ret_list.append(string[pos:pos+size])
        pos += size

    return ret_list


with open("day5-input.txt", "r") as f:
    line = f.readline()

    while line.rstrip() != "":
        # list item in list is the stack names
        stack_item_lines.append([re.sub(r"[\s\[\]]", "", item) for item in fixed_width_split_string(line, 4)])

        line = f.readline()

    line = f.readline()

    while line.rstrip() != "":
        movements.append(get_movement_info(line))
        line = f.readline()


# create initial stacks
pos = 0
for stack in stack_item_lines[len(stack_item_lines)-1]:
    items = list(
            filter(
                lambda item: item != "",
                [item[pos] for item in stack_item_lines[:-1]]
            )
    )
    items.reverse()
    stacks_sim1[stack] = items
    stacks_sim2[stack] = items.copy()
    pos += 1


# perform movements
pos = 1

for movement in movements:
    from_stack = movement["from"]
    to_stack = movement["to"]
    moves = movement["total"]

    for move in range(0, moves):
        stacks_sim1[to_stack].append(
            stacks_sim1[from_stack].pop()
        )

    stacks_sim2[to_stack].extend(
        stacks_sim2[from_stack][-moves:]
    )
    del stacks_sim2[from_stack][-moves:]

    pos += 1

print(stacks_sim2)
print(
    "".join(
        [
            stacks_sim1[stack][-1] for stack in stacks_sim1
        ]
    )
)
print(
    "".join(
        [
            stacks_sim2[stack][-1] for stack in stacks_sim2
        ]
    )
)
