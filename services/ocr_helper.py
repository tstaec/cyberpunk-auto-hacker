from pytesseract import Output

from services.image_helper import *
from services.models import OcrResult

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2

allowed_tuples = ('1C', '7A', '55', 'BD', 'E9')
allowed_characters = ('1', '7', '5', '9', 'A', 'B', 'C', 'D', 'E')


def ocr_core(image):
    code_matrix = cut_code_matrix(image)
    code_matrix_result = get_text_from_image(code_matrix)
    print(code_matrix_result)
    required_sequence = cut_required_sequence(image)
    required_sequence_result = get_text_from_image(required_sequence)
    print(required_sequence_result)
    return code_matrix_result, required_sequence_result


def parse_and_fix_result(text):
    text_array = []
    for line in text.splitlines():
        array_line = []
        for chars in line.split():
            array_line.append(fix_text(chars))
        if len(array_line) != 0:
            text_array.append(array_line)
    return text_array


def fix_text(chars):
    if chars in allowed_tuples:
        return chars
    elif len(chars) == 1:
        for allowed_tuple in allowed_tuples:
            if chars in allowed_tuple:
                return allowed_tuple
    else:
        try:
            # Filter the text to get rid of wrong characters and ensure the returned list is distinct
            filtered_text = "".join(list(set(filter(lambda ch: ch in allowed_characters, chars))))
        except RecursionError as re:
            print('RecursionError: ' + chars)
            raise
        return fix_text(filtered_text)
    return chars


def get_text_from_image(image):
    image = get_grayscale(image)
    image = thresholding(image)
    image = dilate(image)
    image = invert(image)
    #cv2.imshow("test", image)
    #cv2.waitKey(0)

    # Only characters that can occur are whitelisted. PSM = 6 because we want to retain the order of the text.
    custom_config = r"-c tessedit_char_whitelist=' ABCDEF1579' --psm 6"
    d = pytesseract.image_to_data(image, output_type=Output.DICT, config=custom_config)
    n_boxes = len(d['level'])
    result = []
    result_row = []
    for i in range(n_boxes):
        if d['text'][i] == '':
            if len(result_row) == 0:
                continue
            else:
                result.append(result_row)
                result_row = []

        text = fix_text(d['text'][i])
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        result_row.append(OcrResult(text, [x + w * 0.5, y + h * 0.5]))
    result.append(result_row)
    return result


def cut_code_matrix(image):
    height, width, color = image.shape
    return image[round(height * 0.32):round(height * 0.7), round(width*0.15):round(width*0.374)]


def cut_required_sequence(image):
    height, width, color = image.shape
    return image[round(height * 0.31):round(height * 0.5), round(width*0.43):round(width*0.55)]
