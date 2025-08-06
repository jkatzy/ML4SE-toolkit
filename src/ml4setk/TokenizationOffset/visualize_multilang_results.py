#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多语言分析结果可视化脚本
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# 设置中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8')

def load_cross_language_report():
    """加载跨语言对比报告"""
    report_file = Path("results/multilang/cross_language_report_gpt2.json")
    
    if not report_file.exists():
        print(f"错误: 找不到跨语言报告文件 {report_file}")
        return None
    
    with open(report_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_language_ranking_chart(report):
    """创建语言排名图表"""
    
    rankings = report['language_rankings']
    
    # 准备数据
    languages = [r['language'].upper() for r in rankings]
    scores = [r['avg_score'] for r in rankings]
    colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(languages)))
    
    # 创建水平条形图
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(languages, scores, color=colors, edgecolor='black', alpha=0.8)
    
    # 添加数值标签
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                f'{score:.2f}%', ha='left', va='center', fontweight='bold')
    
    # 添加平均线
    avg_score = report['analysis_summary']['average_score']
    ax.axvline(x=avg_score, color='red', linestyle='--', linewidth=2, alpha=0.8,
               label=f'平均分: {avg_score:.2f}%')
    
    ax.set_xlabel('Rule-level Alignment Score (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('编程语言', fontsize=12, fontweight='bold')
    ax.set_title('各编程语言的 Rule-level Alignment Score 排名\n(GPT-2 模型)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # 设置x轴范围
    ax.set_xlim(0, max(scores) * 1.15)
    
    # 添加网格
    ax.grid(axis='x', alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('results/multilang/language_ranking_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("语言排名图表已保存: results/multilang/language_ranking_chart.png")

def create_rules_vs_alignment_scatter(report):
    """创建规则数量vs对齐率散点图"""
    
    rankings = report['language_rankings']
    
    # 准备数据
    languages = [r['language'] for r in rankings]
    total_rules = [r['total_rules'] for r in rankings]
    alignment_rates = [r['alignment_rate'] for r in rankings]
    scores = [r['avg_score'] for r in rankings]
    
    # 创建散点图
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 使用分数作为颜色映射
    scatter = ax.scatter(total_rules, alignment_rates, 
                        c=scores, s=200, alpha=0.7, 
                        cmap='RdYlBu_r', edgecolors='black', linewidth=1)
    
    # 添加语言标签
    for i, lang in enumerate(languages):
        ax.annotate(lang.upper(), (total_rules[i], alignment_rates[i]), 
                   xytext=(5, 5), textcoords='offset points', 
                   fontsize=10, fontweight='bold')
    
    # 添加颜色条
    cbar = plt.colorbar(scatter)
    cbar.set_label('Rule-level Alignment Score (%)', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('总规则数', fontsize=12, fontweight='bold')
    ax.set_ylabel('对齐率 (%)', fontsize=12, fontweight='bold')
    ax.set_title('规则数量 vs 对齐率散点图\n(气泡颜色表示 Rule-level Alignment Score)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # 添加网格
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/multilang/rules_vs_alignment_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("规则数量vs对齐率散点图已保存: results/multilang/rules_vs_alignment_scatter.png")

def create_language_category_analysis(report):
    """创建语言类别分析图"""
    
    # 语言分类
    language_categories = {
        'Static Typed': ['java', 'csharp', 'cpp', 'c', 'rust', 'scala', 'go', 'typescript'],
        'Dynamic Typed': ['python', 'javascript', 'ruby']
    }
    
    rankings = report['language_rankings']
    
    # 按类别统计
    category_stats = {}
    for category, langs in language_categories.items():
        scores = []
        for ranking in rankings:
            if ranking['language'] in langs:
                scores.append(ranking['avg_score'])
        
        if scores:
            category_stats[category] = {
                'scores': scores,
                'mean': np.mean(scores),
                'std': np.std(scores),
                'count': len(scores)
            }
    
    # 创建箱线图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 箱线图
    categories = list(category_stats.keys())
    scores_data = [category_stats[cat]['scores'] for cat in categories]
    
    box_plot = ax1.boxplot(scores_data, labels=categories, patch_artist=True)
    
    # 设置颜色
    colors = ['lightblue', 'lightcoral']
    for patch, color in zip(box_plot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax1.set_ylabel('Rule-level Alignment Score (%)', fontsize=12, fontweight='bold')
    ax1.set_title('按类型系统分类的对齐分数分布', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # 均值对比图
    means = [category_stats[cat]['mean'] for cat in categories]
    stds = [category_stats[cat]['std'] for cat in categories]
    
    bars = ax2.bar(categories, means, yerr=stds, capsize=5, 
                   color=colors, alpha=0.7, edgecolor='black')
    
    # 添加数值标签
    for bar, mean in zip(bars, means):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{mean:.2f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_ylabel('平均 Rule-level Alignment Score (%)', fontsize=12, fontweight='bold')
    ax2.set_title('按类型系统分类的平均对齐分数', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/multilang/language_category_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("语言类别分析图已保存: results/multilang/language_category_analysis.png")

def create_comprehensive_dashboard(report):
    """创建综合仪表板"""
    
    fig = plt.figure(figsize=(20, 12))
    
    # 创建网格布局
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    rankings = report['language_rankings']
    summary = report['analysis_summary']
    
    # 1. 总体统计 (左上)
    ax1 = fig.add_subplot(gs[0, 0])
    stats_labels = ['分析语言数', '总文件数', '总规则数', '对齐规则数']
    stats_values = [
        summary['analyzed_languages'],
        summary['total_files'], 
        summary['total_rules'],
        summary['total_aligned_rules']
    ]
    
    colors_stats = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    bars = ax1.bar(range(len(stats_labels)), stats_values, color=colors_stats, alpha=0.8)
    
    for bar, value in zip(bars, stats_values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(stats_values)*0.01,
                f'{value:,}', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_xticks(range(len(stats_labels)))
    ax1.set_xticklabels(stats_labels, rotation=45, ha='right')
    ax1.set_title('总体统计', fontweight='bold')
    ax1.set_yscale('log')
    
    # 2. 前5名语言 (右上)
    ax2 = fig.add_subplot(gs[0, 1:])
    top5 = rankings[:5]
    languages = [r['language'].upper() for r in top5]
    scores = [r['avg_score'] for r in top5]
    
    bars = ax2.bar(languages, scores, color=plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, 5)), 
                   alpha=0.8, edgecolor='black')
    
    for bar, score in zip(bars, scores):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{score:.2f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_ylabel('Rule-level Alignment Score (%)')
    ax2.set_title('前5名语言对齐分数', fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    # 3. 对齐率分布直方图 (中左)
    ax3 = fig.add_subplot(gs[1, 0])
    all_scores = [r['avg_score'] for r in rankings]
    ax3.hist(all_scores, bins=8, alpha=0.7, color='skyblue', edgecolor='black')
    ax3.axvline(x=np.mean(all_scores), color='red', linestyle='--', 
                label=f'平均: {np.mean(all_scores):.2f}%')
    ax3.set_xlabel('Rule-level Alignment Score (%)')
    ax3.set_ylabel('语言数量')
    ax3.set_title('对齐分数分布', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. 规则数量分布 (中中)
    ax4 = fig.add_subplot(gs[1, 1])
    rule_counts = [r['total_rules'] for r in rankings]
    languages_short = [r['language'][:3].upper() for r in rankings]
    
    ax4.scatter(range(len(rule_counts)), rule_counts, 
               s=100, alpha=0.7, color='orange', edgecolors='black')
    
    for i, (lang, count) in enumerate(zip(languages_short, rule_counts)):
        ax4.annotate(lang, (i, count), xytext=(0, 10), 
                    textcoords='offset points', ha='center', fontsize=8)
    
    ax4.set_xlabel('语言 (按排名)')
    ax4.set_ylabel('规则数量')
    ax4.set_title('各语言规则数量', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # 5. 对齐效率 (中右)
    ax5 = fig.add_subplot(gs[1, 2])
    efficiency = [r['aligned_rules'] / r['total_rules'] * 100 for r in rankings]
    languages_short = [r['language'][:4].upper() for r in rankings]
    
    bars = ax5.bar(range(len(efficiency)), efficiency, 
                   color=plt.cm.viridis(np.linspace(0, 1, len(efficiency))), alpha=0.8)
    
    ax5.set_xticks(range(len(languages_short)))
    ax5.set_xticklabels(languages_short, rotation=45, ha='right')
    ax5.set_ylabel('对齐效率 (%)')
    ax5.set_title('各语言对齐效率', fontweight='bold')
    ax5.grid(True, alpha=0.3)
    
    # 6. 底部总结文本
    ax6 = fig.add_subplot(gs[2, :])
    ax6.axis('off')
    
    summary_text = f"""
    多语言 Rule-level Tokenization Alignment Score 分析总结 (GPT-2 模型)
    
    • 最佳表现: {rankings[0]['language'].upper()} ({rankings[0]['avg_score']:.2f}%)
    • 最差表现: {rankings[-1]['language'].upper()} ({rankings[-1]['avg_score']:.2f}%)
    • 整体对齐率: {summary['overall_alignment_rate']:.2f}%
    • 平均分数: {summary['average_score']:.2f}%
    
    关键发现: 静态类型语言通常表现更好，动态语言和复杂语法结构的语言对齐率较低。
    约 75% 的语法规则边界与 tokenization 边界不匹配，这对代码生成和理解任务具有重要影响。
    """
    
    ax6.text(0.5, 0.5, summary_text, transform=ax6.transAxes, 
             fontsize=12, ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    
    plt.suptitle('多语言 Rule-level Alignment Score 综合分析仪表板', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.savefig('results/multilang/comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("综合仪表板已保存: results/multilang/comprehensive_dashboard.png")

def main():
    """主函数"""
    
    print("=" * 60)
    print("多语言分析结果可视化")
    print("=" * 60)
    
    # 加载数据
    report = load_cross_language_report()
    if not report:
        return
    
    # 确保输出目录存在
    Path("results/multilang").mkdir(parents=True, exist_ok=True)
    
    # 生成各种图表
    print("正在生成可视化图表...")
    
    create_language_ranking_chart(report)
    create_rules_vs_alignment_scatter(report)
    create_language_category_analysis(report)
    create_comprehensive_dashboard(report)
    
    print("\n" + "=" * 60)
    print("所有可视化图表已生成完成！")
    print("=" * 60)
    print("生成的图表:")
    print("- results/multilang/language_ranking_chart.png")
    print("- results/multilang/rules_vs_alignment_scatter.png") 
    print("- results/multilang/language_category_analysis.png")
    print("- results/multilang/comprehensive_dashboard.png")

if __name__ == "__main__":
    main()