"""
生成器示例文件
展示了Python中生成器的使用方法和优势
"""

def simple_generator(n):
    """简单的生成器函数，生成0到n-1的数字"""
    for i in range(n):
        yield i

def fibonacci_generator(limit):
    """斐波那契数列生成器"""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

def infinite_sequence():
    """无限序列生成器"""
    num = 0
    while True:
        yield num
        num += 1

def file_reader(file_path):
    """文件读取生成器，逐行读取文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.strip()

def pipeline_example():
    """生成器管道示例"""
    # 生成1到10的数字
    def numbers():
        for i in range(1, 11):
            yield i
    
    # 过滤出偶数
    def even_filter(nums):
        for num in nums:
            if num % 2 == 0:
                yield num
    
    # 将数字平方
    def square(nums):
        for num in nums:
            yield num * num
    
    # 构建管道
    pipeline = square(even_filter(numbers()))
    
    # 消费管道
    result = list(pipeline)
    print(f"管道结果: {result}")

def generator_expression_demo():
    """生成器表达式示例"""
    # 生成器表达式
    gen_exp = (x**2 for x in range(10) if x % 2 == 0)
    
    print("使用生成器表达式:")
    for value in gen_exp:
        print(f"  {value}")

def memory_comparison():
    """比较列表和生成器的内存使用"""
    import sys
    
    # 使用列表
    list_comp = [i for i in range(10000)]
    # 使用生成器
    gen_exp = (i for i in range(10000))
    
    list_size = sys.getsizeof(list_comp)
    gen_size = sys.getsizeof(gen_exp)
    
    print(f"\n内存使用比较:")
    print(f"  列表占用内存: {list_size} 字节")
    print(f"  生成器占用内存: {gen_size} 字节")
    print(f"  列表比生成器大约大 {list_size/gen_size:.1f} 倍")

# 测试代码
if __name__ == "__main__":
    # 测试简单生成器
    print("简单生成器:")
    gen = simple_generator(5)
    for i in gen:
        print(f"  {i}")
    
    # 测试斐波那契生成器
    print("\n斐波那契数列:")
    for num in fibonacci_generator(100):
        print(f"  {num}", end=" ")
    print()
    
    # 测试无限序列（只取前10个）
    print("\n无限序列的前10个元素:")
    inf_gen = infinite_sequence()
    for _ in range(10):
        print(f"  {next(inf_gen)}", end=" ")
    print()
    
    # 测试生成器管道
    print("\n生成器管道:")
    pipeline_example()
    
    # 测试生成器表达式
    generator_expression_demo()
    
    # 比较内存使用
    memory_comparison()