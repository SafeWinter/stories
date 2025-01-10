# 利用 Python 脚本批量创建空白 Markdown 笔记



## 1 背景介绍

我学视频课有个习惯：每学完一节课，就相应创建一个 `Markdown` 格式的纯文本自学笔记，方便日后查阅。久而久之，要创建的笔记文件越来越多，如果再要求这些文件都具备统一的格式（例如文件名的命名风格、统一的标题模板等等），无形中就会多出不少工作量。之前我都是用 `PowerShell + ChatGPT` 来批量生成这些文件夹和文件名，虽然脚本编写比较繁琐，但可以一劳永逸，倒也划算；前段时间入坑 `Python`，正好可以练练文件操作和正则表达式，才发现 `Python` 处理起这类问题来比 `PowerShell` 轻松太多了。



## 2 需求描述

这里随便找了一个视频课，原始的课程目录长这样：

![](assets/1.png)

**图 1：原始课程目录结构（节选）**

复制到一个临时文件 `toc.md` 后长这样：

![](assets/2.png)

**图 2：复制到临时文件 toc.md 后的课程目录（节选）**

而我想要的效果，是用 `Python` 脚本批量生成这样的文件结构：

![](assets/3.png)

**图 3：最终希望实现的笔记目录结构与内容模板**



## 3 明确思路

再复杂的需求也可以拆分成若干个可以轻松实现的单元。多行的批量处理可以先简化为某一行的处理：

1. 读取 `toc.md` 的某一行，赋给一个变量 `line`；
2. 判定 `line` 是按文件夹处理，还是按 `.md` 文件处理（通过正则表达式判定）；
   1. 是文件夹：
      1. 创建该文件夹；
      2. 提取章节编号（如 `Ch01`），以便本章笔记文件使用；
      3. 重置笔记文件的二级目录编号（比如上一行编号为 `Ch01.2`，这一行需要重置为 `Ch2.1`）
   2. 是文件：
      1. 获取当前章节编号，生成对应的文件名
      2. 获取当前章节编号，生成对应的 `Markdown` 文本内容
      3. 二级目录编号递增 `1`
3. 遍历完 `toc.md` 后，根据文件名是否以 `.md` 结尾，可以判定生成的是文件甲还是 `Markdown` 文件：
   1. 是文件夹：创建该文件夹，并更新当前路径（`curr_path`，以便后续笔记文件引用）；
   2. 是文件：根据当前路径生成对应的笔记文件，同时写入文本内容。



## 4 具体实现

### 4.1. 遍历 toc.md 文件，收集文件名和对应的文件内容

创建 `Python` 脚本文件 `generate_files.py`，确定信息采集逻辑：

```python
def make_chapter(line):
    pass
def make_section(line, num):
    pass

# 参数初始化
chp_num = '0'  # 章节号
sec_num = 1    # 小节号
(contents, file_names) = ([], []) # 初始化章节内容、文件名

# 读取课程目录文件
with open('./toc.md', 'r') as f:
    # 读取文件的每一行，去掉行尾的换行符，然后存入列表 lines
    lines = [l.strip() for l in f.readlines()] 
    
    for line in lines:
        # 判断行首是否是数字，如果是，说明是章节标题
        starts_with_digit = re.match(r'^(\d+)\.', line)
        
        if starts_with_digit:
            # 如果是章节标题，则生成该章节的 文件名 和 章节号
            (file_name, chapter_num) = make_chapter(line)
            
            # 添加本章的章节内容（仅占位用，文件夹没有文本内容）
            contents.append('placeholder')
            
            # 添加本章的文件名
            file_names.append(file_name)
            
            # 更新章节号
            chp_num = chapter_num
        else:
            # 如果不是章节标题，则生成该小节的 文本内容 和 文件名
            (sec_file_name, sec_content) = make_section(line, chp_num, sec_num)
            
            # 添加该小节的文本内容
            file_names.append(sec_file_name)
            
            # 添加该小节的文件名
            contents.append(sec_content)
        
        # 按本行的实际作用动态更新小节编号
        sec_num = 1 if starts_with_digit else (sec_num + 1)
```

注意：`make_chapter` 函数（L1、L22）和 `make_section` 函数（L3、L34）暂不实现，先确定大流程。



### 4.2. 实现文件批量生成逻辑

利用 4.1 的信息采集逻辑，就可以批量生成文件/文件夹了：

```python
# 批量生成文件
curr_path = ''
for index, (file_or_path, cont) in enumerate(zip(file_names, contents)):
    if file_or_path.endswith('.md'):
        file = file_or_path
        with open(f'./{curr_path}/{file}', 'w') as f:
            f.write(cont + '\n')
    else:
        path = file_or_path
        os.makedirs(path, exist_ok=True)
        curr_path = path
```



### 4.3. 补全缺失的工具函数

