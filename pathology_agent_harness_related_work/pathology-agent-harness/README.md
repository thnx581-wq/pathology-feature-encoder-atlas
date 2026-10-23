# Pathology Agent & Harness：入门调研项目

**阅读者画像**：已有计算病理/WSI/MIL 经验，agent 与 harness 新手；当前按“两张 A6000、LLM 通过 API”规划。
**本轮交付**：六篇重点论文中文笔记、概念入门、比较矩阵、循序学习任务、复现计划和预评测草案。
**核查日期**：2026-09-17。项目名为暂定工作名；目标会议/期刊及 deadline 未定。

## 从哪里开始

先读 [调研总报告](related_work/00_survey.md)，再读 [基础概念](related_work/00_foundations.md)；
按 [学习路线](related_work/00_learning_path.md) 完成第一个小任务。六篇逐篇笔记的入口见 [文献索引](related_work/README.md)。
接手项目的 agent 先读 `AGENTS.md`，再读 `handoff.md`。

## 文件结构

```text
AGENTS.md                       项目范围与约束
handoff.md                      本轮状态及下轮接续
brainstorm.md                   待复现后验证的问题，不是已证明创新
related_work/
  00_survey.md                  总报告与路线判断
  00_foundations.md             从 pathology 出发解释 agent/harness
  00_comparison.md              同口径方法对照
  00_learning_path.md           分阶段学习和小任务
  00_search_log.md              检索范围、版本与局限
  00_evidence_ledger.md         易误读数字与证据审计
  references.bib / manifest.json
  01_react/ ... 06_ahe/         每篇 notes、metadata、原文归档状态
  engineering/                 两篇官方工程资料笔记
复现/                           baseline 计划及 NOT_RUN 报告
experiment/evaluation.md        待冻结的评测草案
experiment/results.md           真实实验结果的追加式账本（目前无实验）
DataSet/ + dataset.md           数据位置与使用范围（目前未接入）
examples/                      工具合同与事件日志示例（合成数据）
scripts/                       下载、离线完整性校验
```

## 本次完成与未完成

已完成在线论文阅读、方法和关键评测口径核查，以及能定位到的官方 README 核查。
**未运行任何 LLM/病理 baseline；未接入真实病例；未修改上游 GitHub 仓库。**

**六篇论文的 PDF 和 LaTeX 本次未能落盘**：在线阅读工具可读，但本地下载失败。
每篇都有明确状态、固定版本 URL；`source/README.md` 只是状态说明，不是作者源码。
因此这是可继续工作的“调研与复现准备包”，不是原文已齐全的文献镜像或完成复现的代码仓库。

```bash
# 在能访问 arXiv 的环境，从本项目根目录运行；Python 3.10+，仅使用标准库。
python scripts/fetch_papers.py --list
python scripts/fetch_papers.py --all
python scripts/check_package.py
```

下载脚本没有在本次环境进行成功联网端到端测试；其离线格式校验和安全解包逻辑已测试，见 `VALIDATION_REPORT.md`。
如果无法连接，请保留失败状态，不生成空 PDF、不伪造 TeX。

## 用好这个包

`notes.md` 中明确分开“原文事实”“本调研分析”“建议复现实验”。
最终科研写作必须再次核对论文版本、下载后的表格/图、真实代码和实际运行结果。
研究问题优先从固定 pipeline 与简单 agent 的真实失败中产生；不要把组件组合直接称为首创。
工作流来源与改动见 [WORKFLOW_PROVENANCE.md](WORKFLOW_PROVENANCE.md)。
