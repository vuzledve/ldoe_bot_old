from pynput.keyboard import Key, Listener
import time
import pyautogui

#time.sleep (3.0709066390991211)
pyautogui.keyDown('e')			#2.0560266971588135

#time.sleep (0.0709066390991211)
#pyautogui.keyUp('e')			#2.1269333362579346

#time.sleep (13.432542562484741)
time.sleep (1.432542562484741)
pyautogui.keyDown('d' + 'w')			#15.559475898742676
time.sleep (4.432542562484741)
pyautogui.keyDown('s')			#15.57608699798584e
start = time.time()


pyautogui.keyUp('s')
print (str(time.time() - start))
time.sleep (2.68076467514038)
pyautogui.keyUp('d')			#18.544163465499878

time.sleep (0.0)
pyautogui.keyUp('s')			#18.544163465499878