大流程确定后，再来实现 `make_chapter` 函数和 `make_section` 函数：

```python
#!/usr/bin/env python

import re
import os

def dashed(s, sep=' '):
    pass

def sanitize_filename(s):
    pass

def repl(match):
    pass

def make_chapter(line):
    """Generates the specific file name and the corresponding chapter number for this chapter.

    Args:
        line (string): The original line of text to be processed.

    Returns:
        tuple: A tuple containing the file name and the chapter number.
    
    Example:
        Input: 
            line: '1. Getting Started with GitHub Actions'
        Output: 
            ('Ch01_Getting_Started_with_GitHub_Actions.md', '1')
    """
    
    pttn = r'(\d+)\.(.*)'
    re.findall(pttn, line)
    file_name = re.sub(pttn, repl, line)
    chapter_num = re.sub(pttn, r'\1', line)   
    return (file_name, chapter_num)

def make_section(line, chapter_num, section_num):
    """Generates the specific file name and corresponding content for this section.

    Args:
        line (string): The original line of text to be processed.
        chapter_num (string): The current chapter number.
        section_num (int): The current section number.
        
    Returns:
        tuple: A tuple containing the file name and the content of the section.
        
    Example:
        Input: 
            line: '   - Welcome to the Course!'
            chapter_num: '1'
            section_num: 1
        Output: 
            ('Ch01_1_Introduction_to_the_Course.md', '## Ch01.1 Introduction to the Course')
    """
    
    line = line.strip('- ')
    header_part = f'Ch{chapter_num.zfill(2)}_{section_num}'
    content_part = dashed(line, '_').replace('---', '_')
    file_name = f'{header_part}_{content_part}'
    title_content = f'## Ch{chapter_num.zfill(2)}.{section_num} {line}'
    return (f'{sanitize_filename(file_name)}.md', title_content)
```



### 4.4. 进一步补全工具函数中的工具函数

为了方便管理，再对工具函数中出现的几个工具函数做进一步实现：

```python
def dashed(s, sep=' '):
    """Removes leading and trailing whitespaces and replaces 
        all other whitespaces with the specified separator.

    Args:
        s (str): The original string to be processed
        sep (str, optional): The separator string. Defaults to ' '.

    Returns:
        string: The processed string.
    """
    
    return sep.join(s.strip().split())

def sanitize_filename(s):
    """Sanitizes the file name by removing all characters except letters, numbers, underscores, and dots.

    Args:
        s (string): The original file name to be sanitized.

    Returns:
        string: The sanitized file name.
    """
    
    # 只保留字母、数字、下划线和点，其他字符都删除
    pttn = r'[^\w -]'
    re.findall(pttn, s)
    return re.sub(pttn, '', s)

def repl(match):
    """Generates the specific file name for this chapter.

    Args:
        match (Match[string]): The matched object from the regular expression.

    Returns:
        string: The file name for this chapter.
    """
    num = match.group(1)
    content = match.group(2)
    file_name = f'Ch{num.zfill(2)}_{dashed(content, "_")}'
    return sanitize_filename(file_name)
```



## 5 脚本运行

使用以下命令运行脚本：

```bash
python generate_files.py
```

不到两秒，就生成了所有的文件夹和 `Markdown` 空白文件：

![](assets/4.png)

**图 4：检查最终的批量生成结果（符合预期）**



## 6 注意事项

由于是第一次尝试 `Python` 脚本，调试过程中走了不少弯路，这里集中梳理一下：

1. 一定要小步走，多迭代；
2. 按抽象层次依次实现每一层的函数逻辑，方便后续管理；
3. 读取每一行文本都会包含一个 `\n` 换行符，需要用 `str.strip()` 处理掉；
4. 先用 `re.findall` 捕获匹配结果，然后再用 `re.sub` 执行替换，否则后者始终输出空字符串；
5. 访问捕获的结果时，注意 `f-string` 和 `r-string` 中反斜杠 `\` 的不同写法，前者要写成 `\\`，而后者直接写成 `\` 即可；
6. 脚本运行前提前做好备份（以避免 `rm -Recurse -Force *` 把 `Python` 脚本文件本身也删没了的杯具。。）；
7. 尽量避免引用全局变量，多用参数传参（本例必须使用全局变量，以实时获取当前的文件夹名称和路径）；
8. 主体框架确定后，今后只需要修改文件夹和文件的处理逻辑，就可以适应不同的原始数据。
9. `os.makedirs(path, exist_ok=True)` 中的 `exist_ok` 参数用于控制在指定路径已经存在时的行为：
   1. 当 `exist_ok=True` 时，如果目标目录已经存在，`makedirs` 不会抛出异常（本例暂不涉及）；
   2. 当 `exist_ok=False`（默认值）时，如果目标目录已存在，则会抛出 `FileExistsError` 异常。
