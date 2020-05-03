
import re
import unittest


class MoveRoversException(Exception):
    pass


def move_rovers(input_string):

    # strip any surrounding white space from the input string
    input_string = input_string.strip()

    # make a list of the lines and strip each line of any surrounding white space
    input_lines = [x.strip() for x in input_string.split('\n')]

    # check to see if the number of lines in the input string is odd and at least 3
    line_count = len(input_lines)
    if line_count % 2 != 1 or line_count < 3:
        raise MoveRoversException('The input string must contain an odd '
                                  'number of at least three lines')

    first_line = input_lines[0]

    # check to see if the first line is in an acceptable format
    if re.match(r'^[1-9]\d* [1-9]\d*$', first_line) is None:
        raise MoveRoversException('The first line of the input string must be '
                                  'in the format "X Y" where X and Y are '
                                  'any unsigned integers greater than zero')

    # NOTE: the following variables are named as though we're looking down on the plateau from above
    plateau_width, plateau_height = [int(x) for x in first_line.split()]

    # split the rest of the input string into a list of dicts, each dict representing
    # a rover (its current coordinates and movement instructions).
    rovers = [{
        'current_coordinates': {
            'x': int(input_lines[i].split()[0]),
            'y': int(input_lines[i].split()[1]),
            'facing': input_lines[i].split()[2],
        },
        'movement_instructions': input_lines[i + 1]
    } for i in range(len(input_lines)) if i % 2 == 1]

    # the following will be used to identify rovers by number
    n = 0

    # the following is used to store rovers' current positions so that collision
    # detection and avoidance can be enforced
    rover_current_positions = {}

    # check to see if each rover's coordinates and movement instructions are
    # in an acceptable format and the coordinates are within the dimensions of the plateau

    for rover in rovers:

        rover['id'] = n

        errors = 0

        if not isinstance(rover['current_coordinates']['x'], int):
            errors += 1
        elif rover['current_coordinates']['x'] > plateau_width:
            raise MoveRoversException('A rover cannot exist outside of the X axis of the plateau')

        if not isinstance(rover['current_coordinates']['y'], int):
            errors += 1
        elif rover['current_coordinates']['y'] > plateau_height:
            raise MoveRoversException('A rover cannot exist outside of the Y axis of the plateau')

        if re.match(r'^[NESW]$', rover['current_coordinates']['facing']) is None:
            errors += 1

        if errors:
            raise MoveRoversException(f'A rover\'s coordinates must be in the format "X Y D" '
                                      f'where X and Y are any unsigned integers greater '
                                      f'than zero and where D is either N, E, S or W. The X and Y '
                                      f'coordinates must also be within the dimensions of the plateau. '
                                      f'{str(rover["current_coordinates"])} is invalid.')

        if re.match(r'^[LMR]+$', rover['movement_instructions']) is None:
            raise MoveRoversException('A rover\'s movement instructions '
                                      'must only contain the characters L, M and/or R')

        # store rover's current position
        rover_current_positions[n] = (
            rover['current_coordinates']['x'],
            rover['current_coordinates']['y']
        )

        # increment rover id tag
        n += 1

    # ================================================================================

    # we have established that the supplied data is in a valid format,
    # so we can now proceed with the computations

    # the following function does the actual leg work
    def get_new_position(from_x, from_y, from_facing, move):

        # deal with a left rotation
        if move == 'L':
            left_rotation = {
                'N': 'W',
                'E': 'N',
                'S': 'E',
                'W': 'S',
            }
            # since we are just rotating, x and y stay the same
            return from_x, from_y, left_rotation[from_facing]

        # deal with a right rotation
        elif move == 'R':
            right_rotation = {
                'N': 'E',
                'E': 'S',
                'S': 'W',
                'W': 'N',
            }
            # since we are just rotating, x and y stay the same
            return from_x, from_y, right_rotation[from_facing]

        prevent_movement = False

        # deal with a forward movement (the logic states that the move must equal M)
        if from_facing == 'N':
            # move the rover north (potentially)
            now_y = from_y + 1
            # if the rover is already at the northern most point of the plateau,
            # the rover should not move any further north
            if from_y == plateau_height:
                now_y = plateau_height
            return from_x, now_y, from_facing
        if from_facing == 'E':
            # move the rover east (potentially)
            now_x = from_x + 1
            # if the rover is already at the eastern most point of the plateau,
            # the rover should not move any further east
            if from_x == plateau_width:
                now_x = plateau_width
            return now_x, from_y, from_facing
        if from_facing == 'S':
            # move the rover south (potentially)
            now_y = from_y - 1
            # if the rover is already at the southern most point of the plateau,
            # the rover should not move any further south
            if from_y == 0:
                now_y = 0
            return from_x, now_y, from_facing
        if from_facing == 'W':
            # move the rover west (potentially)
            now_x = from_x - 1
            # if the rover is already at the western most point of the plateau,
            # the rover should not move any further west
            if from_x == 0:
                now_x = 0
            return now_x, from_y, from_facing

    output_strings = []
    for rover in rovers:
        for instruction in rover['movement_instructions']:
            new_x, new_y, new_facing = get_new_position(
                rover['current_coordinates']['x'],
                rover['current_coordinates']['y'],
                rover['current_coordinates']['facing'],
                instruction,
            )
            # ========================================================
            # avoid a collision with another rover
            if (new_x, new_y) in [v for k, v in rover_current_positions.items() if k != rover['id']]:
                raise MoveRoversException('A potential collision has been avoided.')

            # ========================================================
            rover['current_coordinates']['x'] = new_x
            rover['current_coordinates']['y'] = new_y
            rover['current_coordinates']['facing'] = new_facing

            rover_current_positions[rover['id']] = (new_x, new_y)

        output_strings.append(f"{rover['current_coordinates']['x']} "
                              f"{rover['current_coordinates']['y']} "
                              f"{rover['current_coordinates']['facing']}")

    return '\n'.join(output_strings)


