import unittest
from day9 import Position, PositionError


class PositionTestInit(unittest.TestCase):
    def test_position_init(self):
        # test create instance of position
        self.assertIsInstance(Position(), Position)

    def test_position_init_with_coordinates(self):
        p = Position(1, 1)
        self.assertEqual((1, 1), p.coordinates)


class PositionTestPosition(unittest.TestCase):
    def test_position(self):
        p = Position()

        self.assertEqual((0, 0), p.coordinates)


class PositionTestMove(unittest.TestCase):
    def test_move_invalid(self):
        p = Position()

        self.assertRaises(PositionError, p.move, "X")

    def test_move_left(self):
        p = Position()

        # move one space left
        p.move("L")
        self.assertEqual((-1, 0), p.coordinates)

        # move 10 spaces left
        p.move("L", 10)
        self.assertEqual((-11, 0), p.coordinates)

    def test_move_up(self):
        p = Position()

        # move one space up
        p.move("U")
        self.assertEqual((0, -1), p.coordinates)

        # move 10 spaces up
        p.move("U", 10)
        self.assertEqual((0, -11), p.coordinates)

    def test_move_right(self):
        p = Position()

        # move one space right
        p.move("R")
        self.assertEqual((1, 0), p.coordinates)

        # move 10 spaces right
        p.move("R", 10)
        self.assertEqual((11, 0), p.coordinates)

    def test_move_down(self):
        p = Position()

        # move one space down
        p.move("D")
        self.assertEqual((0, 1), p.coordinates)

        # move 10 spaces down
        p.move("D", 10)
        self.assertEqual((0, 11), p.coordinates)

    def test_move_using_coordinates(self):
        p = Position()

        # one step
        p.move_using_coordinates((-1, 2), 1)

        self.assertEqual((-1, 2), p.coordinates)

        # multiple step step
        p.move_using_coordinates((1, 3), 2)

        self.assertEqual((1, 8), p.coordinates)


class PositionTestVisitedPositions(unittest.TestCase):
    def test_visited_positions_single_steps(self):
        p = Position()
        p.move("U")
        p.move("L")
        p.move("D")
        p.move("D")
        p.move("R")

        visited = p.visited_positions

        self.assertEqual(6, len(visited))
        self.assertIn((0, 0), visited)
        self.assertIn((0, -1), visited)
        self.assertIn((-1, -1), visited)
        self.assertIn((-1, 0), visited)
        self.assertIn((-1, 1), visited)
        self.assertIn((0, 1), visited)

    def test_visited_positions_multiple_steps(self):
        p = Position()
        p.move("U")
        p.move("L")
        p.move("D", 2)
        p.move("R", 3)

        visited = p.visited_positions
        self.assertEqual(8, len(visited))
        self.assertIn((0, 0), visited)
        self.assertIn((0, -1), visited)
        self.assertIn((-1, -1), visited)
        self.assertIn((-1, 0), visited)
        self.assertIn((-1, 1), visited)
        self.assertIn((0, 1), visited)
        self.assertIn((1, 1), visited)
        self.assertIn((2, 1), visited)

    def test_visited_positions_move_with_coordinates(self):
        p = Position()

        p.move_using_coordinates((-1, -2), 3)

        visited = p.visited_positions
        self.assertEqual(4, len(visited))
        self.assertIn((0, 0), visited)
        self.assertIn((-1, -2), visited)
        self.assertIn((-2, -4), visited)
        self.assertIn((-3, -6), visited)


