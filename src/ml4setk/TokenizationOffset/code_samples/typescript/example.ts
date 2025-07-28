/**
 * TypeScript示例文件
 * 展示了TypeScript的类型系统和语法特性
 */

// 基本类型注解
let name: string = "张三";
let age: number = 30;
let isActive: boolean = true;
let hobbies: string[] = ["阅读", "游泳", "编程"];
let tuple: [string, number] = ["坐标", 100];

// 接口定义
interface Person {
  name: string;
  age: number;
  address?: string; // 可选属性
  readonly id: number; // 只读属性
  greet(): void;
}

// 类型别名
type Point = {
  x: number;
  y: number;
};

// 枚举
enum Direction {
  Up = "UP",
  Down = "DOWN",
  Left = "LEFT",
  Right = "RIGHT"
}

// 泛型函数
function identity<T>(arg: T): T {
  return arg;
}

// 类实现接口
class Employee implements Person {
  readonly id: number;
  
  constructor(public name: string, public age: number, private position: string) {
    this.id = Math.floor(Math.random() * 1000);
  }
  
  greet(): void {
    console.log(`你好，我是${this.name}，担任${this.position}职位。`);
  }
  
  // 访问修饰符
  private calculateSalary(): number {
    return 10000; // 简化的薪资计算
  }
  
  public getSalaryInfo(): string {
    return `${this.name}的薪资是${this.calculateSalary()}元。`;
  }
}

// 继承
class Manager extends Employee {
  constructor(name: string, age: number, private department: string) {
    super(name, age, "经理");
  }
  
  override greet(): void {
    console.log(`你好，我是${this.name}，${this.department}部门的经理。`);
  }
}

// 联合类型
type ID = string | number;
let userId: ID = 123;
userId = "ABC123"; // 合法

// 交叉类型
type Coordinates = Point & { z: number };
const position: Coordinates = { x: 10, y: 20, z: 30 };

// 类型断言
let someValue: any = "这是一个字符串";
let strLength: number = (someValue as string).length;

// 函数类型
type MathFunc = (x: number, y: number) => number;
const add: MathFunc = (x, y) => x + y;
const subtract: MathFunc = (x, y) => x - y;

// 测试代码
console.log("基本类型:");
console.log(`姓名: ${name}, 年龄: ${age}, 是否活跃: ${isActive}`);
console.log(`爱好: ${hobbies.join(", ")}`);
console.log(`元组: ${tuple[0]} - ${tuple[1]}`);

console.log("\n枚举值:");
console.log(`向上: ${Direction.Up}`);

console.log("\n泛型函数:");
console.log(`字符串标识: ${identity("测试")}`);
console.log(`数字标识: ${identity(42)}`);

console.log("\n类实例:");
const emp = new Employee("李四", 28, "开发工程师");
emp.greet();
console.log(emp.getSalaryInfo());

const mgr = new Manager("王五", 35, "技术");
mgr.greet();

console.log("\n类型操作:");
console.log(`坐标: (${position.x}, ${position.y}, ${position.z})`);
console.log(`字符串长度: ${strLength}`);
console.log(`5 + 3 = ${add(5, 3)}`);