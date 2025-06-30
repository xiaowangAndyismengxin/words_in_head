from handle_configuration_files import (
    parse_one_configuration_file_words_and_phrase_data,
    parse_manual_configuration_file_words_and_phrase_data,
    parse_auto_configuration_file_words_and_phrase_data,
)

import os
import json


def phrase_one_part_no_direct(part_text: dict):

    name_and_content_dict = dict()

    part_name = part_text["name"]
    if part_name is None:
        return
    if part_text["generate_method"] == "manual":
        name_and_content_dict[part_name] = (
            parse_manual_configuration_file_words_and_phrase_data(part_text["content"])
        )

    elif part_text["generate_method"] == "auto":
        name_and_content_dict[part_name] = (
            parse_auto_configuration_file_words_and_phrase_data(part_text["content"])
        )

    else:
        raise ValueError(f"生成方法 {part_text['generate_method']} 不存在")

    return name_and_content_dict


def phrase_one_direct_part(part_text: dict):
    name_and_content_dict_list = list()
    for part in part_text["content"]:
        name_and_content_dict_list.append(
            {
                part.get(
                    "name", "未命名"
                ): parse_one_configuration_file_words_and_phrase_data(part["content"])
            }
        )

    return name_and_content_dict_list


def parse_one_word_book(hole_word_book: dict) -> tuple[str, list]:
    parts_content_list = list()
    book_name = hole_word_book.get("book_name", "未命名")

    for part in hole_word_book["content"]:
        if part.get("name") is not None:
            parts_content_list.append(phrase_one_part_no_direct(part))
        else:
            parts_content_list.append(phrase_one_direct_part(part))

    return book_name, parts_content_list


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
        book_name, parts_content_list = parse_one_word_book(word_book)
        parsed_words_dict[book_name] = parts_content_list
    return parsed_words_dict


print(parse_all_word_books())
