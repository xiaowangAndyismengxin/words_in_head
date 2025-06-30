import json
import os
from typing import Dict, List, Union


def integrate_one_data_file_units(
    dict_with_data_file_name_and_units: Dict[str, Union[str, List[str]]],
) -> Dict[str, List[Dict]] | None:  # 更精确的返回类型注解

    data_abspath: str

    data_file_name: str = dict_with_data_file_name_and_units["data_file_name"]

    data_abspath = os.path.join(
        os.path.dirname(__file__), "../data", data_file_name
    )  # 改用跨平台路径

    if isinstance((unit_keys := dict_with_data_file_name_and_units["unit_keys"]), str):
        unit_keys = [unit_keys]

    try:
        with open(data_abspath, encoding="UTF-8") as f:
            data_file_content = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"数据文件 {data_file_name} 不存在于 data 目录")
    except json.JSONDecodeError:
        raise ValueError(f"数据文件 {data_file_name} 格式错误")

    return {
        "words": [
            word
            for unit_key in unit_keys
            for word in data_file_content[unit_key].get("words", [])
        ],
        "phrases": [
            phrase
            for unit_key in unit_keys
            for phrase in data_file_content[unit_key].get("phrases", [])
        ],
    }


def parse_one_configuration_file_words_and_phrase_data(
    data_content: dict | list[dict],
):
    if isinstance(data_content, dict):
        data_content = [data_content]
    words_list = {"words": [], "phrases": []}
    for configuration in data_content:
        result = integrate_one_data_file_units(configuration)
        words_list["words"].extend(result["words"])
        words_list["phrases"].extend(result["phrases"])

    return words_list


def parse_manual_configuration_file_words_and_phrase_data(
    content: List[Dict] | Dict,
) -> Dict[str, Dict[str, List[Dict]]]:

    name_and_content_dict = dict()

    if isinstance(content, dict):
        content = [content]
    for configuration in content:
        name_and_content_dict[configuration.get("name", "未命名")] = (
            parse_one_configuration_file_words_and_phrase_data(configuration["content"])
        )

    return name_and_content_dict


def parse_auto_configuration_file_words_and_phrase_data(
    content: dict,
) -> Dict[str, Dict[str, List[Dict]]]:

    name_and_content_dict = dict()

    connection = f' {content.get("connection", "and")} '
    data_file_name = content["data_file_name"]
    unit_keys = content["unit_keys"]
    if isinstance(unit_keys, str):
        unit_keys = [unit_keys]

    for unit in unit_keys:
        if isinstance(unit, str):
            unit = [unit]

        name_and_content_dict[connection.join(unit)] = integrate_one_data_file_units(
            {"data_file_name": data_file_name, "unit_keys": unit}
        )

    return name_and_content_dict
