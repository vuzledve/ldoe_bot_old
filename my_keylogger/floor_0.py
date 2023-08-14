from pynput.keyboard import Key, Listener
import time
import pyautogui

def right(sleep_time):
    pyautogui.keyDown('d')
    pyautogui.keyDown('w')
    time.sleep(sleep_time)
    pyautogui.keyUp('d')
    pyautogui.keyUp('w')

def left(sleep_time):
    pyautogui.keyDown('s')
    pyautogui.keyDown('a')
    time.sleep(sleep_time)
    pyautogui.keyUp('s')
    pyautogui.keyUp('a')

def up(sleep_time):
    pyautogui.keyDown('w')
    pyautogui.keyDown('a')
    time.sleep(sleep_time)
    pyautogui.keyUp('w')
    pyautogui.keyUp('a')

def down(sleep_time):
    pyautogui.keyDown('s')
    pyautogui.keyDown('d')
    time.sleep(sleep_time)
    pyautogui.keyUp('s')
    pyautogui.keyUp('d')

def attack():
    pyautogui.keyDown('space')
    pyautogui.keyUp('space')

def sleep(sleep_time):
    time.sleep (sleep_time)


sleep (4.0)

down(0.9)
right(0.6)
pyautogui.press('e')
sleep(1)
right(0.2)
down(2)
up(1.87)
left(0.23)

sleep(4)

for x in range(6):
  right(0.04)
  attack()
  left(0.04)
  sleep(0.5)
