import unittest

import numpy as np

from services.path_finder import find_path
from services.models import OcrResult


def create_object_matrix_from_str_matrix(matrix):
    obj_matrix = []
    for row in matrix:
        new_row = []
        for element in row:
            new_row.append(OcrResult(element, None))
        obj_matrix.append(new_row)
    return obj_matrix


class PathFinderTests(unittest.TestCase):
    def test_path_finder_finds_easy_path(self):
        matrix = create_object_matrix_from_str_matrix([['1C', '7A'],
                                                      ['55', 'BD']])
        required_sequences = ['1C55BD']
        actual_path = find_path(np.array(matrix), required_sequences, 999)
        self.assertTrue(self.path_completes_required(matrix, required_sequences, actual_path))

    def test_path_finder_finds_surrounded_path(self):
        matrix = create_object_matrix_from_str_matrix([['55', '55', '55'],
                                                      ['55', 'BD', '55'],
                                                      ['55', 'BD', '55']])
        required_sequences = ['BDBD']
        actual_path = find_path(np.array(matrix), required_sequences, 999)
        self.assertTrue(self.path_completes_required(matrix, required_sequences, actual_path))

    def test_path_finder_finds_path_full_image(self):
        matrix = create_object_matrix_from_str_matrix([['55', '1C', '1C', '7A', '55', 'BD'],
                                                      ['7A', '7A', '1C', 'E9', 'E9', '1C'],
                                                      ['55', '1C', '1C', '55', 'BD', '7A'],
                                                      ['BD', '55', '55', '1C', '1C', '55'],
                                                      ['1C', '7A', 'E9', '7A', '7A', 'E9'],
                                                      ['7A', '1C', '55', '55', '1C', 'E9']])
        required_sequences = ['7A7A55']
        actual_path = find_path(np.array(matrix), required_sequences, 999)
        self.assertTrue(self.path_completes_required(matrix, required_sequences, actual_path))

    def test_path_finder_finds_multiple_sequences(self):
        matrix = create_object_matrix_from_str_matrix([['55', '55', '55'],
                                                      ['55', 'BD', '55'],
                                                      ['55', 'BD', '55']])
        required_sequences = ['BDBD', 'BD55']
        actual_path = find_path(np.array(matrix), required_sequences, 5)
        self.assertTrue(self.path_completes_required(matrix, required_sequences, actual_path))

    def test_path_finder_finds_path_in_complex_image(self):
        matrix = create_object_matrix_from_str_matrix([['1C', '7A', '1C', 'E9', '55', '1C'],
                                                      ['1C', 'E9', '7A', '1C', '1C', '55'],
                                                      ['55', '1C', '55', '1C', 'E9', '55'],
                                                      ['7A', '55', 'E9', 'BD', '7A', '1C'],
                                                      ['7A', '1C', '7A', '55', 'E9', '55'],
                                                      ['1C', 'BD', '55', '55', 'BD', '7A']])
        required_sequences = ['1C7A1C', 'BD557A1C', '7A5555BD']
        actual_path = find_path(np.array(matrix), required_sequences, 10)
        self.assertTrue(self.path_completes_required(matrix, required_sequences, actual_path))

    # test checks if a partial path that only solves one required sequence is returned and also if it prioritises
    # longer required sequences.
    def test_path_finder_finds_partial_path_in_complex_image(self):
        matrix = create_object_matrix_from_str_matrix([['1C', '7A', '1C', 'E9', '55', '1C'],
                                                       ['1C', 'E9', '7A', '1C', '1C', '55'],
                                                       ['55', '1C', '55', '1C', 'E9', '55'],
                                                       ['7A', '55', 'E9', 'BD', '7A', '1C'],
                                                       ['7A', '1C', '7A', '55', 'E9', '55'],
                                                       ['1C', 'BD', '55', '55', 'BD', '7A']])
        required_sequences = ['1C7A1C', 'BD557A1C', '7A5555BD']
        actual_path = find_path(np.array(matrix), required_sequences, 5)
        self.assertFalse(self.path_completes_required(matrix, [required_sequences[0]], actual_path))
        self.assertFalse(self.path_completes_required(matrix, [required_sequences[1]], actual_path))
        self.assertTrue(self.path_completes_required(matrix, [required_sequences[2]], actual_path))

    def test_path_finder_ignores_already_used_nodes(self):
        array = create_object_matrix_from_str_matrix([['1C', '7A'],
                                                      ['1C', 'E9']])
        actual_path = find_path(np.array(array), ['1C1CE97A1C'], 999)
        self.assertLess(len(actual_path), 5, 'There should not be a valid path for the required sequence')

    @staticmethod
    def path_completes_required(matrix, required_sequences, actual_path):
        mapped_targets = []
        for target in actual_path:
            mapped_targets.append(matrix[target[1]][target[0]])
        actual_joined_path = ''.join([e.code for e in mapped_targets])

        for sequence in required_sequences:
            if sequence not in actual_joined_path:
                return False
        return True
