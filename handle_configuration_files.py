import json
import os


def parse_one_configuration_file_words_and_phrase_data(raw_configuration_file_json_data: dict):
    data_abspath: str

    if (data_file_name := raw_configuration_file_json_data["data_file_name"]) == "internal":
        data_abspath = os.path.join(os.path.dirname(__file__), 'data.json')
    else:
        data_abspath = os.path.join(os.path.dirname(__file__), 'data\\' + data_file_name)

    print(data_abspath)

    if isinstance((unit_keys := raw_configuration_file_json_data['units_keys']), str):
        unit_keys = [unit_keys]

    with open(data_abspath, encoding='UTF-8') as f:
        data_file_content = json.load(f)
        return {
            "words": [word for unit_key in unit_keys for word in data_file_content[unit_key]["words"]],
            "phrases": [phrase for unit_key in unit_keys for phrase in data_file_content[unit_key]["phrases"]]
        }

def parse_whole_configuration_file_words_and_phrase_data(raw_configuration_file_json_data: dict):
    data_content = raw_configuration_file_json_data["content"]
    words_list = {"words": [], "phrases": []}
    for configuration in data_content:
        result = parse_one_configuration_file_words_and_phrase_data(configuration)
        words_list["words"].extend(result["words"])
        words_list["phrases"].extend(result["phrases"])

    return words_list
