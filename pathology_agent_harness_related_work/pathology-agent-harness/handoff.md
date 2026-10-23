# 交接 — 2026-09-17

## 已完成

按照上游规范建立本地项目；六篇主线文献、两篇工程资料、中文概念解释和学习路线已整理。
重点核查了 PathLab 开源承诺、ACP-Bench 分母、PathNavigate 在线记忆、PathPocket 版本规模差异、AHE 优化与迁移的区别。
官方仓库检查主要停留于 README 和入口说明；没有把检查记录称为完整代码审计。

## 尚未完成

PDF 与 LaTeX 均未下载到本地。在线可读不等于本地归档成功。
没有运行病理 baseline，没有申请数据访问，没有测量 API 开销。`复现/` 下全部报告 NOT_RUN。
没有确定最终论文题目、目标会议或 deadline，也未作新颖性判定。

## 下一步（顺序）

第一步完成 `00_learning_path.md` 的工具合同练习；在联网环境补齐固定版本论文原文。
然后在现有固定划分上跑通一个不含 agent 的 MIL 分析流程，保存输入、配置、预测、指标。
再用同一套工具实现简单单 agent，观察真实错误；最后决定是否需要更复杂 harness 或 self-evolution。

## 不要踩的坑

PathLab 不能链接到同名医院管理软件仓库。PathNavigate 官方 README 的内部名称 SurpriseNav 不是另一篇论文。
PathPocket 按 v2 正文记录“超过 21,000 评测条目”，摘要页另一数字暂列冲突，不能称 21,000 独立患者。
AHE 主结果包含在优化任务集上的进化，不能直接当成新任务测试提升。
暂停在这里不会丢失任何未记录实验，因为本轮没有实验。

## 2026-10-23：整理入 GitHub 仓库

按用户要求，将本包纳入 `thnx581-wq/pathology-feature-encoder-atlas` 的
`pathology_agent_harness_related_work/pathology-agent-harness/` 子目录，并在仓库首页添加阅读入口。
此次仅整理和发布已有文件，未重新核验文献、下载原文或运行真实病理 baseline；此前的未归档和 NOT_RUN 状态继续保留。
发布前重新运行 `scripts/check_package.py`，结构与 Markdown 链接检查 PASS；下载助手 10 项离线单元测试通过。以上检查不代表论文下载或科研实验已完成。
