from fast_view import fast_view, clear_input_buffer, clear
from handle_configuration_files import parse_whole_configuration_file_words_and_phrase_data
import os
import json

# 配置文件目录
PROFILES_DIR = os.path.join(os.path.dirname(__file__), 'profiles')

def list_profiles():
    """列出所有可用的配置文件及其名称"""
    profiles = [f for f in os.listdir(PROFILES_DIR) if f.endswith('.json')]
    if not profiles:
        print("未找到任何配置文件")
        return None

    profile_names = []
    for profile in profiles:
        with open(os.path.join(PROFILES_DIR, profile), encoding='UTF-8') as f:
            data = json.load(f)
            profile_names.append((profile, data.get('name', '未命名配置文件')))

    return profile_names

def select_profile():
    """让用户选择配置文件"""
    profiles = list_profiles()
    if not profiles:
        return None

    print("请选择一个配置文件：")
    for i, (filename, name) in enumerate(profiles):
        print(f"{i+1}. {name} ({filename})")

    while True:
        try:
            clear_input_buffer()  # 在input前清除缓冲区
            choice = int(input("请输入编号："))
            if 1 <= choice <= len(profiles):
                return os.path.join(PROFILES_DIR, profiles[choice-1][0])
            print("编号无效，请重新输入")
        except ValueError:
            print("请输入有效的数字")

def load_profile(profile_path):
    """加载选定的配置文件"""
    with open(profile_path, encoding='UTF-8') as f:
        return json.load(f)

def main():
    # 选择配置文件
    profile_path = select_profile()
    if not profile_path:
        return

    # 加载配置文件
    profile_data = load_profile(profile_path)
    words_and_phrases_data = parse_whole_configuration_file_words_and_phrase_data(profile_data)
    clear()
    fast_view(words_and_phrases_data, learning=profile_data["learning_mode"],
              other_args=profile_data["other_args"])

if __name__ == '__main__':
    main()
