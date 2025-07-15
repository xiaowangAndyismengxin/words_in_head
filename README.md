# Words In Head

## 目录
1. [简介](#简介)
2. [功能特性](#功能特性)
3. [依赖库](#依赖库)
4. [使用方法](#使用方法)
5. [单词库（JSON文件）格式说明](#单词库json文件格式说明)
6. [单词本配置文件（profile 文件）格式说明](#单词本配置文件profile-文件格式说明)
7. [代码结构](#代码结构)
8. [注意事项](#注意事项)
9. [贡献与反馈](#贡献与反馈)


## 简介
Words In Head 是一个功能丰富的单词学习命令行程序，简单有效，支持多种学习模式，如快速查看、练习、听写和学习。程序具备语音朗读功能，支持中英文发音，并且能够缓存语音文件以提高性能。同时，它允许用户选择不同的单词本（word book）和学习单元，还可以切换英语发音（英音/美音）。


## 功能特性
1. **多种学习模式**：提供快速查看、练习、听写和学习四种学习模式，满足不同学习需求。
2. **语音朗读**：支持中英文语音朗读，可选择英音或美音。
3. **语音缓存**：将语音文件缓存到本地，减少重复生成语音的时间。
4. **错误记录与复习**：在学习过程中记录错误的单词和短语，并循环练习直到全部掌握。
5. **多单词本支持**：可以加载多个单词本，并选择不同的学习单元。
6. **配置文件支持**：通过配置文件灵活管理单词本和学习内容。


## 依赖库
- `colorama`：用于终端颜色输出。
- `edge-tts`：用于语音合成。
- `pygame`：用于音频播放。
- `tabulate`：用于表格输出。
- `tqdm`：用于进度条显示。


## 使用方法
### 配置文件
- `settings.json`：配置语音相关设置，如默认语音模型、英语发音（英音/美音）、听写延迟等。
- `profiles` 目录：存放单词本的配置文件，支持手动和自动生成单词列表。

### 运行程序
为避免因系统中存在多个Python版本导致调用错误，推荐创建启动文件并使用Python绝对路径：

1. **Windows 系统**：  
   在程序根目录创建 `start.bat` 文件，内容如下（需替换为你的Python安装路径）：
   ```bat
   @echo off
   "C:\Program Files\Python313\python.exe" main.py  # 替换为你的Python绝对路径
   pause  # 程序结束后暂停，方便查看报错信息
   ```
   双击 `start.bat` 即可运行。

2. **Linux/macOS 系统**：  
   在程序根目录创建 `start.sh` 文件，内容如下（需替换为你的Python安装路径）：
   ```bash
   #!/bin/bash
   /usr/local/bin/python3 main.py  # 替换为你的Python绝对路径
   read -p "按回车退出..."  # 程序结束后暂停，方便查看报错信息
   ```
   赋予执行权限并运行：
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

### 安装依赖（补充说明）
若需安装依赖库，同样建议使用绝对路径确保环境正确（以Windows为例）：
```bat
"C:\Program Files\Python313\python.exe" -m pip install colorama edge-tts pygame tabulate tqdm
```
（Linux/macOS 替换为对应的Python绝对路径，如 `/usr/local/bin/python3 -m pip install ...`）

### 操作指南
1. **选择单词本和学习单元**：程序启动后，会显示可用的单词本和学习单元，输入对应的序号选择要学习的内容。
2. **选择学习模式**：进入学习单元后，可选择快速查看、练习、听写或学习模式。
3. **其他操作**：
    - `a`：返回上一页。
    - `b`：回到首页。
    - `c`：改变英语发音（英音/美音）。
    - `d`：清空语音缓存。
    - `q`：退出程序。


## 单词库（JSON文件）格式说明
单词库以JSON格式存储，**需放置在项目根目录的 `data` 文件夹中**，核心结构如下：

### 1. 最外层结构
- 整体是一个**对象（Object）**，用`{}`包裹。
- 内部包含多个自定义键值对，键名可根据需求自定义（如按单元分组用`"unit1"` `"unit2"`，按部分分组用`"part1"` `"part2"`等）。

### 2. 自定义键的值结构
每个自定义键的值是一个**对象（Object）**，包含以下可选键：
- `words`：存储单词的数组（Array），若没有单词可省略。
- `phrases`：存储短语的数组（Array），若没有短语可省略。

### 3. 单词的具体格式
`words` 数组中的每个元素是一个**对象（Object）**，**必须包含以下字段**：
- `word`：单词的拼写。
- `meaning`：中文释义。
- `part_of_speech`：词性（如 `"n."` 表示名词，`"v."` 表示动词）。
- `phonetic_symbol`：音标（你能看得懂的音标，如 `/ˈæpl/`）。

**扩展说明**：  
可根据需求添加自定义字段（如 `example` 例句、`synonym` 同义词等），程序在展示详细信息时会自动显示这些字段。

### 4. 短语的具体格式
`phrases` 数组中的每个元素是一个**对象（Object）**，**仅需包含以下必填字段**：
- `phrase`：短语的拼写。
- `meaning`：中文释义。

**可选字段**（完全按需添加，不强制）：
- `part_of_speech`：词性（如 `"phr."` 表示短语）。
- `phonetic_symbol`：音标。
- `example`：例句等扩展信息。


### 示例（单词库JSON文件，路径：`data/grade_1_vocab.json`）
```json
{
    "unit1": {
        "words": [
            {
                "word": "apple",
                "meaning": "苹果",
                "part_of_speech": "n.",
                "phonetic_symbol": "/ˈæpl/",
                "example": "I eat an apple every day."
            },
            {
                "word": "run",
                "meaning": "跑",
                "part_of_speech": "v.",
                "phonetic_symbol": "/rʌn/"
            }
        ],
        "phrases": [
            {
                "phrase": "run out of",
                "meaning": "用完，耗尽"
                // 无任何可选字段，符合基础要求
            },
            {
                "phrase": "look forward to",
                "meaning": "期待",
                "example": "I look forward to your reply."
                // 仅添加例句，无词性和音标
            }
        ]
    },
    "part2": {
        "words": [
            {
                "word": "book",
                "meaning": "书",
                "part_of_speech": "n.",
                "phonetic_symbol": "/bʊk/"
            }
        ]
        // 此处省略phrases，表示该部分无短语
    }
}
```

### 注意事项
- 键名（如 `unit1` `part2`）可自定义，但后续配置文件中需使用相同的键名调用对应内容。
- 单词的字段名（如 `word` `meaning` `part_of_speech` `phonetic_symbol`）需严格匹配，否则程序可能无法正确识别。
- 短语仅强制要求 `phrase` 和 `meaning`，其他字段（词性、音标等）均为可选，不影响程序运行。
- 空值处理：若某部分无单词或短语，可直接省略 `words` 或 `phrases` 键。


## 单词本配置文件（profile 文件）格式说明
每个 `profile` 文件对应一个单词本（word book），需放在项目根目录的 `profiles` 文件夹中。文件名可根据单词本主题自定义（如 `school_vocab_word_book.json`、`daily_expressions_word_book.json`）。


### 核心概念
- **单词本（word book）**：整个 `profile` 文件代表一个单词本，包含多个「组」或直接可学习的「元素」。
- **组（group）**：`content` 数组中的一个配置项，用于归类多个学习内容，通常有明确的名称（如「基础单元」「重点短语」）。
- **元素（element）**：组内的具体学习内容，由单词库中的单元组合而成（如合并 `unit1` 和 `unit2` 形成的学习单元）。


### 基本结构
文件最外层为一个**对象（Object）**，包含以下两个键：
- `book_name`：字符串类型，表示单词本的名称（如「小学英语单词本」）。
- `content`：数组类型，包含多个配置项（每个配置项为一个「组」或直接可学习的「元素」）。


### 配置项详解（`content` 数组中的元素）
每个配置项是一个**对象**，分为「带分组的配置」和「无分组的直接学习元素」两种类型：


#### 1. 带分组的配置（有 `name` 和 `generate_method`）
适用于需要归类的学习内容，需指定 `name`（组名称）和 `generate_method`（生成方式）。

##### 1.1 自动生成模式（`generate_method: "auto"`）
适用于按规则自动组合**单个单词库**中的单元（不支持跨文件），直接通过 `data_file_name` 和 `unit_keys` 定义内容，无需额外嵌套 `name` 和 `content` 层级，结构如下：

```json
{
  "name": "组名称（如「入门单元1-2」）",
  "generate_method": "auto",
  "content": {  // 直接定义内容，无额外嵌套
    "data_file_name": "单词库文件名（位于data目录，如primary_vocab.json）",
    "unit_keys": ["unit1", ["unit2", "unit3"]],  // 支持字符串/数组/嵌套数组
    "connection": "连接词（可选，默认'and'，如'和'）"
  }
}
```

**参数说明**：
- `data_file_name`：指定单个单词库文件（仅支持一个文件，不跨文件）。
- `unit_keys`：该文件中需要包含的单元键，格式支持：
  - 字符串：单个单元（如 `"unit1"`）。
  - 数组：多个独立单元（如 `["unit1", "unit2"]`）。
  - 嵌套数组：合并多个单元为一组（如 `["unit1", ["unit2", "unit3"]]`，表示「unit1、unit2和unit3」）。
- `connection`：嵌套数组中合并单元的连接词（如用「-」则显示「unit2 - unit3」），是会自动在两侧加空格的。

##### 1.2 手动生成模式（`generate_method: "manual"`）
适用于灵活聚合多个单词库中的单元（支持跨文件组合），也适用于指定特殊的元素。配置结构需包含**元素名称**和**具体来源配置**，层级如下：

```json
{
  "name": "组名称（如「跨教材核心词」）",
  "generate_method": "manual",
  "content": {  // 可写单个元素对象，或数组（包含多个元素对象）
    "name": "元素名称（如「小学+初中基础词」）",
    "content": [  // 可以是数组形式，聚合多个单词库的单元。也可以是单个集合。
      {
        "data_file_name": "单词库文件名1（如primary_vocab.json）",
        "unit_keys": "unit4"  // 单个单元（字符串）
      },
      {
        "data_file_name": "单词库文件名2（如common_phrases.json）",
        "unit_keys": ["daily", "travel"]  // 多个单元（数组）
      },
      {
        "data_file_name": "单词库文件名3",
        "unit_keys": ["unit1", "unit2", "unit3"]
      }
    ]
  }
}
```
**content 中（其中一个）元素参数说明**：
- `name`（元素名称）：用于标识该元素的名称（如「日常用语+考试高频词」），必填。
- `content`（元素内容）：可以是数组，可以是对象，数组每个元素是一个对象，包含：
  - `data_file_name`：单词库文件名（位于 `data` 目录）。
  - `unit_keys`：该文件中需要包含的单元键，支持字符串（单个单元）、数组（多个单元）

#### 2. 无分组的直接学习元素（`name: null`，无 `generate_method`）
适用于无需分组、点击后直接进入学习的内容，**必须设置 `name: null` ，建议不写 `generate_method`**，content内的元素写法与 `manual` 下差不多：

```json
{
  "name": null,
  "content": { // 数组也行，多个元素平铺
    "name":"学习u1", // 此处与 manual 下元素设置一样。
    "content": {
      "data_file_name": "grade_1_vocab",
      "unit_keys": "u1"
    }
  }
}
```


### 示例（`profiles/junior_1_word_book.json`）
```json
{
  "book_name": "初一英语单词本",
  "content": [
    {
      "name": "初一上各单元单词",
      "generate_method": "auto",
      "content": {
        "data_file_name": "grade_7_second_semester_vocab.json",
        "unit_keys": [
          "unit1",
          "unit2",
          "unit3",
          "unit4",
          "unit5",
          "unit6",
          "unit7",
          "unit8"
        ]
      }
    },
    {
      "name": "初一下各单元单词",
      "generate_method": "auto",
      "content": {
        "data_file_name": "grade_7_first_semester_vocab.json",
        "unit_keys": [
          "unit1",
          "unit2",
          "unit3",
          "unit4",
          "unit5",
          "unit6",
          "unit7",
          "unit8"
        ]
      }
    },
    {
      "name": "初一上百词大过关",
      "generate_method": "manual",
      "content": [
        {
          "name": "初一上U1-U4百词大过关",
          "content": {
            "data_file_name": "grade_7_second_semester_vocab.json",
            "unit_keys": [
              "unit1",
              "unit2",
              "unit3",
              "unit4"
            ]
          }
        },
        {
          "name": "初一上U5-U8百词大过关",
          "content": {
            "data_file_name": "grade_7_second_semester_vocab.json",
            "unit_keys": [
              "unit5",
              "unit6",
              "unit7",
              "unit8"
            ]
          }
        }
      ]
    },
    {
      "name": "初一下百词大过关",
      "generate_method": "manual",
      "content": [
        {
          "name": "初一下U1-U4百词大过关",
          "content": {
            "data_file_name": "grade_7_first_semester_vocab.json",
            "unit_keys": [
              "unit1",
              "unit2",
              "unit3",
              "unit4"
            ]
          }
        },
        {
          "name": "初一下U5-U8百词大过关",
          "content": {
            "data_file_name": "grade_7_first_semester_vocab.json",
            "unit_keys": [
              "unit5",
              "unit6",
              "unit7",
              "unit8"
            ]
          }
        }
      ]
    }
  ]
}
```


## 代码结构
### 主要文件和模块
- `main.py`：程序入口，负责初始化命令行程序和处理用户交互。
- `word_learner.py`：单词学习核心功能模块，提供学习、听写和浏览等功能。
- `voice_player_with_cache.py`：支持语音缓存的语音播放器，负责语音合成和播放（短语默认不朗读，有音标时触发）。
- `handle_configuration_files.py`：处理配置文件，解析单词本和学习内容。
- `handle_word_books.py`：解析所有单词本的内容。
- `settings.json`：配置文件，存储语音和其他设置。
- `data/`：存放单词库JSON文件的目录。
- `profiles/`：存放单词本配置文件的目录。
- `voice_cache/`：存放语音缓存文件的目录，用于存储生成的语音文件以提高性能。
- `audios/`：存放内置音频文件（如听写开始提示音 `dictation_audio-ready_go.wav`）。


## 注意事项
- 确保 `profiles` 目录下的配置文件格式正确，否则可能会导致程序报错。
- 语音缓存文件存储在 `voice_cache` 目录下，可定期清理以释放磁盘空间。
- 听写功能需要 `audios/dictation_audio-ready_go.wav` 文件，如果该文件缺失，可能会影响听写开始提示音的播放。
- 短语默认无读音，若需朗读，需在短语对象中添加 `phonetic_symbol` 字段。


## 贡献与反馈
如果你发现任何问题或有改进建议，请在代码库的 `Issues` 页面提交问题，或提交 `Pull Request` 贡献代码。
