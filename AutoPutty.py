import subprocess
import pyautogui
import time
import psutil

# Baud Rate and com port to communicate with nrf52840 Device via USB
BAUD_RATE = '115200'
COM_PORT = 'COM10'  # Not guaranteed (Prompt user for COM port number?)

# folder position to append depending on development on home computer or work computer
WORK_FOLDER = 'work images/'
HOME_FOLDER = 'home images/'

# (x, y, width, height), used in "region" to narrow down search area.
PUTTY_WINDOW_WORK = (620, 200, 675, 675)
PUTTY_WINDOW_HOME = (660, 265, 600, 540)

# Sequence of image to search in putty
BASE_IMAGE_SEQUENCE = ['Keyboard.PNG'
                        , 'The Backspace key.PNG'
                        , 'The Function keys and keypad.PNG'
                        , 'Session.PNG'
                        , 'Connection type.PNG'
                        , 'Speed.PNG'
                        , 'Serial line.PNG']

# Create final image list with correct file path pre-appended
file_image_sequence = [(HOME_FOLDER + image) for image in BASE_IMAGE_SEQUENCE]


# Converts strings to array of characters
def word_to_list(word):
    return list(word)


# Much better error handling here. Don't want to accidentally spawn too many instances
# Searches for and kills any existing putty program
def check_kill_open_putty(process_name):
    for processes in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in processes.name().lower():
                processes.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    subprocess.Popen([r"C:\Program Files\PuTTY\putty.exe"])
    time.sleep(0.5)


check_kill_open_putty("Putty")

'''Configure putty'''
# error handling
s = time.time()

# put in func
for images in file_image_sequence:
    try:
        x, y = pyautogui.locateCenterOnScreen(images, region=PUTTY_WINDOW_HOME)
    except (RuntimeError, TypeError, NameError):
        print("could not find image")
    else:
        pyautogui.click(x, y)
        if images == 'home images/Speed.PNG':
            pyautogui.click(x, y)
            pyautogui.press(word_to_list(BAUD_RATE))
        elif images == 'home images/Serial line.PNG':
            pyautogui.click(x, y)
            pyautogui.press(word_to_list(COM_PORT))

e = time.time()
print(e - s)

pyautogui.press('enter')
# Error handling in case com port can't open
