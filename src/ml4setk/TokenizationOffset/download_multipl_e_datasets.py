from datasets import load_dataset
import os
import time

# 所有可用的配置
configs = [
    'humaneval-adb', 'humaneval-clj', 'humaneval-cpp', 'humaneval-cs', 'humaneval-d', 
    'humaneval-dart', 'humaneval-elixir', 'humaneval-go', 'humaneval-hs', 'humaneval-java', 
    'humaneval-jl', 'humaneval-js', 'humaneval-lua', 'humaneval-ml', 'humaneval-php', 
    'humaneval-pl', 'humaneval-r', 'humaneval-rb', 'humaneval-rkt', 'humaneval-rs', 
    'humaneval-scala', 'humaneval-sh', 'humaneval-swift', 'humaneval-ts', 'mbpp-adb', 
    'mbpp-clj', 'mbpp-cpp', 'mbpp-cs', 'mbpp-d', 'mbpp-elixir', 'mbpp-go', 'mbpp-hs', 
    'mbpp-java', 'mbpp-jl', 'mbpp-js', 'mbpp-lua', 'mbpp-ml', 'mbpp-php', 'mbpp-pl', 
    'mbpp-r', 'mbpp-rb', 'mbpp-rkt', 'mbpp-rs', 'mbpp-scala', 'mbpp-sh', 'mbpp-swift', 
    'mbpp-ts'
]

# 创建主目录
main_dir = 'datasets/multipl-e'
os.makedirs(main_dir, exist_ok=True)

# 下载并保存每个数据集
for i, config in enumerate(configs):
    print(f"[{i+1}/{len(configs)}] 正在下载 {config}...")
    
    try:
        # 创建配置对应的目录
        config_dir = os.path.join(main_dir, config)
        os.makedirs(config_dir, exist_ok=True)
        
        # 加载数据集
        dataset = load_dataset("nuprl/MultiPL-E", config)
        
        # 保存到本地
        dataset.save_to_disk(config_dir)
        
        print(f"✓ 成功保存 {config} 到 {config_dir}")
        
        # 添加短暂延迟以避免过多请求
        time.sleep(1)
        
    except Exception as e:
        print(f"✗ 下载 {config} 时出错: {str(e)}")
        
    print("-" * 50)

print("所有数据集下载完成！")