# 英语单词学习工具 - Words In Head

## 项目简介
本工具是为初中学生设计的英语单词和短语学习程序，提供「学习模式」和「记忆模式」两种模式，支持语音朗读、首字母提示、错题循环练习等功能。数据覆盖初一上下学期共16个单元，可自由组合学习范围。

---

## 功能特性
- **双模式学习**
  - **学习模式**：显示完整单词信息，适合初次学习
  - **记忆模式**：隐藏拼写，通过首字母提示辅助回忆
- **语音朗读**：使用Hazel标准英音朗读单词
- **进度追踪**：实时显示剩余词数和错误计数
- **错题循环**：自动收集错题并循环练习直到完全掌握
- **单元组合**：支持按单元/学期/自定义范围学习
- **跨平台支持**：兼容Windows/macOS/Linux

---

## 文件结构
```bash
.
├── main.py                 # 程序主入口
├── fast_view.py            # 核心学习逻辑实现
├── handle_configuration_files.py # 配置解析器
├── profiles/
│   └── configurations.json # 学习单元配置文件
├── data/
│   ├── data_of_the_first_semester_of_junior_high_school.json   # 初一上学期数据
│   └── data_of_the_second_semester_of_junior_high_school.json  # 初一下学期数据
└── README.md               # 本说明文件
```

---

## 快速开始

### 环境要求
- Python 3.7+
- 依赖库：`colorama`, `tabulate`, `pyttsx3`

### 安装依赖
```bash
pip install colorama tabulate pyttsx3
```

### 安装Hazel语音包
- Windows用户：

  1. 下载Hazel[语音包](https://www.microsoft.com/en-us/download/details.aspx?id=27224)
  2. 安装后重启系统
  3. 在`fast_view.py`中修改`voice`变量为`Hazel`

- macOS用户：
  - 无需额外安装
  - 在`fast_view.py`中修改`voice`变量为`Microsoft Hazel Desktop - English (United States)`

### 运行程序
```bash
python main.py
```

---

## 配置说明
### 配置文件位置
`profiles/configurations.json`

### 配置示例
```json
{
  "name": "初一上U1-U4百词大过关",
  "learning_mode": false,
  "other_args": {"first_letter_tip": "true"},
  "content": [
    {
      "data_file_name": "data_of_the_first_semester_of_junior_high_school.json",
      "units_keys": ["unit1", "unit2", "unit3", "unit4"]
    }
  ]
}
```

### 配置参数说明
| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | String | 配置显示名称 |
| `learning_mode` | Boolean | 学习模式开关 |
| `other_args.first_letter_tip` | Boolean | 首字母提示功能 |
| `content.data_file_name` | String | 数据文件路径 |
| `content.units_keys` | Array/String | 指定单元(支持数组或单个字符串) |

---

## 使用示例
1. 启动程序后选择配置文件：
   ```
   Available profiles:
   1. 初一全部单词
   2. 初一上u1单词(学习模式)
   3. 初一上u1单词(记忆模式)
   ...（其他配置省略）
   ```
   
2. **学习模式界面**：
   ```
    --words--   剩下: 27 错: 0
    
    
    
    word        phonetic_symbol    meaning    part_of_speech
    ----------  -----------------  ---------  ----------------
    friendship  /'frendfip/        友谊；朋友关系    n.
    按回车继续
   ```
   
3. **记忆模式界面**：
   ```
   --words--   剩下: 27 错: 0

   
   
    n.尊敬；尊重:
   ```

---

## 常见问题

### Q1: 语音朗读不工作
- 检查系统语音引擎是否正常
- Windows用户建议安装Hazel[语音包](https://www.microsoft.com/en-us/download/details.aspx?id=27224)
- 修改fast_view中的变量`voice`使用自定义语音包

### Q2: 提示数据文件找不到
- 确认`data/`目录存在且包含两个学期数据文件
- 检查`configurations.json`中的路径配置

---

## 扩展开发
1. **添加新数据**：
   - 在`data/`目录新建JSON文件
   - 格式参照现有数据文件，按单元结构组织

2. **创建新配置**：
   - 修改`configurations.json`
   - 添加新配置项并指定数据文件和单元

---

> 提示：程序运行时可按 `Ctrl+C` 随时退出学习流程。
