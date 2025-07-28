"""
算法示例文件
实现了几种常见的排序和搜索算法
"""

def bubble_sort(arr):
    """冒泡排序"""
    n = len(arr)
    for i in range(n):
        # 每次循环后，最大的元素会"冒泡"到最后
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def selection_sort(arr):
    """选择排序"""
    n = len(arr)
    for i in range(n):
        # 找到未排序部分的最小值
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # 将最小值放到已排序部分的末尾
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(arr):
    """插入排序"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        # 将大于key的元素向右移动
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr

def quick_sort(arr):
    """快速排序"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

def linear_search(arr, target):
    """线性搜索"""
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1

def binary_search_iterative(arr, target):
    """二分查找（迭代版本）"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# 测试代码
if __name__ == "__main__":
    # 测试排序算法
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print(f"原始数组: {test_array}")
    print(f"冒泡排序: {bubble_sort(test_array.copy())}")
    print(f"选择排序: {selection_sort(test_array.copy())}")
    print(f"插入排序: {insertion_sort(test_array.copy())}")
    print(f"快速排序: {quick_sort(test_array.copy())}")
    
    # 测试搜索算法
    sorted_array = [11, 12, 22, 25, 34, 64, 90]
    target = 25
    print(f"线性搜索目标{target}的索引: {linear_search(sorted_array, target)}")
    print(f"二分查找目标{target}的索引: {binary_search_iterative(sorted_array, target)}")