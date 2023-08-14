from pynput.keyboard import Key, Listener
import logging
import time

logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format="%(message)s")

#нужно чтобы сразу писало код чтобы потом ctrl +c ctrl +v
def on_press(key):
    global last_move_time
    global keysPressed

    KEY = str(key)
    if KEY == 'Key.space':
        KEY = "'space'"

    if KEY in keysPressed:
        if keysPressed[KEY]:
            return

    keysPressed[KEY] = True

   # print(keysPressed)

    end = time.time()
    logging.info("\ntime.sleep ("+ str((end - last_move_time))+")" + "\n" + "pyautogui.keyDown("+KEY+")\t\t\t#"+str((end - start)))
    last_move_time = end
#ddfd
def on_up(key):
    print("key up " + str(key))

    global last_move_time
    global keysPressed

    KEY = str(key)
    if KEY == 'Key.space':
        KEY = "'space'"

    keysPressed[KEY] = False

    end = time.time()
    logging.info("\ntime.sleep ("+ str((end - last_move_time))+")" + "\n" + "pyautogui.keyUp("+KEY+")\t\t\t#"+str((end - start)))
    last_move_time = end


start = time.time()
last_move_time = start
keysPressed = {}

with open('keylog.txt', 'wb'):
    pass

with Listener(on_release=on_up, on_press=on_press) as listener:
    listener.join()

#УБЕДИСЬ ЧТО РАСКЛАДКА АНГЛИЙСКАЯ

#wwwwwwwwwwwwwwwwwwwwwwww