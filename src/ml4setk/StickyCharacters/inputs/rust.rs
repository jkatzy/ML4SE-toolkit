// 你需要在 Cargo.toml 文件中添加依赖:
// [dependencies]
// clap = { version = "4.0", features = ["derive"] }

use clap::{Parser, Subcommand};

/// 一个简单的命令行计算器
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// 将两个数字相加
    Add {
        #[arg(value_name = "NUM1")]
        num1: f64,
        #[arg(value_name = "NUM2")]
        num2: f64,
    },
    /// 用第一个数字减去第二个数字
    Subtract {
        #[arg(value_name = "NUM1")]
        num1: f64,
        #[arg(value_name = "NUM2")]
        num2: f64,
    },
}

fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Add { num1, num2 } => {
            let result = num1 + num2;
            println!("{} + {} = {}", num1, num2, result);
        }
        Commands::Subtract { num1, num2 } => {
            let result = num1 - num2;
            println!("{} - {} = {}", num1, num2, result);
        }
    }
}

/*
--- 如何运行 ---
1. 保存代码为 main.rs
2. 在 Cargo.toml 中添加 clap 依赖
3. 编译: cargo build
4. 运行:
   target/debug/your_project_name add 5 3
   输出: 5 + 3 = 8

   target/debug/your_project_name subtract 10 4.5
   输出: 10 - 4.5 = 5.5

   target/debug/your_project_name --help
   显示帮助信息
*/