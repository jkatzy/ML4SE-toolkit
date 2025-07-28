/**
 * C#示例文件
 * 展示了C#的基本语法和面向对象特性
 */

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace CSharpExample
{
    // 主类
    class Program
    {
        // 主方法
        static async Task Main(string[] args)
        {
            Console.WriteLine("C#示例程序\n");
            
            // 基本数据类型
            int age = 30;
            double salary = 10000.50;
            bool isActive = true;
            char grade = 'A';
            
            // 字符串
            string name = "张三";
            
            Console.WriteLine("基本数据:");
            Console.WriteLine($"姓名: {name}");
            Console.WriteLine($"年龄: {age}");
            Console.WriteLine($"薪资: {salary}");
            Console.WriteLine($"是否活跃: {isActive}");
            Console.WriteLine($"等级: {grade}\n");
            
            // 数组
            int[] numbers = { 1, 2, 3, 4, 5 };
            Console.WriteLine("数组元素:");
            foreach (var num in numbers)
            {
                Console.Write($"{num} ");
            }
            Console.WriteLine("\n");
            
            // 集合
            List<string> fruits = new List<string> { "苹果", "香蕉", "橙子" };
            Console.WriteLine("水果列表:");
            foreach (var fruit in fruits)
            {
                Console.WriteLine($"- {fruit}");
            }
            Console.WriteLine();
            
            // 字典
            Dictionary<string, int> scores = new Dictionary<string, int>
            {
                { "数学", 90 },
                { "语文", 85 },
                { "英语", 95 }
            };
            
            Console.WriteLine("成绩单:");
            foreach (var entry in scores)
            {
                Console.WriteLine($"{entry.Key}: {entry.Value}");
            }
            Console.WriteLine();
            
            // 创建对象
            Person person = new Person("李四", 25);
            Console.WriteLine("人物信息:");
            Console.WriteLine(person);
            person.Greet();
            Console.WriteLine();
            
            // 继承
            Employee employee = new Employee("王五", 30, "开发工程师");
            Console.WriteLine("员工信息:");
            Console.WriteLine(employee);
            employee.Greet();
            employee.Work();
            Console.WriteLine();
            
            // LINQ
            var evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
            Console.WriteLine("LINQ - 偶数:");
            foreach (var num in evenNumbers)
            {
                Console.Write($"{num} ");
            }
            Console.WriteLine("\n");
            
            // 异步编程
            Console.WriteLine("异步编程示例:");
            await RunAsyncExample();
            
            // 异常处理
            try
            {
                int result = Divide(10, 0);
                Console.WriteLine($"结果: {result}");
            }
            catch (DivideByZeroException e)
            {
                Console.WriteLine($"捕获异常: {e.Message}");
            }
            finally
            {
                Console.WriteLine("异常处理完成");
            }
        }
        
        // 方法
        static int Divide(int a, int b)
        {
            return a / b;
        }
        
        // 异步方法
        static async Task RunAsyncExample()
        {
            Console.WriteLine("开始异步操作...");
            await Task.Delay(1000); // 模拟异步操作
            Console.WriteLine("异步操作完成\n");
        }
    }
    
    // 人物类
    class Person
    {
        // 属性
        public string Name { get; protected set; }
        public int Age { get; protected set; }
        
        // 构造函数
        public Person(string name, int age)
        {
            Name = name;
            Age = age;
        }
        
        // 方法
        public virtual void Greet()
        {
            Console.WriteLine($"你好，我是{Name}");
        }
        
        // 覆盖ToString方法
        public override string ToString()
        {
            return $"Person [Name={Name}, Age={Age}]";
        }
    }
    
    // 员工类 (继承自Person)
    class Employee : Person
    {
        // 额外的属性
        public string Position { get; private set; }
        
        // 构造函数
        public Employee(string name, int age, string position) : base(name, age)
        {
            Position = position;
        }
        
        // 额外的方法
        public void Work()
        {
            Console.WriteLine($"{Name}正在工作，职位是{Position}");
        }
        
        // 覆盖父类方法
        public override void Greet()
        {
            Console.WriteLine($"你好，我是{Name}，担任{Position}职位");
        }
        
        // 覆盖ToString方法
        public override string ToString()
        {
            return $"Employee [Name={Name}, Age={Age}, Position={Position}]";
        }
    }
}