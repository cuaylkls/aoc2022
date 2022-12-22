import json

rucksacks = []
groups = []
both_compartments = []

offset_upper = ord('A') - 27
offset_lower = ord('a') - 1
line_no = 1

with open("day3-input.txt", "r") as f:
    for line in f:
        line = line.strip()
        char_count = len(line)
        mid_string = int(char_count / 2)

        if char_count % 2 == 1:
            raise Exception("Odd number of characters")

        compartment_1 = set(line[0:mid_string])
        compartment_2 = set(line[mid_string:])
        error_set = compartment_1 & compartment_2

        errors = [
            ord(error) -
            (offset_lower if str(error).islower() else offset_upper) for error in (error_set)
        ]

        rucksacks.append(
            {
                's': line,
                'c1': line[0:mid_string],
                'c2': line[mid_string:],
                'errors': list(error_set),
                'errors_priorities': errors
            }
        )

        if line_no % 3 == 0:
            group_badge = (group_badge & set(line)).pop()

            groups.append(
                {
                    'group_no': int(line_no/3),
                    'group_badge': group_badge,
                    'group_badge_no': ord(group_badge) - (offset_lower if group_badge.islower() else offset_upper)
                }
            )
        elif line_no % 3 == 1:
            group_badge = set(line)
        elif line_no % 3 == 2:
            group_badge = group_badge & set(line)


        line_no += 1

total_errors = sum(
    [
        sum(item['errors_priorities']) for item in rucksacks
    ]
)

total_group_badges = sum(
    [
        sum(item['group_badge_no'] for item in groups)
    ]
)

print(groups[0])
print(rucksacks[0:3])
print(f"Part 1: {total_errors}")
print(f"Part 2: {total_group_badges}")



