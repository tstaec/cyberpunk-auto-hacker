import pyautogui

pyautogui.PAUSE = 1.0


def execute_clicks(targets):
    for target in targets:
        pyautogui.click(target.x, target.y)
