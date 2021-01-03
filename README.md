# cyberpunk-auto-hacker

Script to automatically detect and solve the hacking minigame in Cyberpunk 2077.

## What it does

![Hack the planet](https://imgur.com/a/7X9X5Mq)

## Running auto-hacker

* Download the latest release and unpack
* Open a powershell window where you unpacked the files
* Run: ".\cyberpunk-auto-hacker.exe --buffer X" Where X ist the buffer size()
** For further options run '.\cyberpunk-auto-hacker.exe --help'

## How it works

1. grab a screenshot from the active window on the main screen
2. Extract the code matrix and the list of required sequences with [tesseract](https://github.com/tesseract-ocr/tesseract)
3. Find a path that solves all or most of the required sequences
4. Simulate clicks on the path nodes

## Problems

* tesseract can have problems detecting the code tuples. These are normally only one or two tuples per code matrix which doesn't affect the result much. Otherwise simply reopening the hacking window should suffice.
* If the mouse cursor is on one of the code matrices OCR is impossible. Ensure that the cursor is in a neutral location.

## Please contribute

This was written as an exercise for python and OCR. Feel free to point out mistakes or possible code improvements.
Or do it yourself and fork and PR.

## Additional infos

Change pytesseract.py in you venv in case it doenst find tesseract on windows https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i/53672281#:~:text=On%20Windows%2064%20bits%2C%20just,OCR"%20and%20it%20will%20work.&text=This%20error%20is%20because%20tesseract%20is%20not%20installed%20on%20your%20computer.&text=I%20had%20the%20same%20issue,tesseract%20which%20did%20not%20work.