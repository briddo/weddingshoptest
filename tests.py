
import unittest


def move_rovers(input_string):
    pass


class RoverTests(unittest.TestCase):

    def test_input_and_output(self):

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

        # ==========================================================


if __name__ == '__main__':
    unittest.main()
