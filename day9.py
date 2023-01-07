import math

from typing import Dict


class PositionError(Exception):
    pass


class Position:
    _lookup = {
        'L': (-1, 0),
        'R': (1, 0),
        'U': (0, -1),
        'D': (0, 1)
    }

    @property
    def coordinates(self):
        return self._x_pos, self._y_pos

    @property
    def linked_position(self):
        return self._linked_position

    @staticmethod
    def _sign_int(number):
        if number == 0:
            return 0
        else:
            return 1 if number > 0 else -1

    def __init__(self, x_pos=0, y_pos=0):
        self._x_pos = x_pos
        self._y_pos = y_pos
        self.visited_positions = [(0, 0)]
        self._linked_position = None

    def move_using_coordinates(self, instruction, step):
        x_mov, y_mov = instruction

        # get next position
        cur_position = self.coordinates

        self._x_pos += step * x_mov
        self._y_pos += step * y_mov

        new_position = (self._x_pos, self._y_pos)

        while cur_position != new_position:
            cur_position = (cur_position[0] + x_mov, cur_position[1] + y_mov)

            if cur_position not in self.visited_positions:
                self.visited_positions.append(cur_position)

            if self._linked_position is not None:
                linked: Position = self._linked_position
                link_x, link_y = linked.coordinates
                link_x_distance = cur_position[0] - link_x
                link_y_distance = cur_position[1] - link_y

                if (-1 <= link_x_distance <= 1) and (-1 <= link_y_distance <= 1):
                    # no move required
                    pass
                else:
                    if (abs(link_x_distance) > 1) and (abs(link_y_distance) == 1):
                        # more than 1 point away in a left or right direction
                        link_x_mov = link_x_distance - self._sign_int(link_x_distance)
                        link_y_mov = link_y_distance
                    elif (abs(link_y_distance) > 1) and (abs(link_x_distance) == 1):
                        # more than 1 point away in a up or down direction
                        link_x_mov = link_x_distance
                        link_y_mov = link_y_distance - self._sign_int(link_y_distance)
                    else:
                        # more than one point away in either an up / down or left / right direction
                        link_x_mov = link_x_distance - self._sign_int(link_x_distance)
                        link_y_mov = link_y_distance - self._sign_int(link_y_distance)

                    linked.move_using_coordinates((link_x_mov, link_y_mov), 1)

    def move(self, direction, step=1):
        if direction not in self._lookup:
            raise PositionError(f"Invalid direction ({direction}), expecting (U, D, L, R)")

        self.move_using_coordinates(self._lookup[direction], step)

    def create_linked_position(self):
        if self._linked_position is not None:
            raise PositionError("Linked position already created")

        self._linked_position = Position(self._x_pos, self._y_pos)

        return self._linked_position

    def __str__(self):
        return f"Co-ords: (x={self._x_pos},y={self._y_pos})"

    def __repr__(self):
        return f"Position({self._x_pos}, {self._y_pos})"


def main():
    # create a dictionary to hold all points
    points: Dict[str, Position] = {}

    # intilise points and their respective linked points
    for i in range(0, 10):
        if i == 0:
            points[f"P{i}"] = Position()
        else:
            points[f"P{i}"] = points[f"P{i-1}"].create_linked_position()

    # get references to points we need to report on
    h = points["P0"]
    p2 = points["P1"]
    t = points["P9"]

    # read input file
    with open("input-data/day9-input.txt", "r") as f:
        for line in f:
            components = line.split()
            h.move(components[0], int(components[1]))

    print(f"Part 1: {len(p2.visited_positions)}")
    print(f"Part 2: {len(t.visited_positions)}")


if __name__ == '__main__':
    main()
