/**
 * Java示例文件
 * 展示了Java的基本语法和面向对象特性
 */

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

// 主类
public class Example {
    // 主方法
    public static void main(String[] args) {
        System.out.println("Java示例程序");
        
        // 基本数据类型
        int age = 30;
        double salary = 10000.50;
        boolean isActive = true;
        char grade = 'A';
        
        // 字符串
        String name = "张三";
        
        System.out.println("\n基本数据:");
        System.out.println("姓名: " + name);
        System.out.println("年龄: " + age);
        System.out.println("薪资: " + salary);
        System.out.println("是否活跃: " + isActive);
        System.out.println("等级: " + grade);
        
        // 数组
        int[] numbers = {1, 2, 3, 4, 5};
        System.out.println("\n数组元素:");
        for (int num : numbers) {
            System.out.print(num + " ");
        }
        System.out.println();
        
        // 集合
        List<String> fruits = new ArrayList<>();
        fruits.add("苹果");
        fruits.add("香蕉");
        fruits.add("橙子");
        
        System.out.println("\n水果列表:");
        for (String fruit : fruits) {
            System.out.println("- " + fruit);
        }
        
        // Map
        Map<String, Integer> scores = new HashMap<>();
        scores.put("数学", 90);
        scores.put("语文", 85);
        scores.put("英语", 95);
        
        System.out.println("\n成绩单:");
        for (Map.Entry<String, Integer> entry : scores.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
        
        // 创建对象
        Person person = new Person("李四", 25);
        System.out.println("\n人物信息:");
        System.out.println(person.toString());
        person.greet();
        
        // 继承
        Employee employee = new Employee("王五", 30, "开发工程师");
        System.out.println("\n员工信息:");
        System.out.println(employee.toString());
        employee.greet();
        employee.work();
        
        // Lambda表达式
        List<Integer> nums = List.of(1, 2, 3, 4, 5, 6);
        List<Integer> evenNums = nums.stream()
                                    .filter(n -> n % 2 == 0)
                                    .collect(Collectors.toList());
        
        System.out.println("\nLambda表达式 - 偶数:");
        System.out.println(evenNums);
        
        // 异常处理
        try {
            int result = divide(10, 0);
            System.out.println("结果: " + result);
        } catch (ArithmeticException e) {
            System.out.println("\n捕获异常: " + e.getMessage());
        } finally {
            System.out.println("异常处理完成");
        }
    }
    
    // 方法
    public static int divide(int a, int b) {
        return a / b;
    }
}

// 人物类
class Person {
    // 实例变量
    protected String name;
    protected int age;
    
    // 构造函数
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // 方法
    public void greet() {
        System.out.println("你好，我是" + name);
    }
    
    // 覆盖toString方法
    @Override
    public String toString() {
        return "Person [name=" + name + ", age=" + age + "]";
    }
}

// 员工类 (继承自Person)
class Employee extends Person {
    // 额外的实例变量
    private String position;
    
    // 构造函数
    public Employee(String name, int age, String position) {
        super(name, age);
        this.position = position;
    }
    
    // 额外的方法
    public void work() {
        System.out.println(name + "正在工作，职位是" + position);
    }
    
    // 覆盖父类方法
    @Override
    public void greet() {
        System.out.println("你好，我是" + name + "，担任" + position + "职位");
    }
    
    // 覆盖toString方法
    @Override
    public String toString() {
        return "Employee [name=" + name + ", age=" + age + ", position=" + position + "]";
    }
}