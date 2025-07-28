#!/usr/bin/env ruby
# encoding: utf-8

# Ruby示例文件
# 展示了Ruby的基本语法和特性

# 打印标题
puts "Ruby示例程序\n\n"

# 基本数据类型
age = 30
salary = 10000.50
is_active = true
grade = 'A'

# 字符串
name = "张三"

puts "基本数据:"
puts "姓名: #{name}"
puts "年龄: #{age}"
puts "薪资: #{salary}"
puts "是否活跃: #{is_active}"
puts "等级: #{grade}\n\n"

# 数组
numbers = [1, 2, 3, 4, 5]
puts "数组元素:"
numbers.each { |num| print "#{num} " }
puts "\n"

# 添加元素到数组
numbers << 6
puts "添加后的数组: #{numbers}\n\n"

# 哈希表
scores = {
  "数学" => 90,
  "语文" => 85,
  "英语" => 95
}

puts "成绩单:"
scores.each do |subject, score|
  puts "#{subject}: #{score}"
end
puts

# 符号作为键
person = {
  name: "李四",
  age: 25,
  city: "北京"
}

puts "个人信息:"
person.each do |key, value|
  puts "#{key}: #{value}"
end
puts

# 函数定义
def greet(name)
  "你好，#{name}！"
end

def add(a, b)
  a + b
end

# 带默认参数的函数
def calculate_salary(base, bonus = 0, tax_rate = 0.1)
  (base + bonus) * (1 - tax_rate)
end

# 函数调用
puts greet(name)
puts "5 + 3 = #{add(5, 3)}"
puts "薪资计算: #{calculate_salary(10000, 2000)}\n\n"

# 类定义
class Person
  # 属性访问器
  attr_reader :name, :age
  attr_writer :age
  
  # 构造函数
  def initialize(name, age)
    @name = name
    @age = age
  end
  
  # 实例方法
  def greet
    puts "你好，我是#{@name}"
  end
  
  # 重写to_s方法
  def to_s
    "Person [name=#{@name}, age=#{@age}]"
  end
  
  # 类方法
  def self.species
    "人类"
  end
end

# 继承
class Employee < Person
  attr_reader :position
  
  def initialize(name, age, position)
    super(name, age)
    @position = position
  end
  
  # 覆盖父类方法
  def greet
    puts "你好，我是#{@name}，担任#{@position}职位"
  end
  
  def work
    puts "#{@name}正在工作，职位是#{@position}"
  end
  
  def to_s
    "Employee [name=#{@name}, age=#{@age}, position=#{@position}]"
  end
end

# 创建对象
puts "创建对象:"
person = Person.new("王五", 30)
puts person
person.greet
puts "类方法调用: #{Person.species}\n\n"

# 继承
puts "继承示例:"
employee = Employee.new("赵六", 28, "开发工程师")
puts employee
employee.greet
employee.work
puts

# 模块
module Utilities
  VERSION = "1.0"
  
  def self.format_currency(amount)
    "¥%.2f" % amount
  end
  
  # 可混入的方法
  module Formattable
    def format_name
      @name.upcase
    end
  end
end

# 使用模块
puts "模块使用:"
puts "工具版本: #{Utilities::VERSION}"
puts "格式化货币: #{Utilities.format_currency(1234.56)}\n\n"

# 混入模块
class FormattedPerson < Person
  include Utilities::Formattable
end

formatted_person = FormattedPerson.new("张三", 35)
puts "格式化名称: #{formatted_person.format_name}\n\n"

# 代码块
puts "代码块示例:"
5.times { |i| print "#{i} " }
puts

# 带参数的代码块
["苹果", "香蕉", "橙子"].each_with_index do |fruit, index|
  puts "#{index + 1}. #{fruit}"
end
puts

# Proc和Lambda
puts "Proc和Lambda:"
greeter = Proc.new { |name| puts "Proc: 你好，#{name}！" }
greeter.call("小明")

formatter = lambda { |text| puts "Lambda: #{text.upcase}" }
formatter.call("hello ruby")
puts

# 异常处理
puts "异常处理:"
begin
  result = 10 / 0
  puts "结果: #{result}"
rescue ZeroDivisionError => e
  puts "捕获异常: #{e.message}"
ensure
  puts "异常处理完成"
end
puts

# 文件操作（注释掉以避免实际创建文件）
=begin
File.open("temp.txt", "w") do |file|
  file.puts "这是第一行"
  file.puts "这是第二行"
end

puts "文件内容:"
File.readlines("temp.txt").each do |line|
  puts line.chomp
end
=end

# 符号
puts "符号示例:"
status = :active
puts "状态: #{status}"
puts "符号对象ID: #{:active.object_id}"
puts "相同符号的对象ID: #{:active.object_id}"
puts "字符串对象ID: #{"active".object_id}"
puts "另一个相同字符串的对象ID: #{"active".object_id}\n\n"

# 元编程
puts "元编程示例:"
class DynamicClass
  # 动态方法定义
  def self.create_method(name)
    define_method(name) do |arg|
      "#{name}方法被调用，参数: #{arg}"
    end
  end
  
  # 方法缺失处理
  def method_missing(name, *args)
    "未定义的方法: #{name}，参数: #{args.join(', ')}"
  end
end

dynamic = DynamicClass.new
DynamicClass.create_method(:dynamic_hello)
puts dynamic.dynamic_hello("世界")
puts dynamic.undefined_method("测试")