"""
单词学习核心功能模块，提供交互式单词学习、听写和浏览功能
支持中英文语音朗读、错误记录和多轮复习机制
"""

import asyncio
import os
import random
from typing import Optional, List, Dict, Any, Union

import colorama
from tabulate import tabulate
from colorama import Fore, Cursor
from voice_player_with_cache import VoicePlayerWithCache
import sys
import platform
from time import sleep
import pygame


class WordLearner:
    """
    单词学习核心控制器，提供以下功能：
    - 单词/短语的快速浏览、学习练习、听写测试
    - 语音播放（支持单词发音、中文提示）及预生成缓存
    - 跨平台终端交互（清屏、无缓冲输入、输入缓冲区清理）
    - 学习过程中的错误记录与重复练习

    所有方法均包含独立的清屏逻辑，确保终端界面整洁。
    """

    def __init__(self, default_zh_cn_voice: str, default_en_voice: str) -> None:
        """
        初始化单词学习器，配置语音参数和系统环境

        Args:
            default_zh_cn_voice: 中文默认语音模型（如 'zh-CN-XiaoxiaoNeural'）
            default_en_voice: 英文默认语音模型（如 'en-US-AriaNeural'）
        """
        self.user_system_type = platform.system()
        pygame.mixer.init()

        self.parts_of_speech_map = {
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

        self.default_zh_cn_voice = default_zh_cn_voice
        self.default_en_voice = default_en_voice

        self.voice_player: VoicePlayerWithCache = VoicePlayerWithCache(
            default_voice=self.default_en_voice
        )
        colorama.init()

    def clear_input_buffer(self) -> None:
        """清除标准输入缓冲区中的残留数据"""
        if self.user_system_type == "Windows":
            import msvcrt

            while msvcrt.kbhit():
                msvcrt.getch()
        else:
            import select

            while select.select([sys.stdin], [], [], 0)[0]:
                sys.stdin.readline()

    def unbuffered_input(self, prompt: str = "") -> str:
        """
        无缓冲输入函数，确保用户输入前清空缓冲区，避免残留输入干扰

        Args:
            prompt: 输入提示文本

        Returns:
            用户输入的字符串
        """
        self.clear_input_buffer()
        return input(prompt)

    def speak(self, text: str, voice: Optional[str] = None) -> None:
        """
        调用语音播放器朗读指定文本

        Args:
            text: 待朗读的文本内容
            voice: 语音模型名称，默认为None（使用self.default_en_voice）
        """
        if voice is None:
            voice = self.default_en_voice
        asyncio.run(self.voice_player.speak(text, voice=voice))

    def pregenerate_voices(
        self, word_list: List[str], voice: Optional[str] = None
    ) -> None:
        """
        预生成单词列表的语音文件，提高后续播放效率

        Args:
            word_list: 需要预生成语音的单词/短语列表
            voice: 语音模型名称，默认为None（使用self.default_en_voice）
        """
        if voice is None:
            voice = self.default_en_voice
        asyncio.run(self.voice_player.pregenerate_voices(word_list, voice=voice))

    def clear(self) -> None:
        """清空终端屏幕（跨平台兼容）"""
        if self.user_system_type == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def process_section(
        self,
        section_data: List[Dict[str, Any]],
        section_type: str,
        key_type: str,
        learning: bool,
        other_wrong_count: int = 0,
        other_args: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        处理单词/短语的学习流程（核心逻辑），包括展示、用户输入校验、错误记录

        Args:
            section_data: 待学习的单词/短语数据列表（每个元素为包含单词信息的字典）
            section_type: 内容类型（如 'words' 或 'phrases'，用于界面提示）
            key_type: 校验的关键字段（如 'word' 或 'phrase'，用于比对用户输入）
            learning: 是否为学习模式（True则展示单词详情，False则仅提示释义）
            other_wrong_count: 其他部分（如单词/短语）已累计的错误数，用于总错误统计
            other_args: 额外参数（如首字母提示开关），格式为字典

        Returns:
            学习过程中用户答错的单词/短语列表
        """
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
                self.clear()

                # print header
                print(
                    f"--{section_type}--  ",
                    f"剩下: {left_words}" f" 错: {len(wrong_list)
                            + other_wrong_count}\n\n\n",
                )
                # wrong word header
                if not passed:
                    print("That is wrong: " + Fore.RED + last_wrong_input + Fore.RESET)

                # print word tip
                if learning or not passed:
                    print(tabulate([word], headers="keys"))
                    self.speak(word[key_type])
                    self.unbuffered_input("按回车继续")
                    self.clear()
                    print(
                        f"--{section_type}--  ",
                        f"剩下: {left_words}" f" 错: {len(wrong_list)
                                + other_wrong_count}\n\n\n",
                    )

                # handle user input
                first_letter = word[key_type][0] if first_letter_tip else ""
                user_input_tip = f"{word.get('part_of_speech', '')}{word['meaning']}: "
                print(user_input_tip + first_letter, end="")
                user_input = (first_letter + self.unbuffered_input()).strip()

                if user_input == word[key_type]:
                    print(
                        f"{Cursor.UP(1)}\r{user_input_tip}{Fore.GREEN}{user_input}"
                        f"{Fore.RESET} {word.get('phonetic_symbol', '')}",
                        " " * 50,
                    )
                    self.speak(user_input)
                    self.clear()
                    left_words -= 1
                    break

                # if not passed but status doesn't change
                if passed:
                    wrong_list.append(word)
                    passed = False

                last_wrong_input = user_input
                self.clear()

        return wrong_list

    def fast_view_once(
        self,
        unit_data: Dict[str, List[Dict[str, Any]]],
        learning: bool = True,
        other_args: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        单次快速学习/复习单词和短语（不重复错误内容）

        Args:
            unit_data: 包含单词和短语数据的单元字典（需包含 'words' 和 'phrases' 键）
            learning: 是否为学习模式（True则展示详情，False为测试模式）
            other_args: 额外参数（如首字母提示）

        Returns:
            包含错误单词和短语的字典（格式同unit_data）
        """
        self.clear()
        data = unit_data

        wrong_words = self.process_section(
            data["words"],
            "words",
            "word",
            learning,
            other_wrong_count=0,
            other_args=other_args,
        )
        wrong_phrases = self.process_section(
            data["phrases"],
            "phrases",
            "phrase",
            learning,
            other_wrong_count=len(wrong_words),
            other_args=other_args,
        )

        self.clear()
        return {"words": wrong_words, "phrases": wrong_phrases}

    def fast_view(
        self,
        unit_data: Dict[str, List[Dict[str, Any]]],
        learning: bool = True,
        other_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        快速学习模式（核心入口），循环练习错误内容直到全部掌握

        Args:
            unit_data: 单元数据字典（包含 'words' 和 'phrases'）
            learning: 是否为学习模式
            other_args: 额外参数（如首字母提示）
        """
        self.pregenerate_voices(
            [word["word"] for word in unit_data["words"]]
            + [phrase["phrase"] for phrase in unit_data["phrases"]]
        )

        wrong_data = self.fast_view_once(
            unit_data, learning=learning, other_args=other_args
        )
        while wrong_data.get("words", []) or wrong_data.get("phrases", []):
            wrong_data = self.fast_view_once(
                wrong_data, learning=learning, other_args=other_args
            )

    def get_chinese_pos(self, part_of_speech: str) -> str:
        """
        将英文词性描述转换为对应的中文描述。
        若英文词性包含多个用 '/' 分隔的值，会将每个值转换为中文后用 '或' 连接。

        Args:
            part_of_speech: 英文词性描述，可能包含多个用 '/' 分隔的值。

        Returns:
            对应的中文词性描述，若未找到对应翻译则返回原英文词性。
        """
        if "/" in part_of_speech:
            pos_list = [p.strip() for p in part_of_speech.split("/")]
            chinese_pos = "或".join(
                self.parts_of_speech_map.get(p, p) for p in pos_list
            )
        else:
            chinese_pos = self.parts_of_speech_map.get(part_of_speech, part_of_speech)

        return chinese_pos

    def dictation(
        self,
        unit_data: Dict[str, List[Dict[str, Any]]],
        delay: float = 5,
        use_dictation_start_sound: bool = True,
    ) -> None:
        """
        执行单词和短语的听写测试功能。
        该函数会打乱单词和短语列表，预生成中文提示语音，播放提示音频，
        并在指定延迟后等待用户完成听写，最后输出听写结果。

        Args:
            unit_data: 包含单词和短语数据的字典，
                键通常为 'words' 和 'phrases'，对应的值为包含单词或短语信息的字典列表。
            delay: 每次播放提示语音后等待用户输入的延迟时间，单位为秒。
                默认值为 5 秒。
            use_dictation_start_sound: 是否使用听写开始提示音(ready-go)。
        """
        self.clear()

        # 保存原始语音设置
        original_voice = self.voice_player.default_voice

        # 设置中文
        self.voice_player.default_voice = self.default_zh_cn_voice

        # 打乱词表
        random.shuffle(unit_data["words"])
        random.shuffle(unit_data["phrases"])

        current_count = 1
        answer_lines = []
        total_items = len(unit_data["words"]) + len(unit_data["phrases"])
        items = unit_data["words"] + unit_data["phrases"]

        read_list = [
            f"{self.get_chinese_pos(word['part_of_speech'])}，{word['meaning']}"
            for word in unit_data["words"]
        ] + [
            f"短语，{self.get_chinese_pos(phrase.get('part_of_speech', ''))}，"
            f"{phrase['meaning']}"
            for phrase in unit_data["phrases"]
        ]
        asyncio.run(
            self.voice_player.pregenerate_voices(
                read_list, voice=self.default_zh_cn_voice
            )
        )

        if use_dictation_start_sound:
            self.clear()
            print(f"{Fore.YELLOW}READY GO!{Fore.RESET}")
            # 停止当前可能正在播放的音频
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            # 加载并播放
            pygame.mixer.music.load(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "audios",
                    "dictation_audio-ready_go.wav",
                )
            )
            pygame.mixer.music.play()

            # 等待播放完成
            while pygame.mixer.music.get_busy():
                import time

                time.sleep(0.1)  # 每 0.1 秒检查一次播放状态

        for item in items:
            self.clear()
            print(
                f"--dictation--  original: {current_count} total: {total_items}\n\n\n"
            )
            print(f"{item.get('part_of_speech', '')}{item['meaning']}")
            self.speak(read_list[current_count - 1], voice=self.default_zh_cn_voice)
            self.speak(read_list[current_count - 1], voice=self.default_zh_cn_voice)
            sleep(delay)

            answer_lines.append(
                f"{current_count}. {item.get('part_of_speech', '')}{item.get('word') or item.get('phrase')} ----- {item['meaning']}"
            )
            current_count += 1
        self.clear()

        # 恢复原始语音设置
        self.voice_player.default_voice = original_voice

        # 输出结果
        print("dictation finished")
        self.speak("dictation finished")

        full_answer = "\n".join(answer_lines)
        print(full_answer)
        self.unbuffered_input("按回车退出")
        self.clear()

    def words_browse(self, unit_data: Dict[str, List[Dict[str, Any]]]) -> None:
        """
        浏览模式：展示单元内所有单词和短语的信息

        Args:
            unit_data: 包含单词和短语数据的字典（需包含 'words' 和 'phrases' 键）
        """
        self.clear()
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
        self.unbuffered_input("按回车退出")
        self.clear()
