# Pathology Feature Encoder Atlas

> A curated directory of pathology feature extractors and whole-slide representation models.  
> **病理特征提取器导航：论文、推理模态、预训练模态、特征维度、官方权重和代码。**

**资料核查日期：2026-10-23** · **收录：44 个模型条目（Patch 33 / WSI 11）** · [打开可搜索网页](./index.html) · [下载 CSV](./data/models.csv) · [机器可读 JSON](./data/models.json)

## 为什么建立这个列表？

在 WSI 分类、MIL、基因突变预测、预后分析及病理图文任务中，`feature extractor` 的输出维度**不等同于**网络隐藏层宽度。也不能混淆 **Patch 特征** `(N_patches, D_patch)` 与 **WSI 特征** `(D_slide,)`。不同模型的 `CLS`、`pooler_output`、Patch 均值和图文投影层可以返回完全不同的维度。

本列表优先关联官方模型卡及官方代码仓库；**“受限”表示通常需要登录 Hugging Face、同意条款或提交访问申请，并不代表模型不可获取**；“仓库下载”则是官方仓库提供下载说明，未必有一个可长期访问的直链。权重仍受原作者许可证约束。该目录不是模型性能排行榜。

**如何理解模态**：`推理输入模态` 表示提取特征时需要的数据（例如 H&E 图像）；`预训练模态` 表示训练阶段曾使用的数据（例如 WSI+转录组、病理图像+文本）。后者不意味着模型在推理时必须提供所有模态。

## Patch-level / Tile-level 特征提取器

表中 `特征维度` 为推荐/列明的提取接口结果；具体 pooling 定义见本文件后半部分。