class RoverTests(unittest.TestCase):

    def test_correct_input(self):

        # this is the sample input and output data from the test
        input_string = """
        5 5
        1 2 N
        LMLMLMLMM
        3 3 E
        MMRMMRMRRM
        """
        expected_output = "1 3 N\n5 1 E"
        output = move_rovers(input_string)
        self.assertEqual(output, expected_output)

        # ==========================================================

        input_string = """
        12 8
        9 5 E
        MMLMLMMMRM
        2 5 E
        MMRMMRMRML
        """
        expected_output = "8 7 N\n3 4 W"
        output = move_rovers(input_string)
        self.assertEqual(output, expected_output)

    def test_incorrect_plateau_dimensions(self):

        input_string = """
        1A B7
        9 3 W
        MLMRLRM
        """
        try:
            move_rovers(input_string)
            self.fail()
        except MoveRoversException:
            pass

    def test_incorrect_line_count(self):

        input_string = """
        1A B7
        9 3 W
        MLMRLRM
        0 234
        """
        try:
            move_rovers(input_string)
            self.fail()
        except MoveRoversException:
            pass

    def test_rover_initial_position_should_not_be_outside_plateau(self):

        input_string = """
        5 5
        6 5 N
        MLMRLRM
        """
        try:
            move_rovers(input_string)
            self.fail()
        except MoveRoversException:
            pass

        # ==========================================================

        input_string = """
        5 5
        5 6 N
        MLMRLRM
        """
        try:
            move_rovers(input_string)
            self.fail()
        except MoveRoversException:
            pass

    def test_rover_tries_to_move_too_far_north(self):

        input_string = """
                5 5
                5 5 N
                MM
                """
        expected_output = "5 5 N"
        output = move_rovers(input_string)
        self.assertEqual(output, expected_output)

    def test_rover_tries_to_move_too_far_east(self):

        input_string = """
                5 5
                5 5 E
                MM
                """
        expected_output = "5 5 E"
        output = move_rovers(input_string)
        self.assertEqual(output, expected_output)

    def test_rover_tries_to_move_too_far_south(self):

        input_string = """
                5 5
                5 2 S
                MMMM
                """
        expected_output = "5 0 S"
        output = move_rovers(input_string)
        self.assertEqual(output, expected_output)

    def test_rover_tries_to_move_too_far_west(self):

        input_string = """
                5 5
                0 0 W
                MMMM
                """
        expected_output = "0 0 W"
        output = move_rovers(input_string)
        self.assertEqual(output, expected_output)

    def test_incorrect_movement_instructions(self):

        input_string = """
                5 5
                5 6 N
                MLMFAK@RLRM
                """
        try:
            move_rovers(input_string)
            self.fail()
        except MoveRoversException:
            pass

    def test_incorrect_facing(self):

        input_string = """
                5 5
                5 6 R
                MMMM
                """
        try:
            move_rovers(input_string)
            self.fail()
        except MoveRoversException:
            pass

    def test_collision_prevention(self):

        input_string = """
                5 5
                5 4 S
                M
                5 3 N
                M
                """
        try:
            move_rovers(input_string)
            self.fail()
        except MoveRoversException:
            pass


if __name__ == '__main__':
    unittest.main()
