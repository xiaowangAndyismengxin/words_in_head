# Words In Head

这是一个用于学习和记忆单词的Python程序。它通过交互式的方式帮助用户记忆单词和短语，并提供了语音朗读功能。以下是该程序的亮点和主要功能。

## 亮点

1. **数据全面**：程序支持导入包含单词、短语、词性、音标等信息的JSON数据文件，确保学习内容的丰富性和全面性。
2. **背单词效果好**：通过随机打乱单词顺序、语音朗读、错误记录等功能，帮助用户高效记忆单词。
3. **交互式学习**：用户可以通过命令行与程序交互，选择学习单元和学习模式（学习模式或测试模式）。
4. **语音朗读**：程序集成了`pyttsx3`库，支持单词和短语的语音朗读，帮助用户更好地掌握发音。
5. **错误记录**：程序会自动记录用户出错的单词和短语，并在后续的学习中重点复习，确保用户掌握所有内容。

## 主要功能

- **单词学习**：用户可以学习指定单元的单词，程序会随机打乱单词顺序，并提供语音朗读功能。
- **短语学习**：用户可以学习指定单元的短语，程序会随机打乱短语顺序，并提供语音朗读功能。
- **错误复习**：程序会自动记录用户出错的单词和短语，并在后续的学习中重点复习。
- **学习模式与测试模式**：用户可以选择学习模式（显示正确答案）或测试模式（不显示正确答案）。

## 使用方法

### 1. 安装依赖

在运行程序之前，请确保已安装以下Python库：

```bash
pip install pyttsx3 colorama tabulate
```

### 2. 下载语言包

程序使用了微软的语音引擎，需要下载并安装对应的语言包。请前往以下链接下载并安装 **MSSpeech_TTS_en-GB_Hazel.msi** 文件：

[微软语言包下载地址](https://www.microsoft.com/en-us/download/details.aspx?id=27224)

下载完成后，运行安装程序并按照提示完成安装。

### 3. 准备数据文件

程序已经提供了一个名为 `data.json` 的数据文件，包含单词和短语的信息。你无需自己创建数据文件，直接使用项目中的 `data.json` 即可。

### 4. 运行程序

编写main.py文件，注意读取数据文件时文件路径建议使用绝对路径，然后运行程序.我们为您准备了main文件的编写范例，以展示如何使用我的fast_view库：

```python
from fast_view import fast_view, clear_input_buffer, clear
from time import sleep
import json


# 请将以下路径替换为你的 data.json 文件的绝对路径
data_path = "PATH_TO_YOUR_WORKSPACE/data.json"

with open(data_path, encoding='UTF-8') as f:
    data = json.load(f)


while True:
    learning = False
    clear_input_buffer()

    user_input = input('输入: (单元 [学习?(true/false)]): ').strip().lower()

    try:
        if len(user_input) == 1:
            unit = int(user_input)
        elif len(user_input) == 2:
            unit, learning = int(user_input[0]), bool(user_input[1])
        else:
            print('输入长度错误(length = 1 or 2)')
            sleep(1)
            clear()
            continue
    except ValueError:
        print('输入错误(ValueError)')
        sleep(1)
        clear()
        continue

    fast_view(data[f'unit{unit}'], learning=learning)

```

### 5. 输入指令

程序运行后，用户可以通过输入指令来选择学习单元和学习模式。例如：

- 输入 `1`：学习第1单元，默认进入测试模式。
- 输入 `1 true`：学习第1单元，并进入学习模式（显示正确答案）。

## 项目结构

```
.
├── README.md
├── fast_view.py
└── data.json
```

- `fast_view.py`：主程序文件，包含单词学习的核心逻辑。
- `data.json`：数据文件，包含单词和短语的信息（已提供在项目中）。

## 依赖库

- `pyttsx3`：用于语音朗读。
- `colorama`：用于在控制台中输出彩色文本。
- `tabulate`：用于格式化输出表格。

## 注意事项

- 请尽量使用 **绝对路径** 来指定 `data.json` 文件的位置，以避免路径错误。
- 如果语音朗读功能无法正常工作，请确保已正确安装并启用了 **MSSpeech_TTS_en-GB_Hazel.msi** 语音包。(看看读音是否僵硬，且是否与展示音标一致)
