# 证据台账与易误读点

“确认”仅指来源支持该表述；不表示本项目独立复现了结果。日期 2026-09-17。

| 编号 | 记录 | 正确解释/处理 | 来源与定位 |
|---|---|---|---|
| E01 | PathLab 的非劣效界值 | 按相对性能变化解释，不能改写为所有 AUC 都允许下降 5 个百分点 | R2，Methods / Statistical analysis |
| E02 | PathLab 操作时间 | 编排/生成可执行工作流的操作时间，不是所有 GPU 训练的总时长 | R2，time-motion / orchestration |
| E03 | PathLab 自改进生态 | Discussion 的未来方向，不能当成已完成自进化验证 | R2，Discussion |
| E04 | PathLab 开源 | 正文称同行评议发表后公开；本次未核实完整官方仓库 | R2，Data and Code Availability |
| E05 | ACP-Bench 369 | 41 工作流 × 9 模型–harness 配置；不是再乘 3 个 harness | R3，evaluation setup |
| E06 | ACP-Bench 严格通过 10/369 | 该研究评分规范下的全轨迹分母；不是普遍医学准确率 | R3，workflow execution |
| E07 | ACP-Bench 可恢复诊断结果子集 | 139 条轨迹的条件性分析不能代替全部 369 条 | R3，denominators / diagnostic subset |
| E08 | ACP-Bench 官方代码 | README 标示 progressive release、非完整复现包 | C3，Repository Status |
| E09 | PathNavigate “training-free” | 预训练大模块冻结，但单张切片小型 memory 有在线 SGD | R4，Memory Update，公式 2–3 |
| E10 | PathNavigate surprise | 切片内重构梯度范数产生的 atypicality，不是肿瘤标签 | R4，Surprise-Guided Scan |
| E11 | PathNavigate 代码名称 | 官方仓库 PathNavigate_ 的 README 使用 SurpriseNav；不要误认为另一篇论文 | C4，README |
| E12 | PathPocket 评测规模冲突 | 本次摘要页返回 over 200,000，v2 HTML 与 README 为 over 21,000；记录冲突，按正文“评测条目”引用，不用 200,000 | R5 与 R5a、C5 |
| E13 | PathPocket 6.8% | 原文相对提升口径；80.4%→85.8% 是 5.4 个百分点，不能混写 | R5，reader-study Results |
| E14 | PathPocket corpus | public + authorized，不表示全部可以自由重新分发；评测含私有数据 | R5，Methods / Limitations |
| E15 | PathPocket 视觉模型分工 | TITAN/CONCHv1.5 与 Virchow2 承担不同角色；不是发现版本矛盾的充分依据 | R5，Infrastructure / Implementation |
| E16 | AHE 69.7%→77.0% | 在 89 个参与进化的 Terminal-Bench 任务上，不能称独立未见任务增益 | R6，§4.1–4.2 |
| E17 | AHE 冻结迁移 | SWE-bench-verified 汇总 75.2%→75.6%，与主基准优化分开讨论 | R6，§4.3 / Table 2；PDF 表页核查 |
| E18 | AHE 可复现性 | README 明示 Agent Debugger 部分开源，不声称全部组件已公开 | C6，Agent Debugger licensing |
| E19 | 本包实验状态 | 所有文献性能均为作者报告，本项目没有实测 agent 成功率 | 本项目 results.md |

## 冲突的处置原则

E12 暂按固定版本正文与代码 README 一致口径记录，但摘要页为何不同尚未确认。
正式投稿引用样本规模前应核查指定 PDF / supplementary / 作者确认，不能以猜测解释差异。
其他尚未运行或下载的材料也保留明确状态，不通过补写“合理数字”填空。

## 来源

R2 https://arxiv.org/html/2606.20677v1
R3 https://arxiv.org/html/2607.02598v1
R4 https://arxiv.org/html/2605.23559v1
R5 https://arxiv.org/html/2606.08093v2
R5a https://arxiv.org/abs/2606.08093
R6 https://arxiv.org/html/2604.25850v4
C3 https://github.com/jaylinio/ACP-Bench
C4 https://github.com/Pureeeee/PathNavigate_
C5 https://github.com/zhexu1997/PathPocket
C6 https://github.com/china-qijizhifeng/agentic-harness-engineering
