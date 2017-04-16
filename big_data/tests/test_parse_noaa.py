import sys
sys.path.insert(0, '..')
import unittest
import parse_line
from parse_line import InvalidDoc
import pprint
pp = pprint.PrettyPrinter(indent = 4)

def _get_lines():
    with open('test_data/010010-99999-1995', 'r') as read_obj:
        lines = read_obj.readlines()
    return lines

lines = _get_lines()

class TestParseNoaa(unittest.TestCase):

    def test_parse_line_does_not_raise_error(self):
        pp.pprint(parse_line.parse_line(lines[0]))

    def test_line_is_valid_len_does_not_raise_error(self):
        parse_line.line_is_valid_len(lines[0])

    def test_line_is_valid_len_raises_error_with_short_line(self):
        self.assertRaises(InvalidDoc, parse_line.line_is_valid_len,
                lines[0][0:-2])


if __name__ == '__main__':
    unittest.main()
