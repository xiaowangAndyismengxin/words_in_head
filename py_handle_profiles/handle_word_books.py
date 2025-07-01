from py_handle_profiles.handle_configuration_files import (
    parse_config_words_phrases,
    parse_manual_configuration_file_words_and_phrase_data,
    parse_auto_configuration_file_words_and_phrase_data,
)

import os
import json


def process_non_direct_part(part_text: dict):

    content_map = dict()

    part_name = part_text["name"]
    if part_name is None:
        return
    if part_text["generate_method"] == "manual":
        content_map[part_name] = parse_manual_configuration_file_words_and_phrase_data(
            part_text["content"]
        )

    elif part_text["generate_method"] == "auto":
        content_map[part_name] = parse_auto_configuration_file_words_and_phrase_data(
            part_text["content"]
        )

    else:
        raise ValueError(f"生成方法 {part_text['generate_method']} 不存在")

    return content_map


def process_direct_part(part_text: dict):
    content_map_list = list()
    for part in (
        part_text["content"]
        if isinstance(part_text["content"], list)
        else [part_text["content"]]
    ):
        content_map_list.append(
            {part.get("name", "未命名"): parse_config_words_phrases(part["content"])}
        )

    return content_map_list


def parse_word_book(whole_word_book: dict) -> tuple[str, dict]:
    parts_content_map = dict()
    book_name = whole_word_book.get("book_name", "未命名")

    for part in whole_word_book["content"]:
        if part.get("name") is not None:
            parts_content_map.update(process_non_direct_part(part))
        else:
            for content_map in process_direct_part(part):
                parts_content_map.update(content_map)

    return book_name, parts_content_map


def get_word_books_content_list() -> list[dict]:
    """获取所有单词本的内容列表"""
    import glob

    profiles_dir = os.path.join(os.path.dirname(__file__), "../profiles")
    word_books = []

    # 查找profiles目录下所有json文件
    for file_path in glob.glob(os.path.join(profiles_dir, "*.json")):
        try:
            with open(file_path, encoding="utf-8") as f:
                content = json.load(f)
                word_books.append(content)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

    return word_books


def parse_all_word_books() -> dict:

    hole_word_books = get_word_books_content_list()

    parsed_words_dict = dict()

    for word_book in hole_word_books:
        book_name, parts_content_map = parse_word_book(word_book)
        parsed_words_dict[book_name] = parts_content_map
    return parsed_words_dict


if __name__ == "__main__":
    print(parse_all_word_books())
    print(get_word_books_content_list())
