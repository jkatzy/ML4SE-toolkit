"""
递归算法示例文件
展示了几种常见的递归算法实现
"""

def factorial(n):
    """计算阶乘的递归实现"""
    if n <= 1:
        return 1
    return n * factorial(n-1)

def fibonacci(n):
    """计算斐波那契数列的递归实现"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

def binary_search(arr, target, left, right):
    """二分查找的递归实现"""
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, left, mid-1)
    else:
        return binary_search(arr, target, mid+1, right)

# 测试代码
if __name__ == "__main__":
    print(f"5的阶乘是: {factorial(5)}")
    print(f"斐波那契数列第8项是: {fibonacci(8)}")
    
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]
    target = 7
    result = binary_search(sorted_array, target, 0, len(sorted_array)-1)
    print(f"目标值{target}在数组中的索引是: {result}")