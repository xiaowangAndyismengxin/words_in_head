import colorama
from time import sleep
from fast_view import fast_view, clear, dictation, unbuffered_input, words_browse
from py_handle_profiles.handle_word_books import parse_all_word_books
from colorama import Fore

word_books_words_map = parse_all_word_books()
colorama.init()


def get_json_content_by_path(path: list[str, int], data=None) -> dict | list:
    if data is None:
        data = word_books_words_map
    target = data
    for key in path:
        target = target[key]
    return target


page_path = list()


def make_user_choice_general_options():
    global page_path
    # 显示可用选项
    print("可用的选项:")
    options = list(current_content.keys())
    for i, name in enumerate(options, 1):
        print(f"{i}. {name}")

    if page_path:
        print("a. 返回上一页, b. 回到首页")

    selected_option = None
    while True:
        try:
            choice = unbuffered_input(
                f"输入选项以继续{Fore.RED}(输入q退出){Fore.RESET}: "
            )

            if choice.strip().lower() == "q":
                quit()

            if page_path:
                if choice.strip().lower() == "a":
                    page_path.pop()
                    return

                if choice.strip().lower() == "b":
                    page_path.clear()
                    return

            choice_index = int(choice) - 1

            if 0 <= choice_index < len(options):
                selected_option = options[choice_index]
                break
            print("序号无效，请重新输入")
        except ValueError:
            print("请输入数字")

    if selected_option is not None:
        page_path.append(selected_option)


def make_user_choice_learning_options():

    print(
        """1. 快速查看
2. 练习
3. 听写
4. 学习"""
    )

    print("a. 返回上一页, b. 回到首页")
    exercise_content = current_content
    try:
        choice = unbuffered_input(
            f"请输入要执行的操作序号{Fore.RED}(输入q退出){Fore.RESET}: "
        )
        if choice.strip().lower() == "q":
            quit()
        if choice.strip().lower() == "a":
            page_path.pop()
            return
        if choice.strip().lower() == "b":
            page_path.clear()
            return

        choice = int(choice)
        if choice == 1:
            words_browse(exercise_content)
        elif choice == 2:
            fast_view(exercise_content, learning=False)
        elif choice == 3:
            dictation(exercise_content)
        elif choice == 4:
            fast_view(exercise_content, learning=True)
        else:
            print("序号无效，请重新输入")
            sleep(2)
            return
    except ValueError:
        print("请输入数字")
        sleep(2)
        return


while True:
    clear()

    current_content = get_json_content_by_path(page_path)

    # 显示当前路径
    print(
        f"当前路径: {' -> '.join([str(key) for key in page_path])}"
        if page_path
        else "当前路径: 根目录"
    )
    print()
    if current_content.get("words") is None:
        make_user_choice_general_options()
    else:
        make_user_choice_learning_options()

    clear()
