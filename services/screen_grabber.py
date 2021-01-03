import numpy as np
from PIL import ImageGrab
import win32gui
import warnings
from datetime import datetime
from pathlib import Path
import os


def grab_screen(ignore_foreground_check=False, save_image=False):
    title, rect = find_window(ignore_foreground_check)
    if title is None:
        return

    image = ImageGrab.grab(rect)

    now = datetime.now()
    if save_image:
        save_path = os.getcwd() + '/files/'
        Path(save_path).mkdir(parents=False, exist_ok=True)
        image.save(f'{save_path}\\{now.isoformat().replace(":", "_")}.png')
    return np.array(image)


def find_window(ignore_foreground_check=False):
    window = win32gui.GetForegroundWindow()
    if window is None:
        warnings.warn('No foreground window found. Skipping execution.')
        return None, None

    title = win32gui.GetWindowText(window)
    if ignore_foreground_check is False and title != "Cyberpunk 2077 (C) 2020 by CD Projekt RED":
        warnings.warn('Cyberpunk is not the foreground window.  Skipping execution.')
        return None, None

    if window == 0:  # Can happen if you are in the 'ctrl alt del' screen
        return None, None

    rect = win32gui.GetWindowRect(window)
    return title, rect
