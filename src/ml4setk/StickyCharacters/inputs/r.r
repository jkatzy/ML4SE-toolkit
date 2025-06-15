# 你可能需要先安装 tidyverse 包 (它包含了 dplyr 和 ggplot2):
# install.packages("tidyverse")

library(dplyr)
library(ggplot2)

# 使用内置的 iris 数据集
data("iris")

# 1. 数据处理：计算每个物种 (Species) 的花瓣长度 (Petal.Length) 的统计信息
species_summary <- iris %>%
  group_by(Species) %>%
  summarise(
    AvgPetalLength = mean(Petal.Length),
    MinPetalLength = min(Petal.Length),
    MaxPetalLength = max(Petal.Length),
    Count = n()
  )

cat("--- 按物种分类的花瓣长度统计 ---\n")
print(species_summary)
cat("\n")


# 2. 数据可视化：创建一个箱形图来比较不同物种的花瓣长度分布
cat("--- 正在生成花瓣长度分布的箱形图 ---\n")

plot <- ggplot(iris, aes(x = Species, y = Petal.Length, fill = Species)) +
  geom_boxplot() +  # 创建箱形图
  labs(
    title = "鸢尾花不同物种的花瓣长度分布",
    subtitle = "数据来源: iris 数据集",
    x = "物种 (Species)",
    y = "花瓣长度 (cm)"
  ) +
  theme_minimal() + # 使用一个简洁的主题
  theme(legend.position = "none") # 隐藏图例，因为x轴已经提供了信息

# 打印图表
print(plot)

# 保存图表 (可选)
# ggsave("iris_petal_length_boxplot.png", plot, width = 8, height = 6)