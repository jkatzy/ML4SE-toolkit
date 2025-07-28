"""
异步编程示例文件
展示了Python中的异步编程特性
"""

import asyncio
import time

async def say_after(delay, what):
    """异步等待指定时间后打印消息"""
    await asyncio.sleep(delay)
    print(what)

async def main_async():
    """主异步函数"""
    print(f"开始时间: {time.strftime('%X')}")
    
    # 创建任务
    task1 = asyncio.create_task(say_after(1, '任务1完成'))
    task2 = asyncio.create_task(say_after(2, '任务2完成'))
    
    # 等待任务完成
    await task1
    await task2
    
    print(f"结束时间: {time.strftime('%X')}")

async def fetch_data(url):
    """模拟异步获取数据"""
    print(f"开始从{url}获取数据")
    await asyncio.sleep(1)  # 模拟网络延迟
    print(f"从{url}获取数据完成")
    return f"来自{url}的数据"

async def process_data():
    """并发处理多个数据源"""
    urls = [
        "https://api.example.com/data1",
        "https://api.example.com/data2",
        "https://api.example.com/data3"
    ]
    
    # 并发执行所有任务
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    # 处理结果
    for i, result in enumerate(results):
        print(f"处理结果 {i+1}: {result}")

# 测试代码
if __name__ == "__main__":
    print("运行异步示例1:")
    asyncio.run(main_async())
    
    print("\n运行异步示例2:")
    asyncio.run(process_data())