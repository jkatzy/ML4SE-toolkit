/**
 * Scala示例文件
 * 展示了Scala的基本语法和特性
 */

// 对象定义（相当于静态类）
object Example {
  // 主方法
  def main(args: Array[String]): Unit = {
    println("Scala示例程序\n")
    
    // 基本数据类型
    val age: Int = 30
    val salary: Double = 10000.50
    val isActive: Boolean = true
    val grade: Char = 'A'
    
    // 字符串
    val name = "张三"
    
    println("基本数据:")
    println(s"姓名: $name")
    println(s"年龄: $age")
    println(f"薪资: $salary%.2f")
    println(s"是否活跃: $isActive")
    println(s"等级: $grade\n")
    
    // 变量
    var counter = 0
    counter += 1
    println(s"计数器: $counter\n")
    
    // 数组
    val numbers = Array(1, 2, 3, 4, 5)
    println("数组元素:")
    numbers.foreach(num => print(s"$num "))
    println("\n")
    
    // 列表
    val fruits = List("苹果", "香蕉", "橙子")
    println("水果列表:")
    fruits.foreach(fruit => println(s"- $fruit"))
    
    // 添加元素到列表（创建新列表）
    val moreFruits = fruits :+ "葡萄"
    println(s"\n添加后的水果: $moreFruits\n")
    
    // 映射
    val scores = Map(
      "数学" -> 90,
      "语文" -> 85,
      "英语" -> 95
    )
    
    println("成绩单:")
    scores.foreach { case (subject, score) =>
      println(s"$subject: $score")
    }
    println()
    
    // 元组
    val personInfo = ("李四", 25, "北京")
    println("元组示例:")
    println(s"姓名: ${personInfo._1}")
    println(s"年龄: ${personInfo._2}")
    println(s"城市: ${personInfo._3}\n")
    
    // 函数定义
    def greet(person: String): String = s"你好，$person！"
    
    def add(a: Int, b: Int): Int = a + b
    
    // 带默认参数的函数
    def calculateSalary(base: Double, bonus: Double = 0, taxRate: Double = 0.1): Double =
      (base + bonus) * (1 - taxRate)
    
    // 函数调用
    println(greet(name))
    println(s"5 + 3 = ${add(5, 3)}")
    println(s"薪资计算: ${calculateSalary(10000, 2000)}\n")
    
    // 类定义
    val person = new Person("王五", 30)
    println("创建对象:")
    println(person)
    person.greet()
    println(s"类方法调用: ${Person.species}\n")
    
    // 继承
    val employee = new Employee("赵六", 28, "开发工程师")
    println("继承示例:")
    println(employee)
    employee.greet()
    employee.work()
    println()
    
    // 特质（接口）
    val manager = new Manager("钱七", 35, 20000)
    println("特质示例:")
    manager.greet()
    manager.work()
    println(s"薪资: ${manager.getSalary}\n")
    
    // 模式匹配
    val status = Status.Active
    println("模式匹配示例:")
    status match {
      case Status.Active => println("状态: 活跃")
      case Status.Inactive => println("状态: 不活跃")
      case Status.Pending => println("状态: 待定")
    }
    
    // 带数据的枚举
    val messages = List(
      Message.Quit,
      Message.Move(10, 20),
      Message.Write("你好，Scala!"),
      Message.ChangeColor(255, 0, 0)
    )
    
    println("\n消息示例:")
    messages.foreach {
      case Message.Quit => println("退出消息")
      case Message.Move(x, y) => println(s"移动到坐标: ($x, $y)")
      case Message.Write(text) => println(s"文本消息: $text")
      case Message.ChangeColor(r, g, b) => println(s"颜色变更为: RGB($r, $g, $b)")
    }
    println()
    
    // Option类型
    val optionalName: Option[String] = Some("可选字符串")
    val optionalNumber: Option[Int] = None
    
    println("Option类型示例:")
    optionalName match {
      case Some(name) => println(s"可选名称: $name")
      case None => println("可选名称为None")
    }
    
    optionalNumber match {
      case Some(number) => println(s"可选数字: $number")
      case None => println("可选数字为None")
    }
    println()
    
    // 高阶函数
    println("高阶函数示例:")
    val doubled = numbers.map(_ * 2)
    println(s"数字加倍: ${doubled.mkString(", ")}")
    
    val evenNumbers = numbers.filter(_ % 2 == 0)
    println(s"偶数: ${evenNumbers.mkString(", ")}")
    
    val sum = numbers.reduce(_ + _)
    println(s"总和: $sum\n")
    
    // 闭包
    val addClosure = (a: Int, b: Int) => a + b
    println("闭包示例:")
    println(s"5 + 3 = ${addClosure(5, 3)}\n")
    
    // 柯里化
    def multiply(x: Int)(y: Int): Int = x * y
    println("柯里化示例:")
    println(s"5 * 3 = ${multiply(5)(3)}")
    
    val timesTwo = multiply(2) _  // 部分应用函数
    println(s"4 * 2 = ${timesTwo(4)}\n")
    
    // 集合操作
    println("集合操作:")
    val names = List("张三", "李四", "王五", "赵六")
    val sortedNames = names.sortBy(_.length)
    println(s"按长度排序的名字: $sortedNames")
    
    val nameGroups = names.groupBy(_.length)
    println("按长度分组的名字:")
    nameGroups.foreach { case (length, nameList) =>
      println(s"长度 $length: ${nameList.mkString(", ")}")
    }
    println()
    
    // 错误处理
    println("错误处理示例:")
    try {
      val result = divide(10, 2)
      println(s"10 / 2 = $result")
      
      val errorResult = divide(10, 0)
      println(s"10 / 0 = $errorResult")
    } catch {
      case e: ArithmeticException => println(s"捕获异常: ${e.getMessage}")
      case e: Exception => println(s"未知异常: ${e.getMessage}")
    } finally {
      println("异常处理完成")
    }
    println()
    
    // 隐式转换
    implicit def intToString(x: Int): String = s"数字$x"
    
    println("隐式转换示例:")
    val num: Int = 42
    val str: String = num  // 隐式转换
    println(str)
    println()
    
    // 并发
    println("并发示例:")
    import scala.concurrent.{Future, Await}
    import scala.concurrent.ExecutionContext.Implicits.global
    import scala.concurrent.duration._
    
    val future = Future {
      Thread.sleep(100)
      "异步操作完成"
    }
    
    println("等待异步操作...")
    val result = Await.result(future, 1.second)
    println(result)
    
    println("\nScala示例程序结束")
  }
  
