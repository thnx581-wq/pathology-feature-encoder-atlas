# Contributing / 贡献指南

本项目欢迎补充**具有可核实论文或技术报告、公开代码/权重入口、明确特征输出定义**的病理特征提取器。

## 添加新模型

1. 查阅 [data/models.json](data/models.json)，避免重复收录相同权重。
2. 在文件中添加一条 JSON 对象。主要字段：
   - `id`：唯一、全小写的连字符标识符；`name`, `year`, `level`：模型名、版本年份、`Patch`/`WSI`；
   - `inference_modality`：提取特征时实际需要的模态；`pretrain_modality`：预训练采用的模态；
   - `feature_dim`：以**明确提取接口**返回的嵌入维度为准；
   - `feature_definition`：例如 CLS、mean-pooled tokens、CLIP projected embedding；
   - `paper_url`、`weight_url`、`code_url`：论文/摘要/模型卡，官方权重和代码页面；
   - `weight_access`：`公开`、`受限` 或 `仓库下载`；
   - `upstream`：如果为 WSI encoder，说明前置 Patch encoder 的**具体版本及其特征维度**；
   - `recommended_input`、`notes`：倍率、MPP、Patch 输入尺寸和限制；
   - `paper_kind`：`论文`、`模型卡` 或 `会议摘要`。
3. 运行：

```bash
python scripts/build_site.py
python scripts/validate.py
```

4. 提交同时修改的 `data/models.json`、`data/models.csv`、`README.md` 和 `index.html`。

## 质量原则

- **不要把隐藏维度误当作实际导出维度**。CLS-only 与 CLS+mean-pooled tokens 必须说明差异。
- 尽可能引用作者官方 GitHub/Hugging Face。模型仓库有访问权限门槛须标记。
- WSI encoder 应说明依赖的上游 Patch encoder 与是否需要 Patch 坐标。
- 上游使用的训练模态**不等于**下游推理必需模态。例如联合 RNA 预训练后可能仅输入 H&E。
- 不擅自将项目年份写成论文正式发表年份；若只有摘要/模型卡要明确标记。
- 若项目权重或代码尚未公开，暂不收录或将该项记录为待核实，不虚构链接。

## 备注

项目脚本仅校验数据结构以及本地网页和表格的一致性。**不自动验证真实权重下载、访问审批、许可证或实际推理张量形状**。所有第三方权重由原始作者发布与维护。
