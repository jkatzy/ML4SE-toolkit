// 这是一个异步函数
async function fetchUserData(userId) {
    const apiUrl = `https://jsonplaceholder.typicode.com/users/${userId}`;
  
    console.log(`正在从 ${apiUrl} 获取用户数据...`);
  
    try {
      // 等待 fetch 请求完成
      const response = await fetch(apiUrl);
  
      // 如果响应状态码不是 2xx，则抛出错误
      if (!response.ok) {
        throw new Error(`HTTP 错误! 状态: ${response.status}`);
      }
  
      // 等待 JSON 数据解析完成
      const userData = await response.json();
  
      console.log("--- 用户数据获取成功 ---");
      console.log(`ID: ${userData.id}`);
      console.log(`姓名: ${userData.name}`);
      console.log(`邮箱: ${userData.email}`);
      console.log(`地址: ${userData.address.street}, ${userData.address.city}`);
      console.log("-----------------------");
  
    } catch (error) {
      console.error("获取用户数据时发生错误:", error);
    }
  }
  
  // 调用异步函数
  fetchUserData(1);
  fetchUserData(5);