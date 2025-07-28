"""
装饰器示例文件
展示了Python中装饰器的使用方法
"""

import time
import functools

# 基本装饰器
def timer_decorator(func):
    """计时装饰器：记录函数执行时间"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行时间: {end_time - start_time:.4f} 秒")
        return result
    return wrapper

# 带参数的装饰器
def repeat(n=1):
    """重复执行装饰器：重复执行函数n次"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

# 类装饰器
class Memoize:
    """缓存装饰器：缓存函数结果以避免重复计算"""
    def __init__(self, func):
        self.func = func
        self.cache = {}
        functools.update_wrapper(self, func)
    
    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

# 使用装饰器的示例
@timer_decorator
def slow_function():
    """模拟耗时操作"""
    time.sleep(1)
    return "操作完成"

@repeat(3)
def greet(name):
    """问候函数"""
    return f"你好，{name}！"

@Memoize
def fibonacci(n):
    """计算斐波那契数列（使用缓存提高效率）"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 测试代码
if __name__ == "__main__":
    print("测试计时装饰器:")
    result = slow_function()
    print(f"结果: {result}\n")
    
    print("测试重复执行装饰器:")
    results = greet("张三")
    for i, result in enumerate(results):
        print(f"第{i+1}次结果: {result}")
    print()
    
    print("测试缓存装饰器:")
    start = time.time()
    fib_result = fibonacci(30)
    end = time.time()
    print(f"斐波那契数列第30项: {fib_result}")
    print(f"计算时间: {end - start:.4f} 秒")