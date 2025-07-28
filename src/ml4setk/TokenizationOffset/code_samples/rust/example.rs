/**
 * Rust示例文件
 * 展示了Rust的基本语法和特性
 */

// 导入标准库
use std::collections::HashMap;
use std::fmt;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

// 结构体定义
struct Person {
    name: String,
    age: u32,
}

// 为Person实现方法
impl Person {
    // 构造函数
    fn new(name: &str, age: u32) -> Person {
        Person {
            name: String::from(name),
            age,
        }
    }
    
    // 实例方法
    fn greet(&self) {
        println!("你好，我是{}", self.name);
    }
    
    // 可变self的方法
    fn have_birthday(&mut self) {
        self.age += 1;
        println!("{}现在{}岁了", self.name, self.age);
    }
}

// 为Person实现Display trait
impl fmt::Display for Person {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Person [name={}, age={}]", self.name, self.age)
    }
}

// 定义一个trait
trait Worker {
    fn work(&self);
    fn get_salary(&self) -> f64;
}

// 员工结构体
struct Employee {
    person: Person,
    position: String,
    salary: f64,
}

// 为Employee实现方法
impl Employee {
    fn new(name: &str, age: u32, position: &str, salary: f64) -> Employee {
        Employee {
            person: Person::new(name, age),
            position: String::from(position),
            salary,
        }
    }
}

// 为Employee实现Worker trait
impl Worker for Employee {
    fn work(&self) {
        println!("{}正在工作，职位是{}", self.person.name, self.position);
    }
    
    fn get_salary(&self) -> f64 {
        self.salary
    }
}

// 为Employee实现Display trait
impl fmt::Display for Employee {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "Employee [name={}, age={}, position={}]",
            self.person.name, self.person.age, self.position
        )
    }
}

// 枚举定义
enum Status {
    Active,
    Inactive,
    Pending,
}

// 带数据的枚举
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

// 为枚举实现方法
impl Message {
    fn call(&self) {
        match self {
            Message::Quit => println!("退出消息"),
            Message::Move { x, y } => println!("移动到坐标: ({}, {})", x, y),
            Message::Write(text) => println!("文本消息: {}", text),
            Message::ChangeColor(r, g, b) => println!("颜色变更为: RGB({}, {}, {})", r, g, b),
        }
    }
}

// 泛型函数
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    
    for item in list {
        if item > largest {
            largest = item;
        }
    }
    
    largest
}

// 主函数
fn main() {
    println!("Rust示例程序\n");
    
    // 基本数据类型
    let age: u32 = 30;
    let salary: f64 = 10000.50;
    let is_active: bool = true;
    let grade: char = 'A';
    
    // 不可变变量
    let name = "张三";
    
    println!("基本数据:");
    println!("姓名: {}", name);
    println!("年龄: {}", age);
    println!("薪资: {:.2}", salary);
    println!("是否活跃: {}", is_active);
    println!("等级: {}\n", grade);
    
    // 可变变量
    let mut counter = 0;
    counter += 1;
    println!("计数器: {}\n", counter);
    
    // 数组
    let numbers = [1, 2, 3, 4, 5];
    println!("数组元素:");
    for num in &numbers {
        print!("{} ", num);
    }
    println!("\n");
    
    // 向量
    let mut fruits = vec!["苹果", "香蕉", "橙子"];
    println!("水果列表:");
    for fruit in &fruits {
        println!("- {}", fruit);
    }
    
    // 添加元素到向量
    fruits.push("葡萄");
    println!("\n添加后的水果: {:?}\n", fruits);
    
    // 哈希映射
    let mut scores = HashMap::new();
    scores.insert(String::from("数学"), 90);
    scores.insert(String::from("语文"), 85);
    scores.insert(String::from("英语"), 95);
    
    println!("成绩单:");
    for (subject, score) in &scores {
        println!("{}: {}", subject, score);
    }
    println!();
    
    // 元组
    let person_info = ("李四", 25, "北京");
    println!("元组示例:");
    println!("姓名: {}", person_info.0);
    println!("年龄: {}", person_info.1);
    println!("城市: {}\n", person_info.2);
    
    // 创建结构体
    let mut person = Person::new("王五", 30);
    println!("人物信息:");
    println!("{}", person);
    person.greet();
    person.have_birthday();
    println!();
    
    // 创建员工
    let employee = Employee::new("赵六", 28, "开发工程师", 15000.0);
    println!("员工信息:");
    println!("{}", employee);
    
    // 使用trait
    let worker: &dyn Worker = &employee;
    worker.work();
    println!("薪资: {:.2}", worker.get_salary());
    println!();
    
    // 枚举
    let status = Status::Active;
    println!("状态示例:");
    match status {
        Status::Active => println!("状态: 活跃"),
        Status::Inactive => println!("状态: 不活跃"),
        Status::Pending => println!("状态: 待定"),
    }
    
    // 带数据的枚举
    let messages = [
        Message::Quit,
        Message::Move { x: 10, y: 20 },
        Message::Write(String::from("你好，Rust!")),
        Message::ChangeColor(255, 0, 0),
    ];
    
    println!("\n消息示例:");
    for message in &messages {
        message.call();
    }
    println!();
    
    // Option枚举
    let some_number = Some(5);
    let some_string = Some("一个字符串");
    let absent_number: Option<i32> = None;
    
    println!("Option示例:");
    match some_number {
        Some(n) => println!("数字: {}", n),
        None => println!("没有数字"),
    }
    
    // if let简化匹配
    if let Some(s) = some_string {
        println!("字符串: {}", s);
    }
    
    if let Some(n) = absent_number {
        println!("数字: {}", n);
    } else {
        println!("没有数字");
    }
    println!();
    
    // 泛型
    let number_list = vec![34, 50, 25, 100, 65];
    println!("泛型函数示例:");
    println!("最大数字: {}", largest(&number_list));
    
    let char_list = vec!['y', 'm', 'a', 'q'];
    println!("最大字符: {}\n", largest(&char_list));
    
    // 闭包
    let add = |a, b| a + b;
    println!("闭包示例:");
    println!("5 + 3 = {}\n", add(5, 3));
    
    // 错误处理
    println!("错误处理示例:");
    let result = divide(10.0, 2.0);
    match result {
        Ok(value) => println!("10 / 2 = {}", value),
        Err(e) => println!("错误: {}", e),
    }
    
    let error_result = divide(10.0, 0.0);
    match error_result {
        Ok(value) => println!("10 / 0 = {}", value),
        Err(e) => println!("错误: {}", e),
    }
    println!();
    
    // 线程
    println!("线程示例:");
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];
    
    for i in 0..3 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
            println!("线程 {}: 计数器 = {}", i, *num);
            thread::sleep(Duration::from_millis(10));
        });
        handles.push(handle);
    }
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    println!("最终计数器值: {}", *counter.lock().unwrap());
}

// 返回Result的函数
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err(String::from("除数不能为零"))
    } else {
        Ok(a / b)
    }
}
