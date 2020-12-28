from services.image_helper import *

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2

allowed_tuples = ('1C', '7A', '55', 'BD', 'E9')
allowed_characters = ('1', '7', '5', 'A', 'B', 'C', 'D', 'E')


def ocr_core(filename):

    image = cv2.imread(filename)
    code_matrix = cut_code_matrix(image)
    code_matrix_text = get_text_from_image(code_matrix)

    required_sequence = cut_required_sequence(image)
    required_sequence_text = get_text_from_image(required_sequence)

    return parse_and_fix_result(code_matrix_text), parse_and_fix_result(required_sequence_text)


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
        # Filter the text to get rid of wrong characters and ensure the returned list is distinct
        filtered_text = "".join(list(set(filter(lambda ch: ch in allowed_characters, chars))))
        return fix_text(filtered_text)
    return chars



def get_text_from_image(image):
    image = get_grayscale(image)
    image = thresholding(image)
    image = dilate(image)
    image = invert(image)
    #cv2.imshow("test", image)
    #cv2.waitKey(0)

    custom_config = r"-c tessedit_char_whitelist=' ABCDEF123456789' --psm 6"
    text = pytesseract.image_to_string(image, config=custom_config)
    return text


def cut_code_matrix(image):
    height, width, color = image.shape
    return image[round(height * 0.32):round(height * 0.7), round(width*0.15):round(width*0.374)]


def cut_required_sequence(image):
    height, width, color = image.shape
    return image[round(height * 0.31):round(height * 0.5), round(width*0.45):round(width*0.55)]
