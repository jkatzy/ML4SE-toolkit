/**
 * C++示例文件
 * 展示了C++的基本语法和面向对象特性
 */

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <memory>
#include <algorithm>

// 常量定义
constexpr double PI = 3.14159;

// 类定义
class Person {
protected:
    std::string name;
    int age;
    
public:
    // 构造函数
    Person(const std::string& name, int age) : name(name), age(age) {}
    
    // 虚析构函数
    virtual ~Person() {
        std::cout << "Person析构函数被调用" << std::endl;
    }
    
    // 虚函数
    virtual void greet() const {
        std::cout << "你好，我是" << name << std::endl;
    }
    
    // Getter方法
    std::string getName() const { return name; }
    int getAge() const { return age; }
    
    // 友元函数
    friend std::ostream& operator<<(std::ostream& os, const Person& person);
};

// 运算符重载
std::ostream& operator<<(std::ostream& os, const Person& person) {
    os << "Person [name=" << person.name << ", age=" << person.age << "]";
    return os;
}

// 继承
class Employee : public Person {
private:
    std::string position;
    double salary;
    
public:
    // 构造函数
    Employee(const std::string& name, int age, const std::string& position, double salary)
        : Person(name, age), position(position), salary(salary) {}
    
    // 析构函数
    ~Employee() override {
        std::cout << "Employee析构函数被调用" << std::endl;
    }
    
    // 覆盖虚函数
    void greet() const override {
        std::cout << "你好，我是" << name << "，担任" << position << "职位" << std::endl;
    }
    
    // 新方法
    void work() const {
        std::cout << name << "正在工作，职位是" << position << std::endl;
    }
    
    double getSalary() const { return salary; }
};

// 模板函数
template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

// 模板类
template<typename T>
class Container {
private:
    std::vector<T> elements;
    
public:
    void add(const T& element) {
        elements.push_back(element);
    }
    
    void print() const {
        for (const auto& element : elements) {
            std::cout << element << " ";
        }
        std::cout << std::endl;
    }
    
    size_t size() const {
        return elements.size();
    }
};

// 主函数
int main() {
    std::cout << "C++示例程序" << std::endl << std::endl;
    
    // 基本数据类型
    int age = 30;
    double salary = 10000.50;
    bool isActive = true;
    char grade = 'A';
    
    // 字符串
    std::string name = "张三";
    
    std::cout << "基本数据:" << std::endl;
    std::cout << "姓名: " << name << std::endl;
    std::cout << "年龄: " << age << std::endl;
    std::cout << "薪资: " << salary << std::endl;
    std::cout << "是否活跃: " << std::boolalpha << isActive << std::endl;
    std::cout << "等级: " << grade << std::endl << std::endl;
    
    // 向量
    std::vector<int> numbers = {1, 2, 3, 4, 5};
    std::cout << "向量元素:" << std::endl;
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl << std::endl;
    
    // 映射
    std::map<std::string, int> scores;
    scores["数学"] = 90;
    scores["语文"] = 85;
    scores["英语"] = 95;
    
    std::cout << "成绩单:" << std::endl;
    for (const auto& [subject, score] : scores) {
        std::cout << subject << ": " << score << std::endl;
    }
    std::cout << std::endl;
    
    // 创建对象
    Person person("李四", 25);
    std::cout << "人物信息:" << std::endl;
    std::cout << person << std::endl;
    person.greet();
    std::cout << std::endl;
    
    // 继承
    Employee employee("王五", 30, "开发工程师", 15000.0);
    std::cout << "员工信息:" << std::endl;
    std::cout << "姓名: " << employee.getName() << std::endl;
    std::cout << "年龄: " << employee.getAge() << std::endl;
    std::cout << "薪资: " << employee.getSalary() << std::endl;
    employee.greet();
    employee.work();
    std::cout << std::endl;
    
    // 智能指针
    std::cout << "智能指针:" << std::endl;
    std::shared_ptr<Person> personPtr = std::make_shared<Employee>("赵六", 28, "产品经理", 18000.0);
    personPtr->greet();  // 多态调用
    std::cout << std::endl;
    
    // 模板函数
    std::cout << "模板函数:" << std::endl;
    std::cout << "max(5, 9) = " << max(5, 9) << std::endl;
    std::cout << "max(3.14, 2.71) = " << max(3.14, 2.71) << std::endl;
    std::cout << "max(\"apple\", \"banana\") = " << max(std::string("apple"), std::string("banana")) << std::endl;
    std::cout << std::endl;
    
    // 模板类
    std::cout << "模板类:" << std::endl;
    Container<int> intContainer;
    intContainer.add(10);
    intContainer.add(20);
    intContainer.add(30);
    std::cout << "整数容器: ";
    intContainer.print();
    
    Container<std::string> stringContainer;
    stringContainer.add("苹果");
    stringContainer.add("香蕉");
    stringContainer.add("橙子");
    std::cout << "字符串容器: ";
    stringContainer.print();
    std::cout << std::endl;
    
    // Lambda表达式
    std::cout << "Lambda表达式:" << std::endl;
    auto evenNumbers = std::vector<int>();
    std::copy_if(numbers.begin(), numbers.end(), std::back_inserter(evenNumbers),
                [](int n) { return n % 2 == 0; });
    
    std::cout << "偶数: ";
    for (const auto& num : evenNumbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    return 0;
}