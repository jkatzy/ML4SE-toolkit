package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
    "sync"
    "time"
)

func fetchURL(url string, wg *sync.WaitGroup, ch chan<- string) {
    defer wg.Done()

    start := time.Now()
    resp, err := http.Get(url)
    if err != nil {
        ch <- fmt.Sprintf("获取 %s 失败: %v", url, err)
        return
    }
    defer resp.Body.Close()

    bodyBytes, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        ch <- fmt.Sprintf("读取 %s 响应失败: %v", url, err)
        return
    }

    elapsed := time.Since(start).Seconds()
    ch <- fmt.Sprintf("从 %s 获取了 %d 字节, 用时 %.2f 秒", url, len(bodyBytes), elapsed)
}

func main() {
    urls := []string{
        "https://jsonplaceholder.typicode.com/todos/1",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/users/1",
    }

    var wg sync.WaitGroup
    ch := make(chan string, len(urls))

    fmt.Println("开始并发获取 URL...")

    for _, url := range urls {
        wg.Add(1)
        go fetchURL(url, &wg, ch)
    }

    // 等待所有 goroutine 完成
    wg.Wait()
    close(ch)

    // 从 channel 中读取所有结果
    for result := range ch {
        fmt.Println(result)
    }

    fmt.Println("所有任务完成。")
}