#!/usr/bin/env python

import re
import os

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