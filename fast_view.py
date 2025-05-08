import os
import random
import colorama
from tabulate import tabulate
from colorama import Fore, Cursor
import pyttsx3
import sys
import platform

USER_SYSTEM_TYPE = platform.system()


def clear_input_buffer():
    """清除标准输入缓冲区中的残留数据"""
    if USER_SYSTEM_TYPE == 'Windows':
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
    if USER_SYSTEM_TYPE == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def process_section(section_data: list, section_type: str, key_type: str,
                    learning: bool, other_wrong_count: int = 0, other_args: dict | None = None):

    other_args = other_args or dict()

    # import args from other_args
    first_letter_tip = other_args.get('first_letter_tip', False)

    wrong_list = []
    words = section_data.copy()
    random.shuffle(words)
    left_words = len(words)

    first_letter: str

    for word in words:
        passed = True
        last_wrong_input = ''
        while True:
            clear()

            # print header
            print(f'--{section_type}--  ', f'剩下: {left_words}'
                                           f' 错: {len(wrong_list)
                                                  + other_wrong_count}\n\n\n')
            # wrong word header
            if not passed:
                print('That is wrong: ' + Fore.RED + last_wrong_input
                      + Fore.RESET)

            # print word tip
            if learning or not passed:
                print(tabulate([word], headers='keys'))
                speak(word[key_type])
                clear_input_buffer()
                input('按回车继续')
                clear()
                print(f'--{section_type}--  ', f'剩下: {left_words}'
                                               f' 错: {len(wrong_list)
                                                      + other_wrong_count}\n\n\n')

            # handle user input
            first_letter = word[key_type][0] if first_letter_tip else ''
            user_input_tip = f"{word.get('part_of_speech', '')}{word['meaning']}: "
            clear_input_buffer()
            print(user_input_tip + first_letter, end='')
            user_input = (first_letter + input()).strip()

            if user_input == word[key_type]:
                print(f'{Cursor.UP(1)}\r{user_input_tip}{Fore.GREEN}{user_input}'
                      f'{Fore.RESET} {word.get('phonetic_symbol', '')}', ' ' * 50)
                speak(user_input)
                clear()
                left_words -= 1
                break

            # if not passed but status doesn't change
            if passed:
                wrong_list.append(word)
                passed = False

            last_wrong_input = user_input
            clear()

    return wrong_list


def fast_view_once(unit_data: dict, learning: bool = True, other_args: dict | None = None) -> dict:
    clear()
    data = unit_data

    wrong_words = process_section(
        data['words'], 'words', 'word', learning,
        other_wrong_count=0,
        other_args=other_args
    )
    wrong_phrases = process_section(
        data['phrases'], 'phrases', 'phrase', learning,
        other_wrong_count=len(wrong_words),
        other_args=other_args
    )

    clear()
    return {'words': wrong_words, 'phrases': wrong_phrases}


def fast_view(unit_data: dict, learning: bool = True, other_args: dict | None = None):
    wrong_data = fast_view_once(unit_data, learning=learning, other_args=other_args)
    while wrong_data['words'] or wrong_data['phrases']:
        wrong_data = fast_view_once(wrong_data, learning=learning, other_args=other_args)
