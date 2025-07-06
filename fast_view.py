"""
All functions have independent clear screen functions.
"""

import os
import random
import colorama
from tabulate import tabulate
from colorama import Fore, Cursor
import pyttsx3
import sys
import platform
from time import sleep
from playsound import playsound

USER_SYSTEM_TYPE = platform.system()


def clear_input_buffer():
    """清除标准输入缓冲区中的残留数据"""
    if USER_SYSTEM_TYPE == "Windows":
        import msvcrt

        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        import select

        while select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()


def unbuffered_input(prompt: str = ""):
    clear_input_buffer()
    return input(prompt)


PARTS_OF_SPEECH_MAP = {
    "n.": "名词",
    "v.": "动词",
    "adj.": "形容词",
    "adv.": "副词",
    "prep.": "介词",
    "conj.": "连词",
    "pron.": "代词",
    "intj.": "感叹词",
    "num.": "数字",
    "art.": "冠词",
}

english_voice = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
chinese_voice = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0"
english_rate = 130
chinese_rate = 150

engine = pyttsx3.init()
engine.setProperty("voice", english_voice)

engine.setProperty("rate", english_rate)
colorama.init()


def speak(text: str):
    global engine
    engine.say(text)
    engine.runAndWait()


def clear():
    if USER_SYSTEM_TYPE == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def process_section(
    section_data: list,
    section_type: str,
    key_type: str,
    learning: bool,
    other_wrong_count: int = 0,
    other_args: dict | None = None,
):
    other_args = other_args or dict()

    # import args from other_args
    first_letter_tip = other_args.get("first_letter_tip", False)

    wrong_list = []
    words = section_data.copy()
    random.shuffle(words)
    left_words = len(words)

    first_letter: str

    for word in words:
        passed = True
        last_wrong_input = ""
        while True:
            clear()

            # print header
            print(
                f"--{section_type}--  ",
                f"剩下: {left_words}"
                f" 错: {len(wrong_list)
                        + other_wrong_count}\n\n\n",
            )
            # wrong word header
            if not passed:
                print("That is wrong: " + Fore.RED + last_wrong_input + Fore.RESET)

            # print word tip
            if learning or not passed:
                print(tabulate([word], headers="keys"))
                speak(word[key_type])
                unbuffered_input("按回车继续")
                clear()
                print(
                    f"--{section_type}--  ",
                    f"剩下: {left_words}"
                    f" 错: {len(wrong_list)
                            + other_wrong_count}\n\n\n",
                )

            # handle user input
            first_letter = word[key_type][0] if first_letter_tip else ""
            user_input_tip = f"{word.get('part_of_speech', '')}{word['meaning']}: "
            print(user_input_tip + first_letter, end="")
            user_input = (first_letter + unbuffered_input()).strip()

            if user_input == word[key_type]:
                print(
                    f"{Cursor.UP(1)}\r{user_input_tip}{Fore.GREEN}{user_input}"
                    f"{Fore.RESET} {word.get('phonetic_symbol', '')}",
                    " " * 50,
                )
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


def fast_view_once(
    unit_data: dict, learning: bool = True, other_args: dict | None = None
) -> dict:
    clear()
    data = unit_data

    wrong_words = process_section(
        data["words"],
        "words",
        "word",
        learning,
        other_wrong_count=0,
        other_args=other_args,
    )
    wrong_phrases = process_section(
        data["phrases"],
        "phrases",
        "phrase",
        learning,
        other_wrong_count=len(wrong_words),
        other_args=other_args,
    )

    clear()
    return {"words": wrong_words, "phrases": wrong_phrases}


def fast_view(unit_data: dict, learning: bool = True, other_args: dict | None = None):
    wrong_data = fast_view_once(unit_data, learning=learning, other_args=other_args)
    while wrong_data.get("words", []) or wrong_data.get("phrases", []):
        wrong_data = fast_view_once(
            wrong_data, learning=learning, other_args=other_args
        )


def dictation(unit_data: dict, delay: float = 5):
    global engine
    clear()

    # 定义词性对照表（提取到函数开头）

    def get_chinese_pos(part_of_speech: str) -> str:
        """处理词性并返回中文描述"""

        if "/" in part_of_speech:
            pos_list = [p.strip() for p in part_of_speech.split("/")]
            chinese_pos = "或".join(
                PARTS_OF_SPEECH_MAP.get(p, p) + ", " for p in pos_list
            )
        else:
            chinese_pos = PARTS_OF_SPEECH_MAP.get(part_of_speech, part_of_speech) + ", "

        return chinese_pos

    print(f"{Fore.YELLOW}READY GO!{Fore.RESET}")

    # 使用音效
    playsound(
        os.path.join(
            os.path.dirname(__file__),
            "audios\\dictation_audio-ready_go.wav",
        ).replace("\\", "\\\\")
    )

    # 保存原始语音设置
    original_voice = engine.getProperty("voice")
    original_rate = engine.getProperty("rate")

    # 设置中文
    engine.setProperty("voice", chinese_voice)
    engine.setProperty("rate", chinese_rate)

    # 打乱词表
    random.shuffle(unit_data["words"])
    random.shuffle(unit_data["phrases"])

    current_count = 1
    answer_lines = []
    total_items = len(unit_data["words"]) + len(unit_data["phrases"])

    # 处理单词
    for word in unit_data["words"]:
        clear()
        # 动态生成头部信息
        print(f"--dictation--  ordinal: {current_count} total: {total_items}\n\n\n")

        # 显示和朗读内容
        display_text = f"{word.get('part_of_speech', '')}{word['meaning']}"
        speech_text = (
            f"{get_chinese_pos(word.get('part_of_speech', ''))}{word['meaning']}"
        )

        print(display_text)
        # 朗读两次
        speak(speech_text)
        speak(speech_text)

        sleep(delay)
        answer_lines.append(f"{current_count}.{word['word']} --- {word['meaning']}")
        current_count += 1
        clear()

    # 处理短语
    for phrase in unit_data["phrases"]:
        clear()
        # 动态生成头部信息
        print(f"--dictation--  ordinal: {current_count} total: {total_items}\n\n\n")

        display_text = phrase["meaning"]
        speech_text = f"短语, {get_chinese_pos(phrase.get('part_of_speech', ''))}{phrase['meaning']}"

        print(display_text)
        # 朗读两次
        speak(speech_text)
        speak(speech_text)

        sleep(delay)
        answer_lines.append(
            f"{current_count}.{phrase['phrase']} --- {phrase['meaning']}"
        )
        current_count += 1
        clear()

    # 恢复原始语音设置
    engine.setProperty("voice", original_voice)
    engine.setProperty("rate", original_rate)

    # 输出结果
    print("dictation finished")
    speak("dictation finished")

    full_answer = "\n".join(answer_lines)
    print(full_answer)
    unbuffered_input("按回车退出")
    clear()


def words_browse(unit_data: dict):
    clear()
    # 创建一个新列表合并单词和短语
    all_items = unit_data["words"].copy()
    if "phrases" in unit_data.keys():
        all_items.extend(unit_data["phrases"])

    for item in all_items:
        print(
            f'{item["word"] if "word" in item else item["phrase"]} ----- '
            f'{item.get("part_of_speech", "")}{item["meaning"]}  '
            f'{item.get("phonetic_symbol", "")}'
        )
    unbuffered_input("按回车退出")
    clear()
