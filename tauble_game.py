import random
from typing import List, Any

import openpyxl
import time



bot_hand = []
player_hand = []
# прототип мешает колоду из 36 карт вставьте в первую скобку B, C, D, E,
coords = [["F", "G", "H", "I", "J", "K", "L", "M", "N"], ["2", "3", "4", "5"]]
strtable = " "
black_sheet = []
mixed_deck = []
counter = 1 # если не четное то ходит игрок иначе бот
"""Словарь мастей"""
change = {1: "♥", 2: "♠", 3: "♦", 4: "♣"}

def queue(counter):
    if counter % 2 == 0:
        who = bot_hand
        return who
    else:
        who = player_hand
        return who

"""Вывод данных в консоль"""

def output(bot_hand, player_hand, strtable):

    print("\nв руке бота:", len(bot_hand), "карты")
    print("\nв твоей руке:", player_hand)
    print("\nна столе лежит:", strtable, "\n")


"""фун. тасования колоды"""

def withdraw():
    while True:
        randcard = coords[0][random.randint(0, 8)]
        randsuit = coords[1][random.randint(0, 3)]
        suit_card = randcard + randsuit
        # print(suit_card) ♣ ♦ ♠ ♥
        # print(black_sheet)
        # проверка на то доставалась ли такая карта раньше
        if suit_card in black_sheet:
            continue
        else:
            black_sheet.append(suit_card)
            wb = openpyxl.reader.excel.load_workbook(filename="Deckcard.xlsx")
            ws = wb.active
            withdrawn_card = ws[suit_card].value
            return withdrawn_card
            break
#

"""Фун. смены масти"""


def suit_change(otvet):
    global strtable
    strtable = strtable.replace(strtable[-1], change[otvet])





# print(len(coord[0]) * len(coord[1]))
"""Фун доавления карт в чьюто руку"""


def take_card(who, kol):
    i = 0
    while i < kol:
        who.append(mixed_deck.pop(0))
        i += 1


"""Словарь функций карт и их определение"""


def init_card(card, who):
    if card == 'A':
        global counter
        if queue(counter) == bot_hand:
            print("Ходите еще раз")
        else:
            print("Бот ходит еще раз")
        counter -= 1
    elif card == 'Q':
        print("меняет масть")
        while True:
            otvet = int(input("выберите новую масть 1 = ♥ 2 = ♠ 3 = ♦ 4 = ♣\n"))
            if otvet <= 4:
                suit_change(otvet)
                break
            else:
                print("неправильный выбор")
                continue

    elif card == '9':
        pass
    elif card == '7':
        if who == bot_hand:
            print("Бот берет 2 карты")
            take_card(who, 2)
        else:
            print("Вы берете 2 карты")
            take_card(who, 2)
    elif card == '6':
        if who == bot_hand:
            print("Бот берет 1 карту")
            take_card(who, 1)
        else:
            print("Вы берете 1 карту")
            take_card(who, 1)
    else:
        pass


"""Ход бота"""

def bot_move(bot_hand):
    print("Бот ходит")
    matching_сards = [ ]
    i = 0
    global strtable
    global counter
    counter += 1
    while i < 2:
        for card in bot_hand:
            if card[0] == "Q":

                matching_сards.append(card)
                print("он кладет карут на стол")
                strtable = bot_hand.pop(bot_hand.index(card))
                print("меняет масть")
                otvet = random.randint(1, 4)
                suit_change(otvet)

                return strtable
            elif card[0] == strtable[0] or card[-1] == strtable[-1]:
                matching_сards.append(card)

        if len(matching_сards) == 0 and i == 1:
            print("он ненашел подходящей карты")
            break
        elif len(matching_сards) == 0:
            print("он берет карту")
            take_card(bot_hand, 1)
            i += 1
            continue
        else:
            for card in bot_hand:
                if card in matching_сards:
                    strtable = bot_hand.pop(bot_hand.index(card))
                    init_card(card[0], player_hand)
                    print("он кладет карут на стол")
                    break
            break


"""Функция хода игрока"""


def player_move(player_hand):
    i = 0
    global strtable
    global counter
    counter += 1
    # global strtable
    while i < 2:
        # print(table[0])

        otvet = input("вам есть чем ходить ?: да = 1 нет = 2\n")

        if otvet == "1":
            numcard = int(input("№:")) - 1
            card = str(player_hand[numcard])

            if numcard > len(player_hand):
                print("\nТакого номера нет")
                continue
            elif card[0] == strtable[0] or card[-1] == strtable[-1] or card[0] == "Q":

                strtable = str(player_hand.pop(numcard))
                init_card(card[0], bot_hand)
                # return strtable
                break
            else:
                print("Этой картой ходить нельзя!")
                continue
        elif otvet != 1 and i == 1:
            break
        else:
            take_card(player_hand, 1)
            print(player_hand)
            i += 1
            continue



"""Добавление карт в колоду"""
p = 0
while p < len(coords[0]) * len(coords[1]):
    mixed_deck.append(withdraw())
    p += 1

"""Раздача первых рук и первй ход"""
for i in range(1, 10):
    if i < 4:
        bot_hand.append(mixed_deck.pop(0))
        #   print(mixed_deck)
    elif 4 < i < 9:
        player_hand.append(mixed_deck.pop(0))
    if i == 9:
        strtable = str(mixed_deck.pop(0))

"""основной цикл"""

while counter > 0:
    if len(player_hand) == 0:
        print("\nВЫ ВЫИГРАЛИ")
        quit()
    elif len(bot_hand) == 0:
        print("\nВЫ ПРОИГРАЛИ")
        quit()
    else:
        if queue(counter) == bot_hand:
            output(bot_hand, player_hand, strtable)
            bot_move(bot_hand)
        else:
            output(bot_hand, player_hand, strtable)
            player_move(player_hand)

