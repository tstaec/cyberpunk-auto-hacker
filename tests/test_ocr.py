import unittest
from services.ocr_helper import *


class OcrHelperTests(unittest.TestCase):

    def test_ocr_helper_finds_code_matrix(self):
        expected_array = [['55', '1C', '1C', '7A', '55', 'BD'],
                          ['7A', '7A', '1C', 'E9', 'E9', '1C'],
                          ['55', '1C', '1C', '55', 'BD', '7A'],
                          ['BD', '55', '55', '1C', '1C', '55'],
                          ['1C', '7A', 'E9', '7A', '7A', 'E9'],
                          ['7A', '1C', '55', '55', '1C', 'E9']]
        returned_array, _, _, _ = ocr_core(cv2.imread('..\\tests\\images\\full_image.png'))
        self.assertSequenceEqual(expected_array, [[e.code for e in row] for row in returned_array])

    def test_ocr_helper_finds_required_sequence(self):
        expected_array = [['7A', '7A', '55']]
        _, returned_array, _, _ = ocr_core(cv2.imread('..\\tests\\images\\full_image.png'))
        print(returned_array)
        self.assertSequenceEqual(expected_array, [[e.code for e in row] for row in returned_array])

    def test_ocr_helper_finds_code_matrix_in_complex_image(self):
        expected_array = [['1C', '7A', '1C', 'E9', '55', '1C'],
                          ['1C', 'E9', '7A', '1C', '1C', '55'],
                          ['55', '1C', '55', '1C', 'E9', '55'],
                          ['7A', '55', 'E9', 'BD', '7A', '1C'],
                          ['7A', '1C', '7A', '55', 'E9', '55'],
                          ['1C', 'BD', '55', '55', 'BD', '7A']]
        returned_array, _, _, _ = ocr_core(cv2.imread('..\\tests\\images\\full_image_complex.png'))
        print(returned_array)
        self.assertSequenceEqual(expected_array, [[e.code for e in row] for row in returned_array])

    def test_ocr_helper_finds_required_sequence_in_complex_image(self):
        expected_array = [['1C', '7A', '1C', ''], ['BD', '55', '7A', '1C'], ['7A', '55', '55', 'BD']]
        _, returned_array, _, _ = ocr_core(cv2.imread('..\\tests\\images\\full_image_complex.png'))
        print(returned_array)
        self.assertSequenceEqual(expected_array, [[e.code for e in row] for row in returned_array])

    def test_ocr_helper_finds_missing_tuple(self):
        expected_array = [['55', 'BD', '55', '55', '55'],
                          ['BD', 'E9', 'E9', 'E9', '55'],
                          ['E9', 'E9', 'BD', '1C', 'E9'],
                          ['55', '55', '1C', 'BD', '55'],
                          ['1C', '1C', '1C', '1C', '1C']]
        returned_array, _, _, _ = ocr_core(cv2.imread('..\\tests\\images\\full_image_missing_tuple.png'))
        print([[e.code for e in row] for row in returned_array])
        self.assertSequenceEqual(expected_array, [[e.code for e in row] for row in returned_array])

    def test_ocr_helper_finds_required_sequence_in_seven_row_file(self):
        expected_array = [['BD', 'E9', '1C', ''],
                          ['1C', '55', '1C', ''],
                          ['BD', '1C', '55', '55']]
        _, returned_array, _, _ = ocr_core(cv2.imread('..\\tests\\images\\full_image_extra_large.png'))
        print([[e.code for e in row] for row in returned_array])
        self.assertSequenceEqual(expected_array, [[e.code for e in row] for row in returned_array])

    def test_ocr_helper_finds_code_matrix_in_seven_row_file(self):
        expected_array = [['7A', '55', 'BD', '1C', 'FF', 'E9', '7A'],
                          ['BD', '7A', '55', '1C', '1C', 'E9', 'BD'],
                          ['1C', '1C', '1C', '55', '1C', '7A', 'E9'],
                          ['BD', '7A', '1C', '7A', '7A', 'E9', 'FF'],
                          ['55', '55', '55', '55', 'E9', '1C', '1C'],
                          ['BD', '7A', 'E9', '7A', '7A', 'E9', '1C'],
                          ['BD', '1C', '55', '7A', 'E9', 'FF', 'BD']]
        returned_array, _, _, _ = ocr_core(cv2.imread('..\\tests\\images\\full_image_extra_large.png'))
        print([[e.code for e in row] for row in returned_array])
        self.assertSequenceEqual(expected_array, [[e.code for e in row] for row in returned_array])

