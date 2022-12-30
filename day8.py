"""
    Day 8 Task

        The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain
        that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be
        a good location for a tree house.

        First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to
        count the number of trees that are visible from outside the grid when looking directly along a row or column.

        The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input).
        For example:

        30373
        25512
        65332
        33549
        35390

        Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the
        tallest. A tree is visible if all of the other trees between it and an edge of the grid are shorter than it.
        Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

        All of the trees around the edge of the grid are visible - since they are already on the edge, there are no
        trees to block the view. In this example, that only leaves the interior nine trees to consider:

        The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other
            trees of height 5 are in the way.)
        The top-middle 5 is visible from the top and right.
        The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of
            height 0 between it and an edge.
        The left-middle 5 is visible, but only from the right.
        The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at
            most height 2 between it and an edge.
        The right-middle 3 is visible from the right.
        In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

    With 16 trees visible on the edge and another 5 visible in the interior,
    a total of 21 trees are visible in this arrangement.

    How many trees are visible from outside the grid?
"""
from colorama import Fore, Style


def display_forest(forest):
    for row in forest:
        item_str = ""

        for tree in row:
            tree_str = str(tree["height"])

            if tree["visible"] is not None:
                colour = Fore.GREEN if tree["visible"] else Fore.LIGHTYELLOW_EX
                tree_str = f"{colour}{tree_str}{Style.RESET_ALL}"

            item_str += tree_str

        print(item_str)


def display_forest_scenic_scores(forest):
    for row in forest:
        item_str = ""

        for tree in row:
            tree_str = str(tree["scenic_score"])
            item_str += f"{tree['height']}:{tree_str:<5} "

        print(item_str)


def set_visibility(forest, x, y, height):
    cur_height = forest[y][x]["height"]
    cur_visible = forest[y][x]["visible"]

    if cur_visible:
        # make no changes if the tree is visible somewhere else
        pass
    else:
        if cur_height > height:
            forest[y][x]["visible"] = True
        else:
            forest[y][x]["visible"] = False

    return cur_height if cur_height > height else height, forest[y][x]["visible"]


def calculate_visibility(forest):
    x_total = len(forest[0])
    y_total = len(forest)

    # row 1 and row -1 visible
    for x_pos in range(0, x_total):
        forest[0][x_pos]["visible"] = True
        forest[-1][x_pos]["visible"] = True

    # column 1 and column -1 visible
    for y_pos in range(1, y_total - 1):
        forest[y_pos][0]["visible"] = True
        forest[y_pos][-1]["visible"] = True

    # left and right view point
    for y_pos in range(1, y_total - 1):
        height = forest[y_pos][0]["height"]
        last_visible = 0
        for x_pos in range(1, x_total - 1):
            height, visibility = set_visibility(forest, x_pos, y_pos, height)

            if visibility:
                last_visible = x_pos

        height = forest[y_pos][-1]["height"]
        for x_pos in range(x_total - 2, last_visible, -1):
            height, visibility = set_visibility(forest, x_pos, y_pos, height)

    # top and bottom viewpoint
    for x_pos in range(1, x_total - 1):
        height = forest[0][x_pos]["height"]
        last_visible = 0

        for y_pos in range(1, y_total - 1):
            height, visibility = set_visibility(forest, x_pos, y_pos, height)

            # if visibility:
            #    last_visible = y_pos

        height = forest[-1][x_pos]["height"]
        for y_pos in range(y_total - 1, 0, - 1):
            height, visibility = set_visibility(forest, x_pos, y_pos, height)


def calculate_all_scenic_scores(forest):
    for y_pos in range(0, len(forest)):
        for x_pos in range(0, len(forest[y_pos])):
            new_scenic_score = calculate_scenic_score(forest, x_pos, y_pos)
            forest[y_pos][x_pos]["scenic_score"] = new_scenic_score


def calculate_scenic_score(forest, x, y):
    tree_height = forest[y][x]["height"]

    def find_tree_distance(direction):
        x_len = len(forest[y])
        y_len = len(forest)

        tree_count = 0

        direction_lookup = {
            'l': (-1, 0), 'r': (1, 0), 'u': (0, -1), 'd': (0, 1)
        }
        x_move, y_move = direction_lookup[direction]

        x_cur = x + x_move
        y_cur = y + y_move
        last_tree_seen_height = 0

        while (x_cur >= 0) and (x_cur < x_len) and (y_cur >= 0) and (y_cur < y_len):
            check_height = forest[y_cur][x_cur]['height']

            # only increment tree count if height exceeds the last tree seen
            # if check_height >= last_tree_seen_height:
            #    tree_count += 1
            #     last_tree_seen_height = check_height
            tree_count +=1
            if check_height >= tree_height:
                break

            x_cur = x_cur + x_move
            y_cur = y_cur + y_move

        return tree_count

    if x == 0 or x == len(forest[y]) - 1 or y == 0 or y == len(forest) - 1:
        return 0

    # look left
    left = find_tree_distance("l")

    # look right
    right = find_tree_distance("r")

    # walk up
    top = find_tree_distance("u")

    # walk down
    bottom = find_tree_distance("d")

    return top * bottom * left * right


def main():
    forest = []

    # read input file into a matrix
    with open("input-data/day8-input.txt", "r") as f:
        for line in f:
            forest.append([{"height": int(height), "visible": None} for height in line.strip()])

    calculate_visibility(forest)
    display_forest(forest)
    calculate_all_scenic_scores(forest)
    display_forest_scenic_scores(forest)

    total_visible = 0
    scenic_score = 0
    for y_pos in range(0, len(forest)):
        for x_pos in range(0, len(forest[y_pos])):

            total_visible += (1 if forest[y_pos][x_pos]["visible"] else 0)
            scenic_score = max(scenic_score, forest[y_pos][x_pos]["scenic_score"])

    print(f"Part 1: {total_visible}")
    print(f"Part 2: {scenic_score}")


if __name__ == '__main__':
    main()