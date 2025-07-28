"""
数据结构示例文件
实现了几种基本的数据结构
"""

class Stack:
    """栈的实现"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """入栈"""
        self.items.append(item)
    
    def pop(self):
        """出栈"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        """查看栈顶元素"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        """检查栈是否为空"""
        return len(self.items) == 0
    
    def size(self):
        """返回栈的大小"""
        return len(self.items)

class Queue:
    """队列的实现"""
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """入队"""
        self.items.insert(0, item)
    
    def dequeue(self):
        """出队"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        """检查队列是否为空"""
        return len(self.items) == 0
    
    def size(self):
        """返回队列的大小"""
        return len(self.items)

class Node:
    """链表节点"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """单向链表的实现"""
    def __init__(self):
        self.head = None
    
    def append(self, data):
        """在链表末尾添加节点"""
        new_node = Node(data)
        
        if self.head is None:
            self.head = new_node
            return
        
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        
        last_node.next = new_node
    
    def print_list(self):
        """打印链表"""
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements)

# 测试代码
if __name__ == "__main__":
    # 测试栈
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"栈顶元素: {stack.peek()}")
    print(f"出栈: {stack.pop()}")
    print(f"栈大小: {stack.size()}")
    
    # 测试队列
    queue = Queue()
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")
    print(f"出队: {queue.dequeue()}")
    print(f"队列大小: {queue.size()}")
    
    # 测试链表
    linked_list = LinkedList()
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    print(f"链表: {linked_list.print_list()}")