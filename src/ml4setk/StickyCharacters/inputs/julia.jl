# 你可能需要先安装 Plots 和 GR 包:
# using Pkg
# Pkg.add("Plots")
# Pkg.add("GR")

using Plots

# 定义要绘制的函数
f(x) = sin(x) + cos(3x) / 2

# 定义 x 的范围和步长
x = -2π:0.1:2π

# 计算对应的 y 值
y = f.(x)  # 注意这里的点号表示对 x 数组中的每个元素应用函数 f

# 创建绘图
plot(x, y,
    label="f(x) = sin(x) + cos(3x)/2",
    xlabel="x",
    ylabel="y",
    title="一个简单函数的图像",
    legend=:topright,
    linewidth=2,
    grid=true
)

# 保存图像到文件 (可选)
# savefig("function_plot.png")

# 在 Julia 的绘图窗口显示图像
println("正在生成图像...")
# 在脚本中，需要保持程序运行才能看到绘图窗口。
# 在 REPL 中，图像会自动显示。