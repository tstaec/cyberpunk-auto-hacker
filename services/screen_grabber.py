import numpy as np
from PIL import ImageGrab
import win32gui
import warnings


def grab_screen():
    title, rect = find_window()
    if title is None:
        return
    image = ImageGrab.grab(rect)
    #image.show()
    #input("Press Enter to continue...")
    return np.array(image)


def find_window():
    window = win32gui.GetForegroundWindow()
    if window is None:
        warnings.warn('No foreground window found. Aborting.')
        return None, None

    title = win32gui.GetWindowText(window)
    if title != "Cyberpunk 2077 (C) 2020 by CD Projekt RED":
        warnings.warn('Cyberpunk is not the foreground window. Aborting.')
        return None, None

    rect = win32gui.GetWindowRect(window)
    return title, rect