| 模型 | 年份 | 推理输入模态 | 预训练模态 | 特征维度 | 论文 | 权重 | 代码 | 访问方式 |
|---|---:|---|---|---:|---|---|---|---|
| **CONCH-Z** | 2026 | H&E 病理图像 | 病理图像+文本 | 768 | [论文](https://arxiv.org/abs/2610.17233) | [权重/入口](https://huggingface.co/MahmoodLab/CONCH-Z) | [代码](https://github.com/mahmoodlab/LIMIT) | 受限 |
| **GenBio-PathFM** | 2026 | H&E 病理图像 | H&E | 4608 | [论文](https://www.biorxiv.org/content/10.64898/2026.03.17.712534v1) | [权重/入口](https://huggingface.co/genbio-ai/genbio-pathfm) | [代码](https://github.com/genbio-ai/genbio-pathfm) | 公开 |
| **GigaPath-Flash (Tile)** | 2026 | H&E 病理图像 | H&E | 384 | [论文](https://arxiv.org/abs/2607.18218) | [权重/入口](https://huggingface.co/prov-gigapath/prov-gigapath-flash) | [代码](https://github.com/prov-gigapath/prov-gigapath) | 受限 |
| **H-Optimus-1** | 2026 | H&E 病理图像 | H&E | 1536 | [会议摘要](https://doi.org/10.1158/1538-7445.AM2026-LB174) | [权重/入口](https://huggingface.co/bioptimus/H-optimus-1) | [代码](https://huggingface.co/bioptimus/H-optimus-1) | 受限 |
| **KEEP** | 2026 | 病理图像 | 病理图像+文本 | 768 | [论文](https://doi.org/10.1016/j.ccell.2026.01.019) | [权重/入口](https://huggingface.co/Astaxanthin/KEEP) | [代码](https://github.com/MAGIC-AI4Med/KEEP) | 公开 |
| **Mascaret** | 2026 | H&E 病理图像 | H&E | 1536 | [论文](https://arxiv.org/abs/2607.22861) | [权重/入口](https://huggingface.co/wearewaiv/mascaret) | [代码](https://huggingface.co/wearewaiv/mascaret) | 受限 |
| **Phaet** | 2026 | H&E 病理图像 | H&E | 1024 | [论文](https://arxiv.org/abs/2607.22861) | [权重/入口](https://huggingface.co/wearewaiv/phaet) | [代码](https://huggingface.co/wearewaiv/phaet) | 受限 |
| **CONCH v1.5** | 2025 | H&E 病理图像 | 视觉基础模型 / TITAN 上游 | 768 | [论文](https://doi.org/10.1038/s41591-025-03982-3) | [权重/入口](https://huggingface.co/MahmoodLab/conchv1_5) | [代码](https://github.com/mahmoodlab/TITAN) | 受限 |
| **GPFM** | 2025 | H&E 病理图像 | H&E | 1024 | [论文](https://doi.org/10.1038/s41551-025-01488-4) | [权重/入口](https://huggingface.co/majiabo/GPFM) | [代码](https://github.com/birkhoffkiki/GPFM) | 公开 |
| **H0-mini** | 2025 | H&E 病理图像 | H&E | 768 | [论文](https://arxiv.org/abs/2501.16239) | [权重/入口](https://huggingface.co/bioptimus/H0-mini) | [代码](https://huggingface.co/bioptimus/H0-mini) | 受限 |
| **Midnight-12k** | 2025 | H&E 病理图像 | H&E | 3072 | [论文](https://arxiv.org/abs/2504.05186) | [权重/入口](https://huggingface.co/kaiko-ai/midnight) | [代码](https://github.com/kaiko-ai/midnight) | 公开 |
| **mSTAR** | 2025 | H&E 病理图像 | H&E WSI + 病理报告 + RNA-Seq | 1024 | [论文](https://doi.org/10.1038/s41467-025-66220-x) | [权重/入口](https://huggingface.co/Wangyh/mSTAR) | [代码](https://github.com/Innse/mSTAR) | 受限 |
| **MUSK** | 2025 | H&E 病理图像 | 病理图像+文本 | 1024 | [论文](https://doi.org/10.1038/s41586-024-08378-w) | [权重/入口](https://huggingface.co/xiangjx/musk) | [代码](https://github.com/lilab-stanford/MUSK) | 受限 |
| **PathOrchestra** | 2025 | 多染色病理图像 | 多来源、多组织病理图像 | 1024 | [论文](https://doi.org/10.1038/s41746-025-02027-w) | [权重/入口](https://huggingface.co/AI4Pathology/PathOrchestra) | [代码](https://github.com/yanfang-research/PathOrchestra) | 受限 |
| **UNI2-h** | 2025 | H&E 病理图像 | H&E | 1536 | [论文](https://doi.org/10.1038/s41591-024-02857-3) | [权重/入口](https://huggingface.co/MahmoodLab/UNI2-h) | [代码](https://github.com/mahmoodlab/UNI) | 受限 |
| **CONCH (v1)** | 2024 | H&E / IHC / 特殊染色图像 | 病理图像+文本 | 512 | [论文](https://doi.org/10.1038/s41591-024-02856-4) | [权重/入口](https://huggingface.co/MahmoodLab/CONCH) | [代码](https://github.com/mahmoodlab/CONCH) | 受限 |
| **H-Optimus-0** | 2024 | H&E 病理图像 | H&E | 1536 | [模型卡](https://huggingface.co/bioptimus/H-optimus-0) | [权重/入口](https://huggingface.co/bioptimus/H-optimus-0) | [代码](https://huggingface.co/bioptimus/H-optimus-0) | 受限 |
| **Hibou-B** | 2024 | 多染色病理图像 | 多组织、多染色病理图像 | 768 | [论文](https://arxiv.org/abs/2406.05074) | [权重/入口](https://huggingface.co/histai/hibou-b) | [代码](https://github.com/HistAI/hibou) | 受限 |
| **Hibou-L** | 2024 | 多染色病理图像 | 多组织、多染色病理图像 | 1024 | [论文](https://arxiv.org/abs/2406.05074) | [权重/入口](https://huggingface.co/histai/hibou-L) | [代码](https://github.com/HistAI/hibou) | 受限 |
| **Kaiko ViT-L/14** | 2024 | H&E 病理图像 | H&E | 1024 | [论文](https://arxiv.org/abs/2404.15217) | [权重/入口](https://github.com/kaiko-ai/towards_large_pathology_fms) | [代码](https://github.com/kaiko-ai/towards_large_pathology_fms) | 仓库下载 |
| **Phikon-v2** | 2024 | H&E 病理图像 | H&E | 1024 | [论文](https://arxiv.org/abs/2409.09173) | [权重/入口](https://huggingface.co/owkin/phikon-v2) | [代码](https://github.com/owkin/HistoSSLscaling) | 公开 |
| **Prov-GigaPath (Tile)** | 2024 | H&E 病理图像 | H&E | 1536 | [论文](https://doi.org/10.1038/s41586-024-07441-w) | [权重/入口](https://huggingface.co/prov-gigapath/prov-gigapath) | [代码](https://github.com/prov-gigapath/prov-gigapath) | 受限 |
| **UNI** | 2024 | H&E 病理图像 | H&E | 1024 | [论文](https://doi.org/10.1038/s41591-024-02857-3) | [权重/入口](https://huggingface.co/MahmoodLab/UNI) | [代码](https://github.com/mahmoodlab/UNI) | 受限 |
| **Virchow** | 2024 | H&E 病理图像 | H&E | 2560 | [论文](https://doi.org/10.1038/s41591-024-03141-0) | [权重/入口](https://huggingface.co/paige-ai/Virchow) | [代码](https://huggingface.co/paige-ai/Virchow) | 受限 |
| **Virchow2** | 2024 | H&E 病理图像 | 多倍率、多来源病理图像 | 2560 | [论文](https://arxiv.org/abs/2408.00738) | [权重/入口](https://huggingface.co/paige-ai/Virchow2) | [代码](https://huggingface.co/paige-ai/Virchow2) | 受限 |
| **BiomedCLIP** | 2023 | 生物医学图像 | 广义生物医学图像+文本 | 512 | [论文](https://arxiv.org/abs/2303.00915) | [权重/入口](https://huggingface.co/microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224) | [代码](https://github.com/microsoft/BiomedCLIP) | 公开 |
| **Google Path Foundation** | 2023 | H&E 病理图像 | H&E | 384 | [论文](https://arxiv.org/abs/2310.13259) | [权重/入口](https://huggingface.co/google/path-foundation) | [代码](https://github.com/Google-Health/path-foundation) | 受限 |
| **Phikon** | 2023 | H&E 病理图像 | H&E | 768 | [论文](https://doi.org/10.1101/2023.07.21.23292757) | [权重/入口](https://huggingface.co/owkin/phikon) | [代码](https://github.com/owkin/HistoSSLscaling) | 公开 |
| **PLIP** | 2023 | 病理图像 | 病理图像+文本 | 512 | [论文](https://doi.org/10.1038/s41591-023-02504-3) | [权重/入口](https://huggingface.co/vinid/plip) | [代码](https://github.com/PathologyFoundation/plip) | 公开 |
| **RetCCL / CCL** | 2023 | H&E 病理图像 | H&E | 2048 | [论文](https://doi.org/10.1016/j.media.2022.102645) | [权重/入口](https://github.com/Xiyue-Wang/RetCCL) | [代码](https://github.com/Xiyue-Wang/RetCCL) | 仓库下载 |
| **CTransPath** | 2022 | H&E 病理图像 | H&E | 768 | [论文](https://doi.org/10.1016/j.media.2022.102559) | [权重/入口](https://github.com/Xiyue-Wang/TransPath) | [代码](https://github.com/Xiyue-Wang/TransPath) | 仓库下载 |
| **HIPT (ViT-256)** | 2022 | H&E 病理图像 | H&E | 384 | [论文](https://arxiv.org/abs/2206.02647) | [权重/入口](https://github.com/mahmoodlab/HIPT) | [代码](https://github.com/mahmoodlab/HIPT) | 仓库下载 |
| **ResNet-50 (ImageNet)** | 2016 | 病理图像 | 自然图像监督预训练 | 2048 | [论文](https://arxiv.org/abs/1512.03385) | [权重/入口](https://pytorch.org/vision/stable/models/generated/torchvision.models.resnet50.html) | [代码](https://github.com/pytorch/vision) | 公开 |

## WSI-level / Slide-level 特征提取器

WSI 模型的输入通常是**预先提取的 Patch 向量及空间坐标**，而非直接读入整个 gigapixel 张量；其上游 Patch 编码器必须与预训练时使用的版本匹配。

| 模型 | 年份 | 推理输入模态 | 预训练模态 | 特征维度 | 论文 | 权重 | 代码 | 访问方式 |
|---|---:|---|---|---:|---|---|---|---|
| **GigaPath-Flash (Slide)** | 2026 | H&E 病理图像 | 病理图像（WSI） | 384 | [论文](https://arxiv.org/abs/2607.18218) | [权重/入口](https://huggingface.co/prov-gigapath/prov-gigapath-flash) | [代码](https://github.com/prov-gigapath/prov-gigapath) | 受限 |
| **FEATHER-24K (CONCHv1.5)** | 2025 | H&E 病理图像 | WSI 监督预训练 / PC-108 | 512 | [论文](https://arxiv.org/abs/2506.09022) | [权重/入口](https://huggingface.co/MahmoodLab/abmil.base.conch_v15.pc108-24k) | [代码](https://github.com/mahmoodlab/MIL-Lab) | 受限 |
| **FEATHER-24K (UNI)** | 2025 | H&E 病理图像 | WSI 监督预训练 / PC-108 | 512 | [论文](https://arxiv.org/abs/2506.09022) | [权重/入口](https://huggingface.co/MahmoodLab/abmil.base.uni.pc108-24k) | [代码](https://github.com/mahmoodlab/MIL-Lab) | 受限 |
| **FEATHER-24K (UNI2-h)** | 2025 | H&E 病理图像 | WSI 监督预训练 / PC-108 | 512 | [论文](https://arxiv.org/abs/2506.09022) | [权重/入口](https://huggingface.co/MahmoodLab/abmil.base.uni_v2.pc108-24k) | [代码](https://github.com/mahmoodlab/MIL-Lab) | 受限 |
| **PRISM2** | 2025 | H&E 病理图像 | WSI + 文本/临床病理知识 | 2560 | [论文](https://arxiv.org/abs/2506.13063) | [权重/入口](https://huggingface.co/paige-ai/Prism2) | [代码](https://huggingface.co/paige-ai/Prism2) | 受限 |
| **TITAN** | 2025 | H&E 病理图像 | WSI + 病理报告/合成描述 | 768 | [论文](https://doi.org/10.1038/s41591-025-03982-3) | [权重/入口](https://huggingface.co/MahmoodLab/TITAN) | [代码](https://github.com/mahmoodlab/TITAN) | 受限 |
| **CHIEF** | 2024 | H&E 病理图像 | 病理图像（WSI） | 768 | [论文](https://doi.org/10.1038/s41586-024-07894-z) | [权重/入口](https://github.com/hms-dbmi/CHIEF) | [代码](https://github.com/hms-dbmi/CHIEF) | 仓库下载 |
| **MADELEINE** | 2024 | H&E（亦支持多染色） | H&E + IHC 等多染色 WSI | 512 | [论文](https://arxiv.org/abs/2408.02859) | [权重/入口](https://huggingface.co/MahmoodLab/madeleine) | [代码](https://github.com/mahmoodlab/MADELEINE) | 受限 |
| **PRISM** | 2024 | H&E 病理图像 | WSI + 报告文本 | 1280 | [论文](https://arxiv.org/abs/2405.10254) | [权重/入口](https://huggingface.co/paige-ai/Prism) | [代码](https://huggingface.co/paige-ai/Prism) | 受限 |
| **Prov-GigaPath (Slide)** | 2024 | H&E 病理图像 | 病理图像（WSI） | 768 | [论文](https://doi.org/10.1038/s41586-024-07441-w) | [权重/入口](https://huggingface.co/prov-gigapath/prov-gigapath) | [代码](https://github.com/prov-gigapath/prov-gigapath) | 受限 |
| **TANGLE** | 2024 | H&E 病理图像 | WSI + 基因表达（预训练） | 512 | [论文](https://arxiv.org/abs/2405.11618) | [权重/入口](https://github.com/mahmoodlab/TANGLE) | [代码](https://github.com/mahmoodlab/TANGLE) | 仓库下载 |

## 维度与上游依赖：常见错误

| 情况 | 需要注意 |
|---|---|
| **ResNet-50** | `torchvision` 原始 ResNet-50 的 GAP 特征通常为 **2048**；CLAM/Trident 使用的截断 ResNet50 可能为 **1024**，应以 `extract_features` 实际 shape 为准。 |
| **Virchow / Virchow2** | CLS **1280**；CLS 与 Patch mean 拼接 **2560**。Virchow2 还要正确处理 register tokens。 |
| **PRISM2** | 模型期望的上游是 **Virchow2-CLS 1280**，而不是 2560 维拼接；Slide 可返回不同任务头的 2560 / 3072 维向量。 |
| **CONCH v1 / v1.5 / CONCH-Z** | Trident 标准 Patch 特征分别是 **512 / 768 / 768**；CONCH-Z 的 **768** 维是经过图文投影和归一化的空间。 |
| **Phaet / Mascaret** | 官方 `model.encode()` 推荐 CLS 为 **1024 / 1536**；Mascaret 的 CLS+Patch mean 可形成 **3072** 维，但不是 `model.encode()` 默认结果。 |
| **Midnight-12k** | 特征抽取约定决定是原生 **1536** 还是 CLS+Patch mean **3072**。 |
| **H0-mini** | **768** 的 CLS 与 **1536** 的拼接特征不要混用。 |
| **TITAN / MADELEINE / GigaPath** | Slide embedding 和上游 Patch embedding 的维度不同；详见网页中的“上游依赖”字段。 |
| **FEATHER-24K** | 预训练的 ABMIL/MIL 编码器，不是 Patch encoder；512 代表常用中间 slide embedding，分类输出由 head / `num_classes` 决定。 |

## 如何选择一个模型？

- **经典 MIL / 生物标志物或基因突变预测**：以 UNI、UNI2-h、Phikon-v2、Virchow2、H-Optimus 系列等作为不同规模视觉特征基线；重要的是在相同数据划分、倍率、预处理下比较。
- **病理图文检索、文本引导选区、zero-shot 分类**：优先考虑 CONCH、CONCH-Z、PLIP、MUSK、KEEP；提取图文相似度时必须使用相应投影空间。
- **直接获得 slide-level 表征**：研究 TITAN、PRISM/PRISM2、Prov-GigaPath、CHIEF、MADELEINE；保留其上游 Patch 模型及坐标处理细节。
- **资源受限**：可以优先实测 H0-mini、Phikon、GigaPath-Flash、Kaiko 小型变体；特征维度不能直接替代参数量、显存或推理速度。
- **多染色任务**：优先查看 CONCH、Hibou、MADELEINE 的训练数据与模态支持，迁移至未见染色时需验证。

这些是**实验候选建议**，不是跨数据集的定量性能排名。报告对比结果时请固定 patient-level 划分、外部验证、MPP/放大倍率、Patch 采样、图像预处理和 MIL 聚合器，并检查预训练集合是否包含测试 WSI。

## 快速使用

无需安装依赖：双击 `index.html` 即可打开本地版目录。网页支持模型名搜索、Patch/WSI、开放状态、预训练模态及年份筛选，也可导出当前筛选结果为 CSV。GitHub 仓库首页自动展示这个 `README.md`；GitHub Pages 则展示 `index.html`。

```bash
# 新建空仓库后，在项目目录内运行（将 URL 替换为自己的 GitHub 仓库）
git init
git add .
git commit -m "Add pathology feature encoder atlas"
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/pathology-feature-encoder-atlas.git
git push -u origin main
```

需要网页地址：GitHub 仓库 → **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**。网页通常位于 `https://<YOUR_USERNAME>.github.io/pathology-feature-encoder-atlas/`。这只是 URL 格式示例，实际需启用 GitHub Pages。

## 更新条目

**唯一数据源**：`data/models.json`。更新后运行（仅需 Python 标准库）

```bash
python scripts/build_site.py
python scripts/validate.py
```

自动生成 `README.md` 与离线可用的 `index.html`。CSV 也由构建脚本更新。推荐通过 Issue 提交新模型，并包含：官方名称、论文、视觉输入、预训练模态、输出层定义/维度、模型权重、代码入口、许可及版本号。

## 数据质量与局限

- 模型卡随作者更新，权重链接可能变更或被 gate；**本目录没有测试实际下载权限、模型权重哈希或逐项运行推理**。
- 个别模型没有可确认的独立论文，例如 H-Optimus-0 目前使用官方模型卡；H-Optimus-1 链接对应会议摘要。已在对应行明确标注，不以其他论文冒充。
- 列表中的年份以相应论文/模型版本为主，部分“版本”晚于家族原始论文；同一家族不同版本不可直接视为同一权重。
- **不附带任何第三方模型权重**，请到原始发布页面检查许可证、商业使用、数据保密和临床适用性。
- 此导航聚焦可查证公开获取入口，不保证覆盖全部病理模型；未列入暂无明确官方可下载权重的模型。例如 THREADS 在 TRIDENT 中仍显示权重待发布。

## 参考与基础设施

- [Mahmood Lab TRIDENT](https://github.com/mahmoodlab/TRIDENT) — 多种 Patch 和 WSI 编码器的维度、输入倍率、上游依赖及权重入口；本目录重要交叉核对来源。
- [MIL-Lab](https://github.com/mahmoodlab/MIL-Lab) — MIL 编码器及 FEATHER 特征定义。
- [Patho-Bench](https://github.com/mahmoodlab/Patho-Bench) — 统一 WSI 表征评测及患者级聚合流程。
- [Pathology Foundation Models（独立社区目录）](https://github.com/georg-wolflein/pathology-foundation-models) — 可互补参考，细节以官方模型卡为准。

> Catalog compilation only. No affiliation with model authors; respect each original paper's and checkpoint's license. The directory is for research, not clinical use.

