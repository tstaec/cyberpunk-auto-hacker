import unittest

import numpy as np

from services.path_finder import find_path


class PathFinderTests(unittest.TestCase):
    def test_path_finder_finds_easy_path(self):
        array = [['1C', '7A'],
                 ['55', 'BD']]
        expected_path = [[0, 0], [0, 1], [1, 1]]
        actual_path = find_path(np.array(array), ['1C55BD'], 999)
        self.assertSequenceEqual(expected_path, actual_path)

    def test_path_finder_finds_surrounded_path(self):
        array = [['55', '55', '55'],
                 ['55', 'BD', '55'],
                 ['55', 'BD', '55']]
        expected_path = [[0, 0], [0, 2], [1, 2], [1, 1]]
        actual_path = find_path(np.array(array), ['BDBD'], 999)
        self.assertSequenceEqual(expected_path, actual_path)

    def test_path_finder_finds_path_full_image(self):
        array = [['55', '1C', '1C', '7A', '55', 'BD'],
                 ['7A', '7A', '1C', 'E9', 'E9', '1C'],
                 ['55', '1C', '1C', '55', 'BD', '7A'],
                 ['BD', '55', '55', '1C', '1C', '55'],
                 ['1C', '7A', 'E9', '7A', '7A', 'E9'],
                 ['7A', '1C', '55', '55', '1C', 'E9']]
        expected_path = [[3, 0], [3, 4], [1, 4], [1, 3]]
        actual_path = find_path(np.array(array), ['7A7A55'], 999)
        self.assertSequenceEqual(expected_path, actual_path)

    def test_path_finder_finds_multiple_sequences(self):
        array = [['55', '55', '55'],
                 ['55', 'BD', '55'],
                 ['55', 'BD', '55']]
        expected_path = [[0, 0], [0, 1], [1, 1], [1, 2], [0, 2]]
        actual_path = find_path(np.array(array), ['BDBD', 'BD55'], 5)
        self.assertSequenceEqual(expected_path, actual_path)

    def test_path_finder_finds_path_in_complex_image(self):
        array = [['1C', '7A', '1C', 'E9', '55', '1C'],
                 ['1C', 'E9', '7A', '1C', '1C', '55'],
                 ['55', '1C', '55', '1C', 'E9', '55'],
                 ['7A', '55', 'E9', 'BD', '7A', '1C'],
                 ['7A', '1C', '7A', '55', 'E9', '55'],
                 ['1C', 'BD', '55', '55', 'BD', '7A']]
        expected_path = [[0, 0], [0, 4], [3, 4], [3, 5], [1, 5], [1, 3], [0, 3], [0, 1], [2, 1], [2, 0]]
        actual_path = find_path(np.array(array), ['1C7A1C', 'BD557A1C', '7A5555BD'], 10)
        self.assertSequenceEqual(expected_path, actual_path)

    # test checks if a partial path that only solves one required sequence is returned and also if it prioritises
    # longer required sequences.
    def test_path_finder_finds_partial_path_in_complex_image(self):
        array = [['1C', '7A', '1C', 'E9', '55', '1C'],
                 ['1C', 'E9', '7A', '1C', '1C', '55'],
                 ['55', '1C', '55', '1C', 'E9', '55'],
                 ['7A', '55', 'E9', 'BD', '7A', '1C'],
                 ['7A', '1C', '7A', '55', 'E9', '55'],
                 ['1C', 'BD', '55', '55', 'BD', '7A']]
        expected_path = [[0, 0], [0, 4], [3, 4], [3, 5], [1, 5]]
        actual_path = find_path(np.array(array), ['1C7A1C', 'BD557A1C', '7A5555BD'], 5)
        self.assertSequenceEqual(expected_path, actual_path)

    def test_path_finder_ignores_already_used_nodes(self):
        array = [['1C', '7A'],
                 ['1C', 'E9']]
        actual_path = find_path(np.array(array), ['1C1CE97A1C'], 999)
        self.assertLess(len(actual_path), 5, 'There should not be a valid path for the required sequence')
