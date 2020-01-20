import subprocess
import pyautogui
import time
import psutil
import pyperclip

# Baud Rate and com port to communicate with nrf52840 Device via USB. Might not be needed.
BAUD_RATE = '115200'
COM_PORT = 'COM10'  # Not guaranteed (Prompt user for COM port number?)

# Putty configure
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
CTRL = 'ctrl'
SHIFT = 'shift'
TAB = 'tab'
ENTER = 'enter'
PUTTY_COMMAND_LIST = [TAB, TAB, TAB, TAB, DOWN, DOWN, ENTER]

# BDB setup commands
BDB_CHANNEL = 'bdb channel 16'
BDB_ROLE = 'bdb role zc'
BDB_START = 'bdb start'
BDB_COMMAND_LIST = [BDB_CHANNEL, ENTER, BDB_ROLE, ENTER, BDB_START, ENTER]

# ZDO commands
ZDO_MATCH_DESC = 'zdo match_desc 0xfffd 0xfffd 0x0104 1 0 0'
ZDO_COMMAND_LIST = [ZDO_MATCH_DESC]

# Fake match_desc response
# MATCH_DESC_RESP_1 = 'src_addr=29D5 ep=10'
# MATCH_DESC_RESP_2 = 'src_addr=123F ep=1'
# MATCH_DESC_RESP_3 = 'src_addr=8EC1 ep=10'
# MATCH_DESC_RESP_LIST = [MATCH_DESC_RESP_1, MATCH_DESC_RESP_2, MATCH_DESC_RESP_3]


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


s = time.time()

# Open and configure Putty
check_kill_open_putty("Putty")

time.sleep(0.2
           )
for commands in PUTTY_COMMAND_LIST:
    pyautogui.press(commands)

# pyautogui.press(ENTER)  # Get's rid of error message during testing.

# Configure CLI device as coordinator
time.sleep(0.2)
for commands in BDB_COMMAND_LIST:
    pyautogui.press(commands if commands == ENTER else word_to_list(commands))

time.sleep(5)  # Need to wait until connection established with all devices
for commands in ZDO_COMMAND_LIST:
    pyautogui.press(word_to_list(commands))
    pyautogui.press(ENTER)

''' if failure = sending broadcast request (wait and resend?)(reset command)
    if success = src_addr (triple click)(ctrl+c)(paste in code)
    > src_addr=9826 ep=10 (do some regex magic) to find number.
'''

e = time.time()
print(e - s)