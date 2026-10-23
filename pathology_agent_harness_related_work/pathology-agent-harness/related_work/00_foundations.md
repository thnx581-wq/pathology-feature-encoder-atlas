# 从计算病理理解 agent 与 harness

这是一份教学解释。概念依据 ReAct 与两篇 Anthropic 官方工程资料；病理例子是本调研设计的类比，
不是这些来源已经验证过的系统。术语在不同社区存在边界差异，下表采用适合本项目的工作定义。[R1][E1][E2]

## 1. 先从你熟悉的 pipeline 开始

```text
WSI → 切 patch → 提特征 → MIL → 保存预测 → 计算指标
```

如果所有步骤和异常处理都由 Python 提前写好，这是固定 workflow。
如果模型只把“我要做二分类”转成配置，之后仍按固定步骤执行，它更像自然语言配置器。
如果模型看到“特征缺失”后决定检查文件、选择允许的补救动作，并在新观察后继续判断，才体现了 agent 循环。

| 概念 | 工作定义 | 病理例子 |
|---|---|---|
| LLM | 解释意图、选择动作、整理输出的模型 | 判断当前应查数据还是调用评估 |
| Tool | 有明确输入和输出的可执行操作 | 校验患者划分、提特征、训练 ABMIL |
| Agent | 基于状态与工具反馈反复选择动作的系统 | 发现漏了特征后先检查，而不是继续训练 |
| Harness | 围绕模型的运行控制、状态管理、验证、预算和审计 | 限制工具、保存日志、阻止测试集泄漏 |
| Framework | 帮你实现上述部件的软件开发工具 | 不等于科学创新，也不保证系统可靠 |
| Skill | 可复用的方法说明或受限子流程 | “固定 split 的 WSI 二分类评估” |
| RAG | 先检索外部内容，再据此生成 | 查指南/论文后回答；本身不必是 agent |
| Trace | 实际发生的行动与观察记录 | 工具名、参数、状态、产物路径与摘要 |
| Verifier | 独立判断某一步或结果是否合格 | 检查预测 ID 是否与测试清单一致 |
| Artifact | 可检查的真实产物 | config、预测 CSV、指标 JSON、checkpoint |

## 2. 为什么“聪明的模型”仍需要 harness

假设模型提出运行 `evaluate(pred.csv)`。它可能没有意识到 `pred.csv` 属于上一轮训练。
语言上回答正确，不代表文件对应正确；进程退出码为 0，也不代表患者匹配正确。

为这个教学场景设计的 harness 可以要求：

```text
请求 → 工具参数校验 → 输入身份/版本检查 → 受限执行
     → 输出合同检查 → 更新状态和日志 → 允许继续或停止
```

模型负责选择，工具负责计算，harness 约束和记录，verifier 独立检查。
这四者尽量解耦，才能判断到底是模型不会选、工具本身有 bug，还是运行控制出错。
这里的约束不应仅写在 prompt 中；关键规则应有代码检查。

## 3. 一次工具调用的“合同”是什么

不是“请帮我检查一下”，而是：

```json
{
  "tool": "validate_patient_split",
  "input": {
    "manifest_path": "DataSet/manifest.csv",
    "split_path": "DataSet/split.csv"
  },
  "output_contract": {
    "status": "passed | blocked | error",
    "patient_overlap": "integer",
    "artifact_path": "relative path or null",
    "error_code": "string or null"
  }
}
```

这是合同示例，不是某一家 API 的官方函数格式，也不是已部署工具。
“blocked”表示有可靠证据拒绝继续；“error”表示工具没有得出可信检查结果。
两者不能合并为“验证完成”。样例见 `examples/`。

## 4. memory 有三种完全不同的范围

单次运行状态记录“执行到哪”；文献/病例检索库记录“可以查什么”；跨任务经验库记录“以后怎么处理”。
此外，PathNavigate 的 slide memory 是单张切片内在线适应的数值模型，不等同于保存对话摘要。[R4]

本项目建议：每个 patient/slide 的局部状态隔离；长期经验只来自开发集；最终测试时冻结经验库。
否则“记忆增强”可能只是把测试答案带到了下一次查询里。

## 5. self-evolution 不等于多写一次反思

教学上的最低闭环是：

```text
开发任务失败 → 记录可复查证据 → 提议一个具体改动
→ 在独立开发验证任务重跑 → 同时检查改进与回退 → 接受或回滚
```

固定 LLM，也可以改 prompt、工具合同或 skill；这与训练大模型权重是不同的适应位置。[R6]
只有“我应该更仔细”而没有实际改动和再测，不能据此声称系统进化。
最终盲测集不得进入这个更新循环。

## 6. 最先学什么，不用急着学什么

先能读写 JSON、封装函数、处理异常、记录事件、保存状态、写自动化断言，再接一次真实 LLM 工具调用。
先用一个 agent 和少量白名单工具。暂时不以多智能体通信、分布式服务或大型知识图谱为前置条件。
这是降低调试变量的学习建议，不是声称这些技术没有研究价值。

## 参考

[R1] ReAct：https://arxiv.org/abs/2210.03629v3
[R4] PathNavigate：https://arxiv.org/html/2605.23559v1
[R6] AHE：https://arxiv.org/html/2604.25850v4
[E1] https://www.anthropic.com/engineering/building-effective-agents
[E2] https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
