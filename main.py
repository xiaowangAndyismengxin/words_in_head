from fast_view import fast_view, clear, dictation, unbuffered_input, words_browse
from py_handle_profiles.handle_word_books import parse_all_word_books
import os
import json

word_books_words_map = parse_all_word_books()

# 显示可用词书
print("可用的词书:")
book_names = list(word_books_words_map.keys())
for i, name in enumerate(book_names, 1):
    print(f"{i}. {name}")

# 选择词书
while True:
    try:
        choice = int(unbuffered_input("请输入要查看的词书序号: ")) - 1
        if 0 <= choice < len(book_names):
            selected_book = book_names[choice]
            break
        print("序号无效，请重新输入")
    except ValueError:
        print("请输入数字")
clear()

book_content = word_books_words_map[selected_book]

exercise_content = None
for _ in range(2):
    print(f"可用的练习:")
    exercises = list(book_content.keys())
    for i, exercise in enumerate(exercises, 1):
        print(f"{i}. {exercise}")

    # 选择词书
    while True:
        try:
            choice = int(unbuffered_input("请输入要查看的练习序号: ")) - 1
            if 0 <= choice < len(exercises):
                selected_exercise = exercises[choice]
                break
            print("序号无效，请重新输入")
        except ValueError:
            print("请输入数字")
    exercise_content = book_content[selected_exercise]
    clear()
    if (
        exercise_content.get("words") is not None
        or exercise_content.get("phrases") is not None
    ):
        break
    book_content = exercise_content

while True:

    print(
        """1. 快速查看
2. 练习
3. 听写
4. 学习"""
    )

    choice = int(unbuffered_input("请输入要执行的操作序号: "))
    clear()
    if choice == 1:
        words_browse(exercise_content)
    elif choice == 2:
        fast_view(exercise_content)
    elif choice == 3:
        dictation(exercise_content)
    elif choice == 4:
        fast_view(exercise_content, learning=True)
    else:
        print("序号无效，请重新输入")
        continue

    if choice != 1:
        break
