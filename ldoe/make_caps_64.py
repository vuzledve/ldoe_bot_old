# НАЧАЛО ИЗ СТАРТА ЛОКИ (только что нажата кнопка "войти")
# босиком/
# ВАЖНО: в настройках уже должна быть открыта кнопка "стереть данный"




#заметки по игре:
#`1 - в полицейский участок тащить узи и пулеметы(?)
# 2 - в красные дубы тащить 4 топора. на вышке валяется труп склад

from enum import Enum
import time
import sys
import win32gui
import numpy as np
import cv2
import math
import pyautogui
from matplotlib import pyplot as plt
import util
import cp_util as cp_u
import pytesseract
from PIL import Image, ImageEnhance

import datetime



#выставляем окно
util.set_ldoe_window(cp_u.LDOE_WINDOW_WIDTH, cp_u.LDOE_WINDOW_HEIGHT)


pyautogui.click(x=200, y=200) # фокус на окно

#cp_u.wait_for_smth(26, 102, 84, 24, cp_u.NICKNAME, True, 0, 0, 180, 140, 30, 255)  # ждем карты
# print(str(cp_u.getCapBalance()))


#while (True):
for cycle in range(99000):
    print("==========================")
    print("     КРУГ №" + str(cycle+1) + ". Время: " + str(datetime.datetime.now()))
    print("==========================")
    #TODO добавить защиту от вылетов (если вылет то в любом случае сброс прогресса игры?)

    bet_list = []

    if not cp_u.enter_car():                     # доходим до машины
        print ("не вошли в машину")
        cp_u.reload_ldoe()
        continue
    start_cycle_cap_balance = cp_u.getCapBalance()
    cp_u.seach_winning_bet(bet_list)     # находим выигрышные ставки

    #если весь список 1 элемент джека то находим сумму джека и забираем иначе:
    #if (len(bet_list) == 1 and bet_list[0] == cp_u.bet_result.JACK):
    if cp_u.bet_result.FAIL not in bet_list:
        if start_cycle_cap_balance < 30000: #если баланс маленький то ебемся с джеком
            cp_u.take_jack_full()
        else:   # если баланс большой то не ебемся и экономим время за 40 крышек
            cp_u.take_jack()
            cp_u.save_progress()

    else:
        isOK = False
        while (not isOK):   #если второй раз не совпал с первым

            entered_car = False
            while (not entered_car):
                cp_u.reload_ldoe()                   #очищаем прогресс
                entered_car = cp_u.enter_car()                     # доходим до машины

            start_cap_balance = cp_u.getCapBalance()

               #True - все прошло по плану #False - писок изменился
            isAllOk, win_bet_list = cp_u.win_caps(bet_list)

            if (isAllOk):
                end_cap_balance = cp_u.getCapBalance()

                cap_diff = end_cap_balance - start_cap_balance
                if cap_diff >= 0:
                    sign = "+"
                else:
                    sign = "-"

                print("ИТОГ ЗА КРУГ: " + str(start_cap_balance) + " -> " + str(end_cap_balance) + "  [" + sign + str(cap_diff) + "]")

                print("СЛЕДУЮЩИЙ ДЖЕК (не факт просто список закончился)")

                if (cap_diff >= -700):
                    cp_u.save_progress()
                    isOK = True
                else:
                    print ("cap_diff >= -700. требуется сохранитьяс вручную")
                    exit()
            else:
                print("начинаем заново с новым листом ставок...")
                bet_list = win_bet_list.copy()
