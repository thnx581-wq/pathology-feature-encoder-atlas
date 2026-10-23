# AGENTS — 项目总纲

## 目标

学习并调研 pathology agent / agent harness，选择可在两张 A6000 + LLM API 条件下验证的问题。
首选探索：病理科研工作流可靠执行与证据核验；备选：预算受限 WSI 导航。
这只是方向优先级，不是已确认新颖性、投稿结论或性能承诺。会议/期刊、deadline 未定。

## 每次接手

先读本文件，再读 `handoff.md`。文献看 `related_work/README.md`；跑实验前看 `experiment/evaluation.md`。
每次结束更新 handoff；真实实验追加 results，不覆盖失败记录。

## 术语

WSI、ROI、MIL、agent、tool calling、harness、workflow、RAG、trace、verifier、artifact、self-evolution。
通俗解释在 `related_work/00_foundations.md`。不要自造术语来包装已有机制。

## 硬约束

1. 文献原文数字、分析推论、本项目实测结果分开。没有运行就写 NOT_RUN；没有 PDF 就写未归档。
2. 代码“公开”不等于数据、模型权重、依赖全部可复现；README 阅读不等于逐行审计。
3. 先固定数据/患者划分、标签与任务定义。切片或 patch 数不是独立患者数。
4. LLM 不得改变标签、删失含义、测试划分、评分器、预算或“通过”标准来改善结果。
5. 原始患者资料保留在授权本地环境；API 只接收经批准的最小必要去标识信息。此包不含任何患者数据。
6. 不训练大模型作为前提；agent 的改进需与规则验证器和同预算简单 agent 比较。
7. 不在测试失败上更新 memory/skills 后再把同一测试集报告为独立测试。
8. 不使用生成的叙述替代工具实际产物；保留工具参数、输出状态、文件哈希、关键决策摘要。
9. 需要审批的外部发送、数据许可变更或不可逆动作不能由 agent 自动越权。
10. 不改动未授权远程仓库；本包为本地调研目录。

## 当前阶段

文献调研与复现准备。所有真实 baseline 均未运行。评测协议为 DRAFT，需在首轮正式实验前冻结。