  // 辅助方法
  def divide(a: Int, b: Int): Int = a / b
}

// 类定义
class Person(val name: String, val age: Int) {
  // 重写toString方法
  override def toString: String = s"Person [name=$name, age=$age]"
  
  // 实例方法
  def greet(): Unit = println(s"你好，我是$name")
}

// 伴生对象
object Person {
  // 相当于静态成员
  val species: String = "人类"
}

// 继承
class Employee(name: String, age: Int, val position: String) extends Person(name, age) {
  // 重写toString方法
  override def toString: String = s"Employee [name=$name, age=$age, position=$position]"
  
  // 重写方法
  override def greet(): Unit = println(s"你好，我是$name，担任$position职位")
  
  // 新方法
  def work(): Unit = println(s"$name正在工作，职位是$position")
}

// 特质（接口）
trait Worker {
  def work(): Unit
  def getSalary: Double
}

// 实现特质
class Manager(name: String, age: Int, private val salary: Double) 
  extends Employee(name, age, "经理") with Worker {
  
  def getSalary: Double = salary
}

// 枚举
object Status extends Enumeration {
  val Active, Inactive, Pending = Value
}

// 密封特质（类似枚举）
sealed trait Message
object Message {
  case object Quit extends Message
  case class Move(x: Int, y: Int) extends Message
  case class Write(text: String) extends Message
  case class ChangeColor(r: Int, g: Int, b: Int) extends Message
}