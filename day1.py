f = open("day1-input.txt", "r")

data = f.read()

elf_calorie_counts = data.split("\n\n")
elf_calorie_counts = [tuple(map(int,item.split())) for item in elf_calorie_counts]

elf_total_calories = list(map(sum, elf_calorie_counts))

print("Part 1: {}".format(max(elf_total_calories)))

elf_total_calories.sort(reverse=True)

top3 = elf_total_calories[:3]


print("Part 2: {}".format(sum(top3)))
