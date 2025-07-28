"""
面向对象编程示例文件
展示了类的继承、多态和封装特性
"""

class Animal:
    """动物基类"""
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def make_sound(self):
        """发出声音"""
        pass
    
    def get_info(self):
        """获取动物信息"""
        return f"{self.name}，{self.age}岁"

class Dog(Animal):
    """狗类，继承自动物类"""
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed
    
    def make_sound(self):
        """重写父类方法"""
        return "汪汪汪！"
    
    def get_info(self):
        """扩展父类方法"""
        base_info = super().get_info()
        return f"{base_info}，品种：{self.breed}"

class Cat(Animal):
    """猫类，继承自动物类"""
    def __init__(self, name, age, color):
        super().__init__(name, age)
        self.color = color
    
    def make_sound(self):
        """重写父类方法"""
        return "喵喵喵！"
    
    def get_info(self):
        """扩展父类方法"""
        base_info = super().get_info()
        return f"{base_info}，毛色：{self.color}"

# 测试代码
if __name__ == "__main__":
    dog = Dog("旺财", 3, "金毛")
    cat = Cat("咪咪", 2, "橘色")
    
    animals = [dog, cat]
    
    for animal in animals:
        print(f"{animal.get_info()}")
        print(f"声音: {animal.make_sound()}")
        print("-" * 20)