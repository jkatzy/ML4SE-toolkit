"""
文件操作示例文件
展示了Python中常见的文件读写操作
"""

import os
import json
import csv
import pickle

def text_file_operations():
    """基本文本文件操作"""
    # 写入文本文件
    with open("temp_text.txt", "w", encoding="utf-8") as f:
        f.write("这是第一行\n")
        f.write("这是第二行\n")
        f.write("这是第三行，包含中文字符\n")
    
    # 读取文本文件
    with open("temp_text.txt", "r", encoding="utf-8") as f:
        content = f.read()
        print("读取整个文件:")
        print(content)
    
    # 逐行读取
    with open("temp_text.txt", "r", encoding="utf-8") as f:
        print("\n逐行读取:")
        for line in f:
            print(f"  {line.strip()}")
    
    # 追加内容
    with open("temp_text.txt", "a", encoding="utf-8") as f:
        f.write("这是追加的第四行\n")
    
    # 清理临时文件
    os.remove("temp_text.txt")
    print("\n临时文本文件已删除")

def json_file_operations():
    """JSON文件操作"""
    # 创建示例数据
    data = {
        "姓名": "张三",
        "年龄": 30,
        "职业": "软件工程师",
        "技能": ["Python", "JavaScript", "SQL"],
        "地址": {
            "城市": "北京",
            "邮编": "100000"
        }
    }
    
    # 写入JSON文件
    with open("temp_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # 读取JSON文件
    with open("temp_data.json", "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
        print("\nJSON数据:")
        print(f"  姓名: {loaded_data['姓名']}")
        print(f"  年龄: {loaded_data['年龄']}")
        print(f"  技能: {', '.join(loaded_data['技能'])}")
        print(f"  城市: {loaded_data['地址']['城市']}")
    
    # 清理临时文件
    os.remove("temp_data.json")
    print("\n临时JSON文件已删除")

def csv_file_operations():
    """CSV文件操作"""
    # 创建示例数据
    data = [
        ["姓名", "年龄", "城市"],
        ["张三", "30", "北京"],
        ["李四", "25", "上海"],
        ["王五", "35", "广州"]
    ]
    
    # 写入CSV文件
    with open("temp_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    # 读取CSV文件
    with open("temp_data.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        print("\nCSV数据:")
        for row in reader:
            print(f"  {', '.join(row)}")
    
    # 使用DictReader读取
    with open("temp_data.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("\n使用DictReader:")
        for row in reader:
            print(f"  {row['姓名']}来自{row['城市']}，{row['年龄']}岁")
    
    # 清理临时文件
    os.remove("temp_data.csv")
    print("\n临时CSV文件已删除")

def binary_file_operations():
    """二进制文件操作"""
    # 创建示例数据
    data = {
        "complex_data": [1, 2, 3, 4, 5],
        "nested_dict": {"key": "value"}
    }
    
    # 使用pickle序列化对象
    with open("temp_data.pkl", "wb") as f:
        pickle.dump(data, f)
    
    # 读取pickle文件
    with open("temp_data.pkl", "rb") as f:
        loaded_data = pickle.load(f)
        print("\nPickle数据:")
        print(f"  complex_data: {loaded_data['complex_data']}")
        print(f"  nested_dict: {loaded_data['nested_dict']}")
    
    # 清理临时文件
    os.remove("temp_data.pkl")
    print("\n临时Pickle文件已删除")

# 测试代码
if __name__ == "__main__":
    print("文件操作示例:")
    text_file_operations()
    json_file_operations()
    csv_file_operations()
    binary_file_operations()