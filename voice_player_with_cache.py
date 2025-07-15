from asyncio import sleep
import edge_tts
import asyncio
from pathlib import Path
import hashlib
from typing import Optional, List
from tqdm import tqdm
import pygame


class VoicePlayerWithCache:
    """支持语音缓存的语音播放器
    edge-tts --list-voices查看可用的语音模型"""

    def __init__(
        self,
        cache_dir: str = "voice_cache",
        default_voice: str = "zh-CN-XiaoxiaoNeural",
        rate: str = "+0%",
        volume: str = "+0%",
        max_retries: int = 3,
    ):
        """
        初始化语音播放器

        Args:
            cache_dir: 缓存目录路径
            default_voice: 默认语音模型
            rate: 语速，例如 "+10%" 或 "-20%"
            volume: 音量，例如 "+0%" 或 "+20%"
            max_retries: 最大重试次数
        """
        self.cache_dir = Path(__file__).absolute().parent / cache_dir
        self.default_voice = default_voice
        self.rate = rate
        self.volume = volume
        self.max_retries = max_retries

        pygame.mixer.init()

        # 确保缓存目录存在
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_file_path(self, text: str, voice: Optional[str] = None) -> Path:
        """生成缓存文件路径（用哈希值替代原文本）"""
        voice_name = voice or self.default_voice

        # 核心：将「语音模型+文本」组合计算哈希
        # 1. 组合内容（用特殊符号分隔，避免不同文本哈希冲突）
        content = f"{voice_name}||{text}".encode("utf-8")  # 双竖线分隔更安全
        # 2. 计算MD5哈希（32位纯字母数字，无特殊字符）
        hash_str = hashlib.md5(content).hexdigest()  # 结果如：a1b2c3d4...

        # 生成文件名：语音模型_哈希值.mp3
        return self.cache_dir / f"{voice_name}_{hash_str}.mp3"

    async def _generate_voice(self, text: str, voice: Optional[str] = None) -> Path:
        """生成语音文件并返回路径"""
        voice = voice or self.default_voice
        output_file = self._get_cache_file_path(text, voice)

        for attempt in range(self.max_retries):
            try:
                # 创建 Edge TTS 通信对象并生成语音
                communicate = edge_tts.Communicate(
                    text=text, voice=voice, rate=self.rate, volume=self.volume
                )
                await communicate.save(str(output_file))
                return output_file
            except Exception as e:
                if attempt == self.max_retries - 1:
                    if output_file.exists():
                        output_file.unlink()
                    raise RuntimeError(f"语音生成失败: {str(e)}") from e

        return output_file

    async def speak(self, text: str, voice: Optional[str] = None) -> None:
        if not text.strip():
            return

        voice = voice or self.default_voice
        cache_file = self._get_cache_file_path(text, voice)

        if not cache_file.exists():
            await self._generate_voice(text, voice)

        if not cache_file.exists():
            raise RuntimeError(f"音频文件未生成: {cache_file}")

        try:

            # 停止当前可能正在播放的音频
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            # 加载并播放 MP3
            pygame.mixer.music.load(str(cache_file))
            pygame.mixer.music.play()

            # 等待播放完成
            while pygame.mixer.music.get_busy():
                await sleep(0.1)

        except Exception as e:
            raise RuntimeError(f"播放失败（文件：{cache_file.name}）：{str(e)}") from e

    async def pregenerate_voices(
        self,
        word_list: List[str],
        voice: Optional[str] = None,
        show_progress_bar: bool = True,
    ) -> None:
        """
        批量预生成语音文件，带进度条显示

        Args:
            word_list: 单词列表
            voice: 语音模型，默认为初始化时设置的语音
            show_progress_bar: 是否显示进度条
        """
        voice = voice or self.default_voice

        # 过滤空单词
        filtered_words = [word for word in word_list if word.strip()]
        if not filtered_words:
            return

        # 统计已存在的缓存数量
        existing_count = 0
        for word in filtered_words:
            if self._get_cache_file_path(word, voice).exists():
                existing_count += 1

        # 创建进度条
        with tqdm(
            total=len(filtered_words),
            desc=f"预生成语音 ({voice})",
            unit="单词",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        ) as pbar:

            tasks = []

            if not show_progress_bar:
                pbar.disable()

            # 更新已存在的缓存数量
            pbar.update(existing_count)

            # 生成不存在的语音
            for word in filtered_words:
                cache_file = self._get_cache_file_path(word, voice)

                # 检查缓存是否存在
                if cache_file.exists():
                    continue

                # 缓存不存在，添加到任务队列

                tasks.append(asyncio.create_task(self._generate_voice(word, voice)))

            for task in tasks:
                task.add_done_callback(lambda t: pbar.update(1))

            await asyncio.gather(*tasks)

    def clear_cache(self) -> None:
        """清空所有语音缓存文件"""
        try:
            # 尝试删除文件，跳过正在使用的文件
            for file in self.cache_dir.glob("*.mp3"):
                try:
                    file.unlink()
                except PermissionError:
                    raise RuntimeError(
                        f"警告: 无法删除文件 {file}，可能仍在使用中，你不是不小心开了多个背单词小程序？"
                    )
        except Exception as e:
            raise RuntimeError(f"清空缓存失败: {str(e)}") from e
