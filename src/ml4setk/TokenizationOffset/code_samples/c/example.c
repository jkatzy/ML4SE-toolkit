/**
 * C语言示例文件
 * 展示了C语言的基本语法和特性
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 常量定义
#define MAX_NAME_LENGTH 50
#define PI 3.14159

// 结构体定义
struct Person {
    char name[MAX_NAME_LENGTH];
    int age;
    float height;
};

// 函数声明
void greet(const char* name);
int add(int a, int b);
float calculate_circle_area(float radius);
void modify_array(int arr[], int size);
void print_person(struct Person p);
struct Person create_person(const char* name, int age, float height);

// 全局变量
int global_counter = 0;

// 主函数
int main() {
    printf("C语言示例程序\n\n");
    
    // 基本数据类型
    int age = 30;
    float salary = 10000.50f;
    char grade = 'A';
    
    // 字符串
    char name[MAX_NAME_LENGTH] = "张三";
    
    printf("基本数据:\n");
    printf("姓名: %s\n", name);
    printf("年龄: %d\n", age);
    printf("薪资: %.2f\n", salary);
    printf("等级: %c\n\n", grade);
    
    // 调用函数
    greet(name);
    printf("5 + 3 = %d\n", add(5, 3));
    printf("半径为5的圆面积: %.2f\n\n", calculate_circle_area(5.0f));
    
    // 数组
    int numbers[5] = {1, 2, 3, 4, 5};
    printf("数组元素:\n");
    for (int i = 0; i < 5; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n\n");
    
    // 修改数组
    modify_array(numbers, 5);
    printf("修改后的数组:\n");
    for (int i = 0; i < 5; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n\n");
    
    // 指针
    int value = 10;
    int* ptr = &value;
    printf("指针示例:\n");
    printf("value的值: %d\n", value);
    printf("value的地址: %p\n", &value);
    printf("ptr存储的地址: %p\n", ptr);
    printf("ptr指向的值: %d\n\n", *ptr);
    
    // 修改指针指向的值
    *ptr = 20;
    printf("修改后value的值: %d\n\n", value);
    
    // 结构体
    struct Person person1 = create_person("李四", 25, 175.5f);
    printf("结构体示例:\n");
    print_person(person1);
    
    // 动态内存分配
    int* dynamic_array = (int*)malloc(5 * sizeof(int));
    if (dynamic_array != NULL) {
        printf("\n动态内存分配:\n");
        for (int i = 0; i < 5; i++) {
            dynamic_array[i] = i * 10;
            printf("%d ", dynamic_array[i]);
        }
        printf("\n");
        
        // 释放内存
        free(dynamic_array);
    }
    
    return 0;
}

// 函数定义
void greet(const char* name) {
    printf("你好，%s！\n", name);
    global_counter++; // 修改全局变量
}

int add(int a, int b) {
    return a + b;
}

float calculate_circle_area(float radius) {
    return PI * radius * radius;
}

void modify_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] *= 2;
    }
}

void print_person(struct Person p) {
    printf("姓名: %s\n", p.name);
    printf("年龄: %d\n", p.age);
    printf("身高: %.1f cm\n", p.height);
}

struct Person create_person(const char* name, int age, float height) {
    struct Person p;
    strncpy(p.name, name, MAX_NAME_LENGTH - 1);
    p.name[MAX_NAME_LENGTH - 1] = '\0'; // 确保字符串结束
    p.age = age;
    p.height = height;
    return p;
}