class LinkedPositionTest(unittest.TestCase):
    def test_create_linked_position(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        # instance check
        self.assertIsInstance(p2, Position)

        # check linked_position property
        self.assertEqual(p2, p1.linked_position)

        # initial co-ordinate match
        self.assertEqual(p1.coordinates, p2.coordinates)

        # exception when creating second linked position
        self.assertRaises(
            PositionError,
            lambda: p1.create_linked_position()
        )

    def test_follow_left_from_overlap(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        '''
        {-} ........[12]
        {L} ....[ 1][ 2]
        '''
        p1.move("L")

        # no movement expected
        self.assertEqual((0, 0), p2.coordinates)

    def test_follow_left_from_adjacent_right(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        '''
        {-} ........[12]
        {L} ....[ 1][ 2]
        {L} [ 1][ 2][ s]
        '''
        p1.move("L", 2)

        # move one to the left
        self.assertEqual((-1, 0), p2.coordinates)

    def test_follow_left_from_adjacent_left(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        '''
        {-} ........[12]....
        {R} ........[ 2][ 1]
        {R} ............[ 2][ 1]
        {L} ........[ S][12]....
        '''
        p1.move("R", 2)
        p1.move("L")

        # coordinates overlap, so no change
        self.assertEqual((1, 0), p2.coordinates)

    def test_follow_right_from_overlap(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        '''
        {-} ........[12]....
        {R} ........[ 2][ 1]
        '''
        p1.move("R")

        # no movement expected
        self.assertEqual((0, 0), p2.coordinates)

    def test_follow_right_from_adjacent_right(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        '''
        {-} ........[12]....
        {L} ....[1 ][ 2]....
        {L} [1 ][2 ][S ]....
        {R} ....[12][S ]....
        '''
        p1.move("L", 2)
        p1.move("R")

        # coordinates overlap, so no change
        self.assertEqual((-1, 0), p2.coordinates)

    def test_follow_right_from_adjacent_left(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        '''
        {-} ........[12]........
        {R} ........[ 2][1 ]....
        {R} ........[S ][2 ][1 ]
        '''
        p1.move("R", 2)

        # move one to the right
        self.assertEqual((1, 0), p2.coordinates)

    def test_follow_up_from_overlap(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        p1.move("U", 2)
        p1.move("D")
        self.assertEqual((0, -1), p2.coordinates)

        '''
        {-} ....................
            ........[12]........
            ........[S ]........
        {U} ........[1 ]........
            ........[2 ]........
            ........[S ]........
        '''
        p1.move("U")

        # no change
        self.assertEqual((0, -1), p2.coordinates)

    def test_follow_up_left(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        p1.move("U", 2)
        self.assertEqual((0, -1), p2.coordinates)

        '''
        {-} ........[1 ]........
            ........[2 ]........
            ........[S ]........
        {L} ....[1 ]............
            ........[2 ]........
            ........[S ]........
        '''
        p1.move("L")

        # no change touching
        self.assertEqual((0, -1), p2.coordinates)

    def test_follow_up_left2(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        p1.move("U", 2)
        self.assertEqual((0, -1), p2.coordinates)

        '''
        {-} ........[1 ]........
            ........[2 ]........
            ........[S ]........
        {L} ....[1 ]............
            ........[2 ]........
            ........[S ]........
        {L} [1 ][2 ]............
            ....................
            ........[S ]........
        '''
        p1.move("L", 2)

        # move diagonal up left
        self.assertEqual((-1, -2), p2.coordinates)

    def test_follow_up_right(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        p1.move("U", 2)
        self.assertEqual((0, -1), p2.coordinates)

        '''
        {-} ........[1 ]........
            ........[2 ]........
            ........[S ]........
        {R} ............[1 ]....
            ........[2 ]........
            ........[S ]........
        '''
        p1.move("R")

        # no change touching
        self.assertEqual((0, -1), p2.coordinates)

    def test_follow_up_right2(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        p1.move("U", 2)
        self.assertEqual((0, -1), p2.coordinates)

        '''
        {-} ........[1 ]........
            ........[2 ]........
            ........[S ]........
        {R} ............[1 ]....
            ........[2 ]........
            ........[S ]........
        {R} ............[2 ][1 ]
            ....................
            ........[S ]........
        '''
        p1.move("R", 2)

        # diagonal up right
        self.assertEqual((1, -2), p2.coordinates)

    def test_follow_left_up(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        p1.move("L", 2)
        self.assertEqual((-1, 0), p2.coordinates)

        '''
        {-} ....................
            [1 ][2 ][S ]........
        {U} [1 ]................
            ....[2 ][S ]........
        '''
        p1.move("U")

        # touching points
        self.assertEqual((-1, -0), p2.coordinates)

    def test_follow_left_up2(self):
        p1 = Position()
        p2 = p1.create_linked_position()

        p1.move("L", 2)
        self.assertEqual((-1, 0), p2.coordinates)

        '''
        {-} ....................
            ....................
            [1 ][2 ][S ]........
        {U} [1 ]................
            ....[2 ][S ]........
        {U} [1 ]................
            [2 ]................
            ........[S ]........
        '''
        p1.move("U", 2)

        # move diagonal up left
        self.assertEqual((-2, -1), p2.coordinates)


if __name__ == '__main__':
    unittest.main()
