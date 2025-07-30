import os
import re
from datasets import load_dataset_builder, load_from_disk
import pandas as pd

# 主目录
main_dir = 'datasets/multipl-e'
# 输出目录
output_base_dir = 'extracted_multipl_e_files'

# 确保输出基础目录存在
os.makedirs(output_base_dir, exist_ok=True)

# 获取所有已下载的数据集目录
dataset_dirs = [d for d in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, d))]

for dataset_name in dataset_dirs:
    print(f"正在处理数据集: {dataset_name}")
    
    # 创建对应的输出目录
    output_dir = os.path.join(output_base_dir, dataset_name)
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 加载本地保存的数据集
        dataset_path = os.path.join(main_dir, dataset_name)
        dataset = load_from_disk(dataset_path)
        
        # 获取数据集的第一个分割（通常是"test"）
        split_name = list(dataset.keys())[0]
        data = dataset[split_name]
        
        # 将数据集转换为DataFrame以便处理
        df = pd.DataFrame(data)
        
        # 确定文件扩展名
        lang = dataset_name.split('-')[-1]
        extension_map = {
            'adb': '.adb',  # Ada
            'clj': '.clj',  # Clojure
            'cpp': '.cpp',  # C++
            'cs': '.cs',    # C#
            'd': '.d',      # D
            'dart': '.dart', # Dart
            'elixir': '.ex', # Elixir
            'go': '.go',    # Go
            'hs': '.hs',    # Haskell
            'java': '.java', # Java
            'jl': '.jl',    # Julia
            'js': '.js',    # JavaScript
            'lua': '.lua',  # Lua
            'ml': '.ml',    # OCaml
            'php': '.php',  # PHP
            'pl': '.pl',    # Perl
            'r': '.r',      # R
            'rb': '.rb',    # Ruby
            'rkt': '.rkt',  # Racket
            'rs': '.rs',    # Rust
            'scala': '.scala', # Scala
            'sh': '.sh',    # Shell
            'swift': '.swift', # Swift
            'ts': '.ts',    # TypeScript
        }
        
        file_ext = extension_map.get(lang, '.txt')
        
        # 处理每一行数据
        for index, row in df.iterrows():
            # 获取必要的字段
            task_id = row.get('task_id', f'task_{index}')
            prompt = row.get('prompt', '')
            canonical_solution = row.get('canonical_solution', '')
            entry_point = row.get('entry_point', '')
            
            # 创建文件名
            safe_filename = re.sub(r'[^\w\-_.]', '_', task_id) + file_ext
            file_path = os.path.join(output_dir, safe_filename)
            
            # 组合内容
            content = f"""# Task ID: {task_id}
# Entry Function: {entry_point}

# Problem Description:
\"\"\"
{prompt}
\"\"\"

# Solution:
{canonical_solution}

"""
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"已创建文件: {file_path}")
        
        print(f"已为 {dataset_name} 创建 {len(df)} 个文件")
        
    except Exception as e:
        print(f"处理 {dataset_name} 时出错: {str(e)}")
    
    print("-" * 50)

print("所有数据集处理完成！")