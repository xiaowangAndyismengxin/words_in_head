import os
import random
import colorama
from tabulate import tabulate
from colorama import Fore, Cursor
import pyttsx3
import sys
import platform


def clear_input_buffer():
    """清除标准输入缓冲区中的残留数据"""
    system = platform.system()
    if system == 'Windows':
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        import select
        while select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()


voice = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'
engine = pyttsx3.init()
engine.setProperty('voice', voice)

engine.setProperty('rate', 130)
colorama.init()


def speak(text: str):
    global engine
    engine.say(text)
    engine.runAndWait()


def clear():
    os.system('cls')


def process_section(section_data: list, section_type: str, key_type: str,
                    learning: bool, other_wrong_count: int=0):
    wrong_list = []
    words = section_data.copy()
    random.shuffle(words)
    left_words = len(words)

    for word in words:
        passed = True
        last_wrong_input = ''
        while True:
            clear()
            print(f'--{section_type}--  ', f'剩下: {left_words}'
                                           f' 错: {len(wrong_list)
                                                   + other_wrong_count}\n\n\n')

            if not passed:
                print('That is wrong: ' + Fore.RED + last_wrong_input
                      + Fore.RESET)

            if learning or not passed:
                print(tabulate([word], headers='keys'))
                speak(word[key_type])
                clear_input_buffer()
                input('按回车继续')
                clear()
                print(f'--{section_type}--  ', f'剩下: {left_words}'
                                               f' 错: {len(wrong_list)
                                                       + other_wrong_count}\n\n\n')

            user_input_tip = f"{word.get('part_of_speech', '')}{word['meaning']}: "
            clear_input_buffer()
            user_input = input(user_input_tip).strip()
            if user_input == word[key_type]:
                print(f'{Cursor.UP(1)}\r{user_input_tip}{Fore.GREEN}{user_input}'
                      f'{Fore.RESET} {word.get('phonetic_symbol', '')}', ' ' * 50)
                speak(user_input)
                clear()
                left_words -= 1
                break

            if passed:
                wrong_list.append(word)
                passed = False

            last_wrong_input = user_input
            clear()

    return wrong_list


def fast_view_once(unit_data: dict, learning: bool = True) -> dict:
    clear()
    data = unit_data

    wrong_words = process_section(
        data['words'], 'words', 'word', learning,
        other_wrong_count=0
    )
    wrong_phrases = process_section(
        data['phrases'], 'phrases', 'phrase', learning,
        other_wrong_count=len(wrong_words)
    )

    clear()
    return {'words': wrong_words, 'phrases': wrong_phrases}


def fast_view(unit_data: dict, learning: bool = True):
    wrong_data = fast_view_once(unit_data, learning=learning)
    while wrong_data['words'] or wrong_data['phrases']:
        wrong_data = fast_view_once(wrong_data, learning=learning)
