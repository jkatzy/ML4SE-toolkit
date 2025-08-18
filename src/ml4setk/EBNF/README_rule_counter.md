# EBNF Rule Counter

这是一个基于tree-sitter的EBNF规则计数工具，可以分析源代码并统计各种语法规则的使用频率。

## 功能特性

- **代码解析**: 使用tree-sitter解析源代码，生成抽象语法树(AST)
- **规则映射**: 将AST节点类型映射到EBNF语法规则
- **统计计数**: 统计每种规则在代码中的出现次数
- **多种输入**: 支持单个文件、JSONL文件等多种输入格式
- **结果导出**: 支持JSON和CSV格式的结果导出
- **可视化报告**: 生成详细的分析报告

## 安装依赖

```bash
pip install -r requirements.txt
```

## 基本用法

### 1. 基本代码分析

```python
from rule_counter import RuleCounter

# 创建计数器
counter = RuleCounter(language="python")

# 分析代码
code = """
def hello(name):
    return f"Hello, {name}!"

result = hello("World")
print(result)
"""

counts = counter.count_rules_in_code(code)
counter.print_summary(counts)
```

### 2. 文件分析

```python
# 分析单个Python文件
counts = counter.count_rules_in_file("example.py")
counter.save_counts_to_json(counts, "results.json")
```

### 3. JSONL文件分析

```python
# 分析JSONL文件（如HumanEval数据集）
counts = counter.count_rules_in_jsonl("data/HumanEval.jsonl")
counter.print_summary(counts, top_n=20)
```

## 命令行使用

### 基本命令

```bash
# 分析Python文件
python rule_counter.py example.py --output results.json

# 分析JSONL文件
python rule_counter.py data/HumanEval.jsonl --output humaneval_counts.json

# 指定语言和显示前30个规则
python rule_counter.py code.py --language python --top-n 30
```

### 集成工作流

```bash
# 使用集成处理器进行完整分析
python integrated_rule_processor.py data/HumanEval.jsonl --work-dir results --base-name humaneval
```

## 输出格式

### JSON格式
```json
{
  "metadata": {
    "language": "python",
    "total_rules": 45,
    "total_occurrences": 1250
  },
  "rule_counts": {
    "identifier": 320,
    "function_definition": 85,
    "call": 78,
    "assignment": 65,
    "return_statement": 45
  }
}
```

### CSV格式
```csv
name,count
identifier,320
function_definition,85
call,78
assignment,65
return_statement,45
```

## 支持的语言

目前支持的编程语言：
- Python (完全支持)

计划支持的语言：
- Java
- JavaScript
- C/C++
- Go

## 规则映射

工具将tree-sitter的AST节点类型映射到EBNF语法规则。主要的映射包括：

### Python语言映射
- `function_definition` → `function_definition`
- `class_definition` → `class_definition`
- `if_statement` → `if_statement`
- `for_statement` → `for_statement`
- `call` → `call`
- `binary_operator` → `binary_operator`
- 等等...

## 高级功能

### 集成处理器

`IntegratedRuleProcessor`类提供了完整的工作流：

```python
from integrated_rule_processor import IntegratedRuleProcessor

processor = IntegratedRuleProcessor(language="python", work_dir="results")
results = processor.process_complete_workflow("data/code.jsonl", "analysis")
```

这将生成：
- JSON格式的规则计数
- CSV格式的规则计数
- Markdown格式的分析报告

### 自定义规则映射

可以通过修改`RuleCounter`类中的`rule_mapping`字典来自定义规则映射：

```python
counter = RuleCounter(language="python")
counter.rule_mapping["custom_node"] = "custom_rule"
```

## 示例和测试

运行测试脚本：
```bash
python test_rule_counter.py
```

运行使用示例：
```bash
python example_usage.py
```

## 与现有工具集成

该工具可以与项目中现有的EBNF工具集成：

1. **SVG可视化**: 生成的CSV文件可以用于`svg_coloring.py`进行可视化
2. **数据处理**: 与`real_data_processor.py`兼容
3. **报告生成**: 生成的分析报告可以与其他分析工具结合

## 性能考虑

- 大文件处理：工具针对大型代码库进行了优化
- 内存使用：采用流式处理减少内存占用
- 并发处理：支持多文件并发分析（计划功能）

## 故障排除

### 常见问题

1. **tree-sitter解析错误**
   - 确保代码语法正确
   - 检查编码格式（建议使用UTF-8）

2. **规则映射缺失**
   - 某些AST节点可能没有对应的EBNF规则
   - 可以通过自定义映射解决

3. **性能问题**
   - 对于大型文件，考虑分批处理
   - 使用`--top-n`参数限制输出规则数量

### 调试模式

启用详细输出：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork项目
2. 创建功能分支
3. 添加测试
4. 提交Pull Request

## 许可证

本项目采用MIT许可证。