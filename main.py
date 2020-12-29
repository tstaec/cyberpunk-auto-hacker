from services.ocr_helper import ocr_core
from services.path_finder import find_path
from services.screen_grabber import *
import time

start_time = time.time()
interval_seconds = 10.0
while True:
    image = grab_screen()
    if image is not None:
        print('screen grabbed. Processing...')
        matrix, required_sequences = ocr_core(image)
        print('Screen processed.')
        end_paths = []
        for sequence in required_sequences:
            end_paths.append(''.join(sequence))
        path = find_path(np.array(matrix), end_paths, 10)
        print(path)
    time.sleep(interval_seconds - ((time.time() - start_time) % interval_seconds))

