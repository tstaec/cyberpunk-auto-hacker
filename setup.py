import PyInstaller.__main__

#pyinstaller --onefile main.py --clean -n cyberpunk-auto-hacker
# The Tesseract-OCR folder needs to be on the application level

PyInstaller.__main__.run([
    'main.py',
    '--onedir',
    '--clean',
    '-n cyberpunk-auto-hacker',  # This stupid shit adds the whitespace to the name. So execute it in terminal for now..
    '--add-data README.md;LICENSE'
])
