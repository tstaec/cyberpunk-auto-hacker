from pytesseract import Output
from services.image_helper import *
from services.models import OcrResult
import pytesseract

allowed_tuples = ('1C', '7A', '55', 'BD', 'E9', 'FF')
allowed_characters = ('1', '7', '5', '9', 'A', 'B', 'C', 'D', 'E')
# Only characters that can occur are whitelisted. PSM = 6 because we want to retain the order of the text.
custom_config = r"-c tessedit_char_whitelist=' ABCDEF1579' --psm 6"


def ocr_core(image):
    # Process the required sequences first because it is faster.
    required_sequence = cut_required_sequence(image)
    required_sequence_result = get_text_from_image(required_sequence)

    # If the required sequences could not be read skip the rest.
    if required_sequence_result is None or len(required_sequence_result) < 1:
        return None, None, None, None
    print([[e.code for e in row] for row in required_sequence_result])

    code_matrix, offset_matrix_x, offset_matrix_y = cut_code_matrix(image)
    code_matrix_result = get_text_from_image(code_matrix)

    if code_matrix_result is None or len(code_matrix_result) < 5:
        return None, None, None, None
    print([[e.code for e in row] for row in code_matrix_result])

    return code_matrix_result, required_sequence_result, offset_matrix_x, offset_matrix_y


# Tesseract has a lot of problems processing the Cyberpunk font. This tries to fix the returned text.
# It mainly uses the fact that the code matrix uses the same set of tuples.
def fix_text(chars):
    chars = chars.strip()
    try:
        if chars == '':
            return None

        # Check if we already have a valid tuple.
        if chars in allowed_tuples:
            return chars
        # If we only have on character try to find the correct tuple in the set of allowed tuples.
        # Since each tuple only uses distinct characters there can never be a collision.
        elif len(chars) == 1:
            for allowed_tuple in allowed_tuples:
                if chars in allowed_tuple:
                    return allowed_tuple
        else:
            # Filter the text to get rid of invalid characters and ensure the returned list is distinct.
            filtered_text = "".join(list(set(filter(lambda ch: ch in allowed_characters, chars))))
            # Retry with the cleaned list.
            if filtered_text != chars:
                return fix_text(filtered_text)
            print('Could not process chars: ' + chars)
            return chars
        return chars
    except RecursionError:
        return None


# Extract the textual data from the image.
def get_text_from_image(image):
    image = get_grayscale(image)
    image = thresholding(image)
    image = dilate(image)
    image = invert(image)
    # cv2.imshow("test", image)  # Use this to debug the cut images.
    # cv2.waitKey(0)

    print('Start OCR processing.')
    d = pytesseract.image_to_data(image, output_type=Output.DICT, config=custom_config)
    print('OCR processing finished.')

    found_lines = max(d['line_num'])
    max_word_count = max(d['word_num'])

    # Create an empty matrix to be filled later.
    result = [[OcrResult('', [-1, -1]) for _ in range(max_word_count)] for _ in range(found_lines)]

    for i in range(found_lines):
        row_indices = indices(d['line_num'], (i + 1))  # skip the first row
        avg_width = Average(list(d['width'][index] for index in row_indices))
        j = 0
        for index in row_indices:
            text = d['text'][index]
            if text == '':
                continue
            fixed_text = fix_text(text)
            if fixed_text is None:
                print(f'Could not fix tuple {text}. Aborting.')
                return None
            # Get the coordinates of the surrounding box for the found text to be used later to execute the clicks.
            (x, y, w, h) = (d['left'][index], d['top'][index], d['width'][index], d['height'][index])
            width = d['width'][index]
            # If the width of an element is several times the size of the average width,
            # this indicates that a tuple was skipped. We try to recreate the original position of the next elements.
            # So we can retry to find the missing tuple.
            if width // avg_width > 1:
                j += 1
            try:
                if j >= max_word_count or i >= found_lines:
                    print('Invalid matrix found. Aborting OCR processing.')
                    return None
                result[i][j] = OcrResult(fixed_text, [x + w * 0.5, y + h * 0.5])  # Get the middle of the bounding box
            except IndexError:
                raise
            j += 1

    fix_holes(result, image)
    return result


def Average(lst):
    return sum(lst) / len(lst)


# There could still be holes in the matrix(empty strings) that can be fixed by a second tesseract run.
def fix_holes(matrix, image):
    tolerance = 15
    for row in matrix:
        for element in row:
            if element.code == '':  # This indicates hole in the matrix
                element_column_index = row.index(element)
                column = np.array(matrix)[:, element_column_index]  # Get the column in which the hole exists.

                # Find an element in the column that was correctly processed and use it coordinate to calculate
                # the rectangle in the image where the missing tuple should be.
                for col_element in column:
                    if col_element.code != '':
                        # Find an element in the broken row to use its y boundaries for the new sub image.
                        element_index = row.index(element)
                        if element_index > 0:
                            element_index = 0
                        else:
                            element_index += 1
                        correct_row_element = row[element_index]
                        # Cut the existing image so we only get the area of the missing tuple.
                        new_cut = image[
                                  round(correct_row_element.position[1] - tolerance):round(
                                      correct_row_element.position[1] + tolerance),
                                  round(col_element.position[0] - tolerance):round(col_element.position[0] + tolerance)]
                        # Rerun tesseract with the new image, use image_to_string since we expect only a single word.
                        new_text = pytesseract.image_to_string(new_cut, config=custom_config).strip()
                        new_text = fix_text(new_text)
                        if new_text is None:
                            print(f'Could not fix tuple.')
                            return None
                        element.code = new_text
                        element.position = [col_element.position[0], correct_row_element.position[1]]
                        break


# We cut the original image to reduce distractions for tesseract.
# We try to get a simple smaller image that only contains the matrix we seek.
# Due to different screen resolution and code matrix sizes the margin are larger than normally necessary.
def cut_code_matrix(image):
    height, width, color = image.shape
    offset_matrix_y = round(height * 0.32)
    offset_matrix_x = round(width * 0.13)
    return image[offset_matrix_y:round(height * 0.75), offset_matrix_x:round(width * 0.374)], \
           offset_matrix_x, \
           offset_matrix_y


# We cut the original image to reduce distractions for tesseract.
# We try to get a simple smaller image that only contains the matrix we seek.
# Due to different screen resolution and code matrix sizes the margin are larger than normally necessary.
def cut_required_sequence(image):
    height, width, color = image.shape
    return image[round(height * 0.31):round(height * 0.5), round(width * 0.43):round(width * 0.56)]


# Helper function to return ALL indices for an element in a list.
def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset + 1)
        except ValueError:
            return result
        result.append(offset)
