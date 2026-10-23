# 检索与核查记录

日期：2026-09-17。问题：为只有 pathology 背景的 agent/harness 新手选择少量主线文献，
按照 skJack/research-workflow 形成可接续项目。不是 PRISMA 系统综述，不报告虚构的检索命中/排除篇数。

## 方法

先读取指定仓库的 README、SKILL、抓论文脚本和树结构，明确交付职责。
围绕 pathology agent、pathology harness、workflow execution、whole-slide navigation、evidence grounded pathology、
agentic harness engineering 查询原始论文和作者页面；从论文指向的官方仓库核查入口与发布状态。
重点选择覆盖“循环基础—病理编排—评测—视觉导航—证据检索—自进化”的互补工作，而非按引用量机械排序。
这些是主题记录，不冒充所有查询请求的逐字导出。

## 主要排除/保留判断

保留 ReAct 作为基础控制思想，即使不是新论文。两篇 Anthropic 文章归入 engineering，不冒充学术论文。
PathLab 的同名软件仓库不能作为该论文代码；以论文的 Data and Code Availability 为准。
没有将 WSI 编码器/MIL 模型本身当作 agent 方法，也没有把“有聊天界面”自动视为动态 agent。

## 实际访问状态

六篇论文均进行了在线阅读。ReAct、AHE 还核查了可访问 PDF 的方法/结果页面；其余主要依据 arXiv HTML。
官方 PathNavigate、PathPocket、ACP-Bench、AHE 的 README 已读取。
代码阅读级别为入口与 README 核查；不是完整实现审计，不含环境安装或实验。

容器 clone 无法解析域名，二进制下载接口也未成功，因此没有本地 PDF、LaTeX 或完整作者代码。
每篇单独记录 NOT_DOWNLOADED；下载失败不被解释为 PDF-only 投稿。

## 版本控制

ReAct 2210.03629v3；PathLab 2606.20677v1；ACP-Bench 2607.02598v1；
PathNavigate 2605.23559v1；PathPocket 2606.08093v2；AHE 2604.25850v4。
这是本轮选定的阅读快照；未来更新需新增说明，不能无记录覆盖旧结论。

## 局限

并未穷尽所有相关 2025–2026 工作，也没有新颖性排除检索的完备性保证。
HTML、摘要页、README 可能异步更新；冲突进入 evidence ledger。
引用正式数值前应核查下载后的指定版 PDF 和最终发表版本。后续开源状态可能变化。
