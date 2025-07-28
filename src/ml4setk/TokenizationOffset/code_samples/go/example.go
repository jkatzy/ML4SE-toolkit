/**
 * Go语言示例文件
 * 展示了Go的基本语法和特性
 */

package main

import (
	"fmt"
	"math"
	"strings"
	"sync"
	"time"
)

// 结构体定义
type Person struct {
	Name string
	Age  int
}

// 为Person结构体定义方法
func (p Person) Greet() {
	fmt.Printf("你好，我是%s\n", p.Name)
}

// 指针接收者方法
func (p *Person) Birthday() {
	p.Age++
	fmt.Printf("%s现在%d岁了\n", p.Name, p.Age)
}

// 接口定义
type Worker interface {
	Work()
	GetSalary() float64
}

// Employee结构体
type Employee struct {
	Person    // 嵌入Person结构体
	Position  string
	Salary    float64
	IsWorking bool
}

// 实现Worker接口的方法
func (e *Employee) Work() {
	e.IsWorking = true
	fmt.Printf("%s正在工作，职位是%s\n", e.Name, e.Position)
}

func (e Employee) GetSalary() float64 {
	return e.Salary
}

// 自定义String方法
func (e Employee) String() string {
	return fmt.Sprintf("员工[姓名=%s, 年龄=%d, 职位=%s]", e.Name, e.Age, e.Position)
}

// 函数定义
func add(a, b int) int {
	return a + b
}

// 多返回值函数
func divide(a, b float64) (float64, error) {
	if b == 0 {
		return 0, fmt.Errorf("除数不能为零")
	}
	return a / b, nil
}

// 可变参数函数
func sum(nums ...int) int {
	total := 0
	for _, num := range nums {
		total += num
	}
	return total
}

// 闭包函数
func makeCounter() func() int {
	count := 0
	return func() int {
		count++
		return count
	}
}

// 并发函数
func printNumbers(wg *sync.WaitGroup, prefix string) {
	defer wg.Done()
	for i := 1; i <= 5; i++ {
		fmt.Printf("%s: %d\n", prefix, i)
		time.Sleep(100 * time.Millisecond)
	}
}

// 主函数
func main() {
	fmt.Println("Go语言示例程序\n")

	// 基本数据类型
	var age int = 30
	var salary float64 = 10000.50
	var isActive bool = true
	var grade rune = '优'

	// 短变量声明
	name := "张三"

	fmt.Println("基本数据:")
	fmt.Printf("姓名: %s\n", name)
	fmt.Printf("年龄: %d\n", age)
	fmt.Printf("薪资: %.2f\n", salary)
	fmt.Printf("是否活跃: %t\n", isActive)
	fmt.Printf("等级: %c\n\n", grade)

	// 数组
	numbers := [5]int{1, 2, 3, 4, 5}
	fmt.Println("数组元素:")
	for _, num := range numbers {
		fmt.Printf("%d ", num)
	}
	fmt.Println("\n")

	// 切片
	fruits := []string{"苹果", "香蕉", "橙子"}
	fmt.Println("水果列表:")
	for _, fruit := range fruits {
		fmt.Printf("- %s\n", fruit)
	}
	fmt.Println()

	// 添加元素到切片
	fruits = append(fruits, "葡萄")
	fmt.Printf("添加后的水果: %v\n\n", fruits)

	// 映射
	scores := map[string]int{
		"数学": 90,
		"语文": 85,
		"英语": 95,
	}

	fmt.Println("成绩单:")
	for subject, score := range scores {
		fmt.Printf("%s: %d\n", subject, score)
	}
	fmt.Println()

	// 函数调用
	fmt.Printf("5 + 3 = %d\n", add(5, 3))

	// 多返回值处理
	result, err := divide(10, 2)
	if err != nil {
		fmt.Printf("错误: %s\n", err)
	} else {
		fmt.Printf("10 / 2 = %.1f\n", result)
	}

	// 错误处理示例
	_, err = divide(10, 0)
	if err != nil {
		fmt.Printf("错误处理: %s\n", err)
	}
	fmt.Println()

	// 可变参数
	fmt.Printf("1+2+3+4+5 = %d\n\n", sum(1, 2, 3, 4, 5))

	// 创建结构体
	person := Person{
		Name: "李四",
		Age:  25,
	}
	fmt.Println("人物信息:")
	fmt.Printf("%+v\n", person)
	person.Greet()
	person.Birthday()
	fmt.Println()

	// 创建员工
	employee := Employee{
		Person:    Person{Name: "王五", Age: 30},
		Position:  "开发工程师",
		Salary:    15000,
		IsWorking: false,
	}
	fmt.Println("员工信息:")
	fmt.Println(employee) // 使用String()方法
	employee.Greet()      // 继承自Person
	employee.Work()
	fmt.Printf("薪资: %.2f\n\n", employee.GetSalary())

	// 接口使用
	var worker Worker = &employee
	fmt.Println("通过接口调用:")
	worker.Work()
	fmt.Printf("通过接口获取薪资: %.2f\n\n", worker.GetSalary())

	// 闭包
	counter := makeCounter()
	fmt.Println("闭包计数器:")
	fmt.Printf("第一次调用: %d\n", counter())
	fmt.Printf("第二次调用: %d\n", counter())
	fmt.Printf("第三次调用: %d\n\n", counter())

	// 字符串操作
	fmt.Println("字符串操作:")
	message := "  Hello, Go!  "
	fmt.Printf("原始字符串: '%s'\n", message)
	fmt.Printf("去除空格: '%s'\n", strings.TrimSpace(message))
	fmt.Printf("转小写: '%s'\n", strings.ToLower(message))
	fmt.Printf("包含'Go': %t\n\n", strings.Contains(message, "Go"))

	// 数学函数
	fmt.Println("数学函数:")
	fmt.Printf("Pi值: %.5f\n", math.Pi)
	fmt.Printf("2的平方根: %.2f\n", math.Sqrt(2))
	fmt.Printf("2的3次方: %.0f\n\n", math.Pow(2, 3))

	// 并发
	fmt.Println("并发示例:")
	var wg sync.WaitGroup
	wg.Add(2)
	go printNumbers(&wg, "协程A")
	go printNumbers(&wg, "协程B")
	wg.Wait()

	// 通道
	fmt.Println("\n通道示例:")
	ch := make(chan string)
	go func() {
		ch <- "通道消息1"
		ch <- "通道消息2"
		close(ch)
	}()

	for msg := range ch {
		fmt.Println(msg)
	}
}