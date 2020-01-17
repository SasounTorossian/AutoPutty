import subprocess
import pyautogui
import time
import psutil

# NOTE: When taken to new monitor/laptop, need to retake pictures

BAUD_RATE = '115200'                        # Required baud rate to communicate with device
COM_PORT = 'COM10'                          # Expected com port device will appear on. Not guaranteed (Prompt user for COM port number?)
PUTTY_WINDOW_X_Y = (620, 200, 675, 675)     # (x, y, width, height), used in "region" to narrow down search area.
IMAGE_SEQUENCE = ('Keyboard.PNG'
                  , 'The Backspace key.PNG'
                  , 'The Function keys and keypad.PNG'
                  , 'Session.PNG'
                  , 'Connection type.PNG'
                  , 'Speed.PNG'
                  , 'Serial line.PNG')      # Sequence of image to search in putty


# Converts strings to array of characters
def word_to_list(word):
    return list(word)


# Much better error handling here. Don't want to accidentally spawn too many instances
def check_and_kill_process(process_name):
    for processes in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in processes.name().lower():
                processes.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


'''Open Putty'''
# Searches for and kills any existing putty program
check_and_kill_process("Putty")
subprocess.Popen([r"C:\Program Files\PuTTY\putty.exe"])
time.sleep(0.5)

'''Configure putty'''
# error handling
s = time.time()

for images in IMAGE_SEQUENCE:
    try:
        x, y = pyautogui.locateCenterOnScreen(images, region=PUTTY_WINDOW_X_Y)
    except (RuntimeError, TypeError, NameError):
        print("could not find image")
    else:
        pyautogui.click(x, y)
        if images == 'Speed.PNG':
            pyautogui.click(x, y)
            pyautogui.press(word_to_list(BAUD_RATE))
        elif images == 'Serial line.PNG':
            pyautogui.click(x, y)
            pyautogui.press(word_to_list(COM_PORT))


e = time.time()
print(e - s)

pyautogui.press('enter')
# Error handling in case com port can't open
