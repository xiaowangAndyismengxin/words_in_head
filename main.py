from fast_view import fast_view, clear, dictation
from py_handle_profiles.handle_configuration_files import (
    parse_whole_configuration_file_words_and_phrase_data,
)
import os
import json

# 配置文件目录
PROFILES_DIR = os.path.join(os.path.dirname(__file__), "profiles")


def get_configurations() -> list:
    with open(os.path.join(PROFILES_DIR, "configurations.json"), encoding="UTF-8") as f:
        return json.load(f)


def select_profile() -> dict:
    configurations = get_configurations()
    print("可用配置文件:")

    for i, config in enumerate(configurations):
        print(f"{i + 1}. {config.get('name', '未命名')}")

    while True:
        try:
            choice = int(input("请输入要使用的配置文件编号: "))
            if 1 <= choice <= len(configurations):
                return configurations[choice - 1]
            else:
                print("无效选择，请重试。")
        except ValueError:
            print("输入无效，请输入数字。")


def main():
    # 选择配置文件
    profile_data = select_profile()
    if not profile_data:
        return

    words_and_phrases_data = parse_whole_configuration_file_words_and_phrase_data(
        profile_data
    )
    clear()
    learning_mode = profile_data.get("learning_mode")
    dictation_mode = input("是否开启听写模式？(y/n): ").lower() == "y"
    if dictation_mode:
        dictation(words_and_phrases_data)
        return
    if learning_mode is None:
        learning_mode = (
            input("由于配置文件没有指定模式，是否开启学习模式？(y/n): ").lower() == "y"
        )

    fast_view(
        words_and_phrases_data,
        learning=learning_mode,
        other_args=profile_data.get("other_args", dict()),
    )


if __name__ == "__main__":
    main()
