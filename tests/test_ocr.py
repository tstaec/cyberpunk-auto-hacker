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
        returned_array, _ = ocr_core(cv2.imread('..\\tests\\images\\full_image.png'))
        self.assertSequenceEqual(expected_array, returned_array)

    def test_ocr_helper_finds_required_sequence(self):
        expected_array = [['7A', '7A', '55']]
        _, returned_array = ocr_core(cv2.imread('..\\tests\\images\\full_image.png'))
        print(returned_array)
        self.assertSequenceEqual(expected_array, returned_array)

    def test_ocr_helper_finds_code_matrix_in_complex_image(self):
        expected_array = [['1C', '7A', '1C', 'E9', '55', '1C'],
                          ['1C', 'E9', '7A', '1C', '1C', '55'],
                          ['55', '1C', '55', '1C', 'E9', '55'],
                          ['7A', '55', 'E9', 'BD', '7A', '1C'],
                          ['7A', '1C', '7A', '55', 'E9', '55'],
                          ['1C', 'BD', '55', '55', 'BD', '7A']]
        returned_array, _ = ocr_core(cv2.imread('..\\tests\\images\\full_image_complex.png'))
        print(returned_array)
        self.assertSequenceEqual(expected_array, returned_array)

    def test_ocr_helper_finds_required_sequence_in_complex_image(self):
        expected_array = [['1C', '7A', '1C'], ['BD', '55', '7A', '1C'], ['7A', '55', '55', 'BD']]
        _, returned_array = ocr_core(cv2.imread('..\\tests\\images\\full_image_complex.png'))
        print(returned_array)
        self.assertSequenceEqual(expected_array, returned_array)

