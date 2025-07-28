/**
 * JavaScript示例文件
 * 展示了JavaScript的基本语法和功能
 */

// 变量声明
const name = "张三";
let age = 30;
var isActive = true;

// 函数定义
function greet(person) {
  return `你好，${person}！`;
}

// 箭头函数
const calculateArea = (width, height) => {
  return width * height;
};

// 类定义
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  
  sayHello() {
    console.log(`我是${this.name}，今年${this.age}岁。`);
  }
  
  static createAnonymous() {
    return new Person("匿名", 0);
  }
}

// 继承
class Employee extends Person {
  constructor(name, age, position) {
    super(name, age);
    this.position = position;
  }
  
  introduce() {
    console.log(`我是${this.name}，担任${this.position}职位。`);
  }
}

// 异步函数
async function fetchData(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("获取数据失败:", error);
    return null;
  }
}

// 数组操作
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(num => num * 2);
const sum = numbers.reduce((acc, curr) => acc + curr, 0);
const evenNumbers = numbers.filter(num => num % 2 === 0);

// 对象解构
const person = {
  name: "李四",
  age: 25,
  city: "上海",
  hobbies: ["阅读", "游泳", "编程"]
};

const { name: personName, age: personAge, ...rest } = person;

// 测试代码
console.log("基本变量:");
console.log(`姓名: ${name}, 年龄: ${age}, 是否活跃: ${isActive}`);

console.log("\n函数调用:");
console.log(greet("王五"));
console.log(`矩形面积: ${calculateArea(5, 3)}`);

console.log("\n类实例化:");
const john = new Person("约翰", 28);
john.sayHello();

const manager = new Employee("玛丽", 35, "项目经理");
manager.introduce();

console.log("\n数组操作:");
console.log(`原始数组: ${numbers}`);
console.log(`加倍后: ${doubled}`);
console.log(`总和: ${sum}`);
console.log(`偶数: ${evenNumbers}`);

console.log("\n对象解构:");
console.log(`解构后的姓名: ${personName}`);
console.log(`解构后的年龄: ${personAge}`);
console.log("剩余属性:", rest);