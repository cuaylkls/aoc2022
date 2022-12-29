data = []

with open("input-data/day4-input.txt", "r") as f:
    for line in f:
        line = line.rstrip()
        data.append(
            [list(map(int, assignment.split('-'))) for assignment in line.split(',')]
        )

fully_covered = []
over_lapped = []

for pair in data:
    assignment1, assignment2 = pair

    if assignment2[0] <= assignment1[0] <= assignment2[1] and assignment2[1] >= assignment1[1] >= assignment2[0]:
        fully_covered.append(pair)
        over_lapped.append(pair)
    elif assignment1[0] <= assignment2[0] <= assignment1[1] and assignment1[1] >= assignment2[1] >= assignment1[0]:
        fully_covered.append(pair)
        over_lapped.append(pair)
    elif assignment2[0] <= assignment1[1] <= assignment2[1] or \
            assignment1[0] <= assignment2[1] <= assignment1[1]:
        over_lapped.append(pair)

print(len(fully_covered))
print(len(over_lapped))
