import unittest
import pprint
pp = pprint.PrettyPrinter(indent = 4)
import map_legends
from numpy import nan

class TestAdAddribution(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_2_colors_dataset_5_returns_right_list(self):
        data = [1, 2, 3, 4, 1]
        palette = ['blue', 'green']
        l = map_legends.make_legends(data, palette)
        needed = ['1: 2.5', '1: 2.5', '2.5: 4.0', '2.5: 4.0', '1: 2.5']
        self.assertEqual(needed, l)

    def test_3_colors_dataset_9_returns_right_list(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8,9]
        palette = ['blue', 'green', 'red']
        l  = map_legends.make_legends(data, palette)
        needed = [   '1: 3.7',
                '1: 3.7',
                '1: 3.7',
                '3.7: 6.3',
                '3.7: 6.3',
                '3.7: 6.3',
                '6.3: 9.0',
                '6.3: 9.0',
                '6.3: 9.0']
        self.assertEqual(needed, l)

    def test_nan(self):
        data = [1, 2, 3, 4, 5, 6, 7, nan, 8,9]
        palette = ['blue', 'green', 'red']
        l  = map_legends.make_legends(data, palette)
        needed = [   '1.0: 3.7',
                '1.0: 3.7',
                '1.0: 3.7',
                '3.7: 6.3',
                '3.7: 6.3',
                '3.7: 6.3',
                '6.3: 9.0',
                nan,
                '6.3: 9.0',
                '6.3: 9.0']
        self.assertEqual(needed, l)

    def test_nan_start(self):
        data = [nan, 1, 2, 3, 4, 5, 6, 7, nan, 8,9]
        palette = ['blue', 'green', 'red']
        l  = map_legends.make_legends(data, palette)
        needed = [   nan,
            '1.0: 3.7',
            '1.0: 3.7',
            '1.0: 3.7',
            '3.7: 6.3',
            '3.7: 6.3',
            '3.7: 6.3',
            '6.3: 9.0',
            nan,
            '6.3: 9.0',
            '6.3: 9.0']
        self.assertEqual(needed, l)

if __name__ == '__main__':
    unittest.main()
