import colorama
from time import sleep
from word_learner import WordLearner
from py_handle_profiles.handle_word_books import parse_all_word_books
from colorama import Fore
import json
import os


class WordLearningApp:
    """以page_path为准，current_content有滞后性"""

    def __init__(self):

        self.settings_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "settings.json"
        )
        with open(self.settings_path, "r", encoding="utf-8") as f:
            self.settings = json.load(f)
        self.voice_settings = self.settings["voice"]

        self.page_path = list()
        self.learner: WordLearner = WordLearner(
            default_zh_cn_voice=self.voice_settings["zh-CN"],
            default_en_voice=self.voice_settings[
                self.voice_settings["english_pronunciation"]
            ],
        )
        self.speak = self.learner.speak
        self.clear = self.learner.clear
        self.unbuffered_input = self.learner.unbuffered_input
        self.clear_voice_cache = self.learner.voice_player.clear_cache

        self.word_books_words_map = parse_all_word_books()
        self.current_content = self.word_books_words_map

        colorama.init()

    def get_current_content(self) -> dict | list:
        data = self.word_books_words_map
        target = data
        for key in self.page_path:
            target = target[key]
        return target

    def _make_user_choice_general_options(self):

        print("可用的选项:")
        options = list(self.current_content.keys())
        for i, name in enumerate(options, 1):
            print(f"{i}. {name}")

        if self.page_path:
            print("a. 返回上一页, b. 回到首页, ", end="")
        print("c. 改变英语发音(英音/美音), d. 清空语音缓存")

        selected_option = None
        while True:
            try:
                choice = self.unbuffered_input(
                    f"输入选项以继续{Fore.RED}(输入q退出){Fore.RESET}: "
                )

                if choice.strip().lower() == "q":
                    quit()

                if self.page_path:
                    if choice.strip().lower() == "a":
                        self.page_path.pop()
                        return

                    if choice.strip().lower() == "b":
                        self.page_path.clear()
                        return

                if choice.strip().lower() == "c":
                    self.change_english_pronunciation()
                    return

                if choice.strip().lower() == "d":
                    self.clear_voice_cache()
                    return

                choice_index = int(choice) - 1

                if 0 <= choice_index < len(options):
                    selected_option = options[choice_index]
                    break
                print("序号无效，请重新输入")
            except ValueError:
                print("请输入数字")

        if selected_option is not None:
            self.page_path.append(selected_option)

    def _make_user_choice_learning_options(self):

        print("1. 快速查看\n2. 练习\n3. 听写\n4. 学习")

        print("a. 返回上一页, b. 回到首页, c. 改变英语发音(英音/美音), d. 清空语音缓存")
        exercise_content = self.current_content
        try:
            choice = self.unbuffered_input(
                f"请输入要执行的操作序号{Fore.RED}(输入q退出){Fore.RESET}: "
            )
            if choice.strip().lower() == "q":
                quit()
            if choice.strip().lower() == "a":
                self.page_path.pop()
                return
            if choice.strip().lower() == "b":
                self.page_path.clear()
                return
            if choice.strip().lower() == "c":
                self.change_english_pronunciation()
                return
            if choice.strip().lower() == "d":
                self.clear_voice_cache()
                return

            choice = int(choice)
            if choice == 1:
                self.learner.words_browse(exercise_content)
            elif choice == 2:
                self.learner.fast_view(exercise_content, learning=False)
            elif choice == 3:
                self.learner.dictation(
                    exercise_content,
                    delay=self.settings["dictation_delay"],
                    use_dictation_start_sound=self.settings[
                        "use_dictation_start_sound"
                    ],
                )
            elif choice == 4:
                self.learner.fast_view(exercise_content, learning=True)
            else:
                print("序号无效，请重新输入")
                sleep(2)
                return
        except ValueError:
            print("请输入数字")
            sleep(2)
            return

    def main(self):
        while True:
            self.clear()

            self.current_content = self.get_current_content()

            # 显示当前路径
            print(
                (
                    f"当前路径: {' -> '.join([str(key) for key in self.page_path])}"
                    if self.page_path
                    else "当前路径: 根目录"
                ),
                end="",
            )
            print(f"  当前发音: {self.learner.default_en_voice
                .replace("en-US", "美音")
                .replace("en-GB", "英音")}({self.learner.default_en_voice})")
            print()

            if self.current_content.get("words") is None:
                self._make_user_choice_general_options()
            else:
                self._make_user_choice_learning_options()

            self.clear()

    def change_english_pronunciation(self):
        self.voice_settings["english_pronunciation"] = (
            "en-GB"
            if self.voice_settings["english_pronunciation"] == "en-US"
            else "en-US"
        )

        self.settings["voice"] = self.voice_settings
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)
        self.learner.default_en_voice = self.voice_settings[
            self.voice_settings["english_pronunciation"]
        ]


if __name__ == "__main__":
    app = WordLearningApp()
    app.main()
