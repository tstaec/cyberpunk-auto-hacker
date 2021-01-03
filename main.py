from services.click_helper import execute_clicks
from services.ocr_helper import ocr_core
from services.path_finder import find_path
from services.screen_grabber import *
import time
import argparse

version_info = (1, 0, 0)
version = '.'.join(str(c) for c in version_info)

# interval_seconds = 2.0
# buffer_size = 5
# save_images = False

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--buffer',
                        '-b',
                        help='set the "buffer"(allowed code length) of the minigame',
                        required=True,
                        default=5,
                        type=int)
    parser.add_argument('--save_images',
                        '-s',
                        help='save the capture screen to execution path. Warning! this will fill up your drive very fast.',
                        default=False, action='store_true')
    parser.add_argument('--interval',
                        '-i',
                        help='set the interval in seconds in which the program captures the screen.',
                        default=2.0,
                        type=float)
    parser.add_argument('--version',
                        '-v',
                        help='show program version',
                        action='version',
                        version='cyberpunk-auto-hacker {}'.format(version))
    args = parser.parse_args()

    if args.buffer:
        buffer_size = args.buffer
    if args.save_images is not None:
        save_images = args.save_images
    if args.interval:
        interval_seconds = args.interval
    execute(buffer_size, save_images, interval_seconds)


def execute(buffer_size, save_images, interval_seconds):
    start_time = time.time()

    while True:
        image = grab_screen(ignore_foreground_check=False, save_image=save_images)
        if image is not None:
            print('screen grabbed. Processing...')
            matrix, required_sequences, offset_matrix_x, offset_matrix_y = ocr_core(image)
            print('Screen processed.')

            # check if we found a valid matrix of codes
            if matrix is not None and len(matrix) >= 5 and required_sequences is not None and len(
                    required_sequences) > 0:
                end_paths = []

                # reformat the required sequences
                for sequence in required_sequences:
                    end_paths.append(''.join([s.code for s in sequence]))

                path = find_path(np.array(matrix), end_paths, buffer_size)
                execute_clicks(matrix, path, offset_matrix_x, offset_matrix_y)
                print(path)
        time.sleep(interval_seconds - ((time.time() - start_time) % interval_seconds))


if __name__ == "__main__":
    main()
