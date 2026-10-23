#!/usr/bin/env python3
"""Build README.md and standalone index.html from data/models.json. No dependencies."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
models=json.loads((ROOT/'data/models.json').read_text(encoding='utf-8'))
order={'Patch':0, 'WSI':1}
models=sorted(models, key=lambda r:(order[r['level']], -r['year'], r['name'].casefold()))

def a(text,url):
    return f'[{text}]({url})' if url else '—'

def md_escape(x):
    return str(x).replace('|','\\|').replace('\n',' ').replace('\r',' ')

def row(m):
    paper=a(m['paper_kind'] if m['paper_kind']!='论文' else '论文',m['paper_url'])
    return '| '+' | '.join(map(md_escape, [f"**{m['name']}**",m['year'],m['inference_modality'],m['pretrain_modality'],m['feature_dim'],paper,a('权重/入口',m['weight_url']),a('代码',m['code_url']),m['weight_access']]))+' |'

n_patch=sum(m['level']=='Patch' for m in models)
n_wsi=len(models)-n_patch
intro=f'''# Pathology Feature Encoder Atlas

> A curated directory of pathology feature extractors and whole-slide representation models.  
> **病理特征提取器导航：论文、推理模态、预训练模态、特征维度、官方权重和代码。**

**资料核查日期：2026-10-23** · **收录：{len(models)} 个模型条目（Patch {n_patch} / WSI {n_wsi}）** · [打开可搜索网页](./index.html) · [下载 CSV](./data/models.csv) · [机器可读 JSON](./data/models.json)

## 为什么建立这个列表？

在 WSI 分类、MIL、基因突变预测、预后分析及病理图文任务中，`feature extractor` 的输出维度**不等同于**网络隐藏层宽度。也不能混淆 **Patch 特征** `(N_patches, D_patch)` 与 **WSI 特征** `(D_slide,)`。不同模型的 `CLS`、`pooler_output`、Patch 均值和图文投影层可以返回完全不同的维度。

本列表优先关联官方模型卡及官方代码仓库；**“受限”表示通常需要登录 Hugging Face、同意条款或提交访问申请，并不代表模型不可获取**；“仓库下载”则是官方仓库提供下载说明，未必有一个可长期访问的直链。权重仍受原作者许可证约束。该目录不是模型性能排行榜。

**如何理解模态**：`推理输入模态` 表示提取特征时需要的数据（例如 H&E 图像）；`预训练模态` 表示训练阶段曾使用的数据（例如 WSI+转录组、病理图像+文本）。后者不意味着模型在推理时必须提供所有模态。

## Patch-level / Tile-level 特征提取器

表中 `特征维度` 为推荐/列明的提取接口结果；具体 pooling 定义见本文件后半部分。

| 模型 | 年份 | 推理输入模态 | 预训练模态 | 特征维度 | 论文 | 权重 | 代码 | 访问方式 |
|---|---:|---|---|---:|---|---|---|---|
'''
intro+='\n'.join(row(m) for m in models if m['level']=='Patch')
intro+='''

## WSI-level / Slide-level 特征提取器

WSI 模型的输入通常是**预先提取的 Patch 向量及空间坐标**，而非直接读入整个 gigapixel 张量；其上游 Patch 编码器必须与预训练时使用的版本匹配。

| 模型 | 年份 | 推理输入模态 | 预训练模态 | 特征维度 | 论文 | 权重 | 代码 | 访问方式 |
|---|---:|---|---|---:|---|---|---|---|
'''
intro+='\n'.join(row(m) for m in models if m['level']=='WSI')
intro+='''

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
'''
(ROOT/'README.md').write_text(intro+'\n',encoding='utf-8')

import csv
with (ROOT/'data/models.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f, fieldnames=models[0].keys());w.writeheader();w.writerows(models)

TEMPLATE=r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark">
<meta name="description" content="病理特征提取器导航：模型论文、模态、embedding 维度、官方权重与 GitHub 实现。">
<title>Pathology Feature Encoder Atlas</title>
<style>
:root{--bg:#080d18;--panel:#101828;--panel2:#172238;--line:#2a3950;--text:#e7eefb;--muted:#9fb0c9;--accent:#71ccf3;--accent2:#93f0c0;--amber:#ffd292;--danger:#f9a5a5;--shadow:0 14px 50px #03081570}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(ellipse 900px 540px at 80% -12%,#1e3764 0%,transparent 74%),var(--bg);color:var(--text);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;line-height:1.65}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}button,select,input{font:inherit}button{cursor:pointer}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.wrap{max-width:1380px;margin:auto;padding:0 30px}.top{display:flex;align-items:center;justify-content:space-between;gap:16px;border-bottom:1px solid #ffffff14;padding:18px 0}.brand{font-weight:780;letter-spacing:-.4px;font-size:17px}.brand .glyph{display:inline-flex;align-items:center;justify-content:center;width:29px;height:29px;background:linear-gradient(135deg,var(--accent),#877dff);border-radius:9px;margin-right:10px;color:#071223}.topnav{display:flex;gap:20px;font-size:13px}.topnav a{color:#bdcfe9}.hero{padding:66px 0 38px;max-width:960px}.eyebrow{font-size:12px;letter-spacing:.12em;color:var(--accent2);text-transform:uppercase;font-weight:750}.hero h1{margin:11px 0 15px;font-size:clamp(33px,4.4vw,60px);line-height:1.14;letter-spacing:-1.7px}.grad{background:linear-gradient(100deg,#c6f1ff 5%,#73bbff 52%,#aea3ff);background-clip:text;color:transparent}.subtitle{max-width:820px;font-size:16px;color:var(--muted);margin:0}.stats{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}.stat{padding:12px 20px;border:1px solid var(--line);border-radius:12px;background:#ffffff06;min-width:139px}.stat strong{font-size:22px;font-weight:760;display:block;line-height:1.25}.stat span{color:var(--muted);font-size:12px}.notice{border:1px solid #3a5677;background:linear-gradient(100deg,#17304b66,#13213755);border-radius:14px;padding:15px 18px;color:#cfdeef;margin:15px 0 29px;font-size:13px}.notice strong{color:#e5f2ff}
.section-title{margin:40px 0 16px;font-size:24px;letter-spacing:-.4px}.section-title small{font-weight:450;color:var(--muted);font-size:13px;margin-left:12px}.filterbox{background:var(--panel);border:1px solid var(--line);padding:22px;border-radius:17px;box-shadow:var(--shadow)}.filters{display:grid;grid-template-columns:minmax(240px,2.2fr) repeat(3,minmax(140px,1fr)) minmax(130px,.85fr);gap:12px}.field label{color:var(--muted);display:block;font-size:12px;margin-bottom:7px}.field input,.field select{width:100%;height:42px;border:1px solid #384761;color:var(--text);background:#0b1424;border-radius:9px;padding:0 12px;outline:none}.field input::placeholder{color:#7c91ae}.toolrow{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:16px;flex-wrap:wrap}.meta{font-size:13px;color:var(--muted)}.btns{display:flex;gap:9px;flex-wrap:wrap}.btn{background:#1a2941;color:var(--text);border:1px solid #3f526e;border-radius:9px;padding:9px 13px;font-size:12px;font-weight:650;transition:background .2s}.btn:hover{background:#29415c}.btn.primary{border-color:#4a91b2;background:#113249;color:#aee4fc}.tablewrap{border:1px solid var(--line);border-radius:16px;overflow-x:auto;background:var(--panel);box-shadow:var(--shadow)}table{width:100%;border-collapse:collapse;min-width:1090px;font-size:12.5px;text-align:left}th{background:#19243a;font-size:11px;letter-spacing:.05em;color:#91a5c0;font-weight:700;white-space:nowrap;position:sticky;top:0;z-index:1}td,th{padding:15px 13px;border-bottom:1px solid #243248;vertical-align:top}tbody tr:hover{background:#182740}tr:last-child td{border-bottom:0}.name{font-size:14px;font-weight:730;color:#f1f7ff;white-space:nowrap}.small{font-size:11px;color:var(--muted);line-height:1.5}.dim{font-variant-numeric:tabular-nums;font-size:14px;font-weight:770;color:#b6e3ff}.pill{display:inline-flex;align-items:center;border-radius:999px;border:1px solid #355f4e;background:#112f28;padding:2px 10px;font-size:11px;font-weight:650;color:var(--accent2);white-space:nowrap}.pill.lock{color:var(--amber);background:#3c2b1b;border-color:#644e32}.pill.repo{color:#c6b8fc;background:#312a49;border-color:#4e4177}.links{display:flex;gap:10px;flex-wrap:wrap;white-space:nowrap}.links a{color:#9de1ff}.links a:hover{color:#fff}.empty{padding:42px;text-align:center;color:var(--muted)}.helpgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:15px 0}.help{border:1px solid var(--line);background:#0e1828;border-radius:14px;padding:19px}.help h3{font-size:15px;margin:0 0 9px}.help p{color:var(--muted);font-size:12.5px;margin:0}.help b{color:var(--text)}.footer{border-top:1px solid var(--line);color:#91a6c2;font-size:12px;margin:52px auto 0;padding:25px 0 55px;display:flex;gap:20px;justify-content:space-between;flex-wrap:wrap}.resource{display:flex;gap:14px;flex-wrap:wrap}.tiny{font-size:11px;color:#8da4be}.iconline{font-weight:730;color:#b9ccde}.badge-year{font-weight:700;color:#8ba4c9;font-size:12px}.level{padding:2px 8px;background:#1d3346;border:1px solid #31576e;color:#a8d8f0;border-radius:7px;font-size:11px}.level.wsi{color:#d0b9fa;background:#30243d;border-color:#5c457c}.highlight{background:#1e3e54;padding:1px 3px;border-radius:3px}
@media(max-width:1050px){.filters{grid-template-columns:repeat(3,1fr)}.filters .field:first-child{grid-column:span 3}.helpgrid{grid-template-columns:repeat(2,1fr)}}@media(max-width:680px){.wrap{padding:0 16px}.topnav{gap:12px}.topnav a:nth-child(2){display:none}.hero{padding:41px 0 18px}.hero h1{letter-spacing:-1px}.filters{grid-template-columns:repeat(2,1fr)}.filters .field:first-child{grid-column:span 2}.helpgrid{grid-template-columns:1fr}.filterbox{padding:15px}.stat{min-width:118px}.section-title small{display:block;margin-left:0}}
</style>
</head>
<body>
<div class="wrap">
  <header class="top"><div class="brand"><span class="glyph">↗</span>PATHOLOGY <span style="font-weight:450;color:#a8bbd1">ATLAS</span></div><nav class="topnav"><a href="#catalog">模型目录</a><a href="#guide">选型指南</a><a href="./README.md">README</a><a href="./data/models.json">JSON</a></nav></header>
  <section class="hero"><div class="eyebrow">An open research catalog · Updated 2026.10.23</div><h1>Choose your<br><span class="grad">pathology encoder.</span></h1><p class="subtitle">病理特征提取器导航：汇总官方论文、Patch / WSI 级别、推理与预训练模态、输出特征维度、权重下载入口、代码实现和使用要求。面向 MIL、病理分型、分子预测及 WSI 表征研究。</p><div class="stats"><div class="stat"><strong id="stat-all">—</strong><span>模型条目</span></div><div class="stat"><strong id="stat-patch">—</strong><span>Patch encoders</span></div><div class="stat"><strong id="stat-wsi">—</strong><span>Slide encoders</span></div><div class="stat"><strong id="stat-year">2016–2026</strong><span>论文/版本年份</span></div></div></section>
  <aside class="notice"><strong>重要：维度是特征接口定义。</strong> 例如 Virchow2 的单独 CLS 为 1280 维、CLS+patch 均值拼接为 2560 维；PRISM2 使用的是上游 Virchow2-CLS。页面的“预训练模态”不等于推理时必须提供的模态。<strong>受限</strong> 权重需同意使用条款或申请访问。</aside>
  <section id="catalog"><h2 class="section-title">Encoder directory <small>按名称、模态、年份与权重状态检索</small></h2><div class="filterbox"><div class="filters"><div class="field"><label for="query">搜索模型 / 模态 / 上游依赖</label><input id="query" type="search" placeholder="UNI, CONCH, transcriptomics, Virchow…" autocomplete="off" /></div><div class="field"><label for="level">特征级别</label><select id="level"><option value="">全部级别</option><option>Patch</option><option>WSI</option></select></div><div class="field"><label for="modality">预训练类型</label><select id="modality"><option value="">全部</option><option value="cross">跨模态（图文/多组学）</option><option value="vision">纯视觉预训练</option></select></div><div class="field"><label for="access">权重获取方式</label><select id="access"><option value="">全部</option><option>公开</option><option>受限</option><option>仓库下载</option></select></div><div class="field"><label for="sort">排序</label><select id="sort"><option value="recent">最新年份</option><option value="oldest">最早年份</option><option value="name">模型名称</option><option value="dim">维度从大到小</option></select></div></div><div class="toolrow"><div class="meta" id="found" role="status" aria-live="polite">正在读取模型清单…</div><div class="btns"><button class="btn" type="button" id="reset">重置筛选</button><button class="btn primary" type="button" id="download">导出筛选结果 CSV ↓</button></div></div></div>
  <h2 class="section-title">Model list <small id="table-sub">41 curated entries</small></h2>
  <div class="tablewrap"><table><thead><tr><th>模型 / 年份</th><th>级别</th><th>推理输入模态</th><th>预训练模态</th><th>输出维度<br>提取定义</th><th>权重权限</th><th>论文与代码</th><th>上游 / 输入规范</th></tr></thead><tbody id="rows"></tbody></table><div id="empty" class="empty" hidden>没有符合条件的模型，尝试放宽筛选条件。</div></div>
  </section>
  <section id="guide"><h2 class="section-title">Selection notes <small>选型提示与复现要点</small></h2><div class="helpgrid"><div class="help"><h3>01 · MIL / 分子标志物</h3><p>可比较 <b>UNI / UNI2-h、Virchow2、Phikon-v2、H-Optimus</b> 等视觉特征。训练/验证划分与 MIL 结构需保持一致。</p></div><div class="help"><h3>02 · 病理图文 / 零样本</h3><p>考虑 <b>CONCH、CONCH-Z、PLIP、MUSK、KEEP</b>。图文匹配需先核对投影层以及输出归一化。</p></div><div class="help"><h3>03 · WSI 直接表征</h3><p>考虑 <b>TITAN、PRISM2、GigaPath、MADELEINE</b>。需匹配预训练使用的 Patch 模型、倍率、坐标。</p></div><div class="help"><h3>04 · 资源与存储</h3><p>比较 <b>H0-mini、Phikon、GigaPath-Flash</b>。向量维度不能直接代表模型参数量或算力。</p></div><div class="help"><h3>05 · 多染色 / 多模态</h3><p>区分 <b>推理输入</b> 与 <b>预训练模态</b>。有图文或 RNA 监督的模型也可能仅需 H&E 推理。</p></div><div class="help"><h3>06 · 评估规范</h3><p>检查 <b>MPP、倍率、标准化、患者级分组、数据污染和许可证</b>。权重存在不代表可以商用或用于临床。</p></div></div></section>
  <footer class="footer"><div><div class="iconline">Pathology Feature Encoder Atlas</div><div class="tiny">A literature & checkpoint directory. No external model weights are redistributed.</div></div><div class="resource"><a href="https://github.com/mahmoodlab/TRIDENT" target="_blank" rel="noopener noreferrer">TRIDENT ↗</a><a href="https://github.com/mahmoodlab/MIL-Lab" target="_blank" rel="noopener noreferrer">MIL-Lab ↗</a><a href="./data/models.csv">完整 CSV ↗</a></div></footer>
</div>
<script id="atlas-data" type="application/json">__EMBEDDED_MODELS__</script>
<script>
'use strict';
const all=JSON.parse(document.getElementById('atlas-data').textContent);
const els={q:document.getElementById('query'),level:document.getElementById('level'),modality:document.getElementById('modality'),access:document.getElementById('access'),sort:document.getElementById('sort'),rows:document.getElementById('rows'),found:document.getElementById('found'),empty:document.getElementById('empty')};
const find=id=>document.getElementById(id);
find('stat-all').textContent=all.length;find('stat-patch').textContent=all.filter(x=>x.level==='Patch').length;find('stat-wsi').textContent=all.filter(x=>x.level==='WSI').length;
find('stat-year').textContent=Math.min(...all.map(x=>x.year))+'–'+Math.max(...all.map(x=>x.year));
const classify=x=>/文本|报告|基因|表达|RNA|转录组|图文|IHC.*H&E|H&E.*IHC/.test(x.pretrain_modality)?'cross':'vision';
const cell=(tag,text,cls)=>{const el=document.createElement(tag);if(cls)el.className=cls;el.textContent=String(text??'');return el;};
function link(label,url){const l=document.createElement('a');l.href=url;l.target='_blank';l.rel='noopener noreferrer';l.textContent=label;return l;}
function filtered(){const q=els.q.value.trim().toLocaleLowerCase(),lev=els.level.value,mod=els.modality.value,acc=els.access.value;let x=all.filter(m=>(!lev||m.level===lev)&&(!acc||m.weight_access===acc)&&(!mod||classify(m)===mod)&&(!q||[m.name,m.year,m.inference_modality,m.pretrain_modality,m.feature_dim,m.feature_definition,m.upstream,m.notes].join(' ').toLocaleLowerCase().includes(q)));const s=els.sort.value;x.sort((a,b)=>s==='oldest'?a.year-b.year||a.name.localeCompare(b.name):s==='name'?a.name.localeCompare(b.name):s==='dim'?parseInt(b.feature_dim)-parseInt(a.feature_dim):b.year-a.year||a.name.localeCompare(b.name));return x;}
function appendLinks(td,m){const links=cell('div','','links');links.append(link(m.paper_kind==='论文'?'论文 ↗':m.paper_kind+' ↗',m.paper_url));links.append(link('权重 ↗',m.weight_url));if(m.code_url)links.append(link('代码 ↗',m.code_url));td.append(links);}
function render(){const models=filtered();els.rows.replaceChildren();const frag=document.createDocumentFragment();for(const m of models){const tr=document.createElement('tr');tr.id=m.id;const n=document.createElement('td');n.append(cell('div',m.name,'name'),cell('div',m.year,'badge-year'));tr.append(n);let t=document.createElement('td');t.append(cell('span',m.level,'level'+(m.level==='WSI'?' wsi':'')));tr.append(t);tr.append(cell('td',m.inference_modality));tr.append(cell('td',m.pretrain_modality));t=document.createElement('td');t.append(cell('div',m.feature_dim,'dim'),cell('div',m.feature_definition,'small'));tr.append(t);t=document.createElement('td');t.append(cell('span',m.weight_access,'pill'+(m.weight_access==='受限'?' lock':m.weight_access==='仓库下载'?' repo':'')));tr.append(t);t=document.createElement('td');appendLinks(t,m);tr.append(t);t=document.createElement('td');t.append(cell('div',m.upstream==='—'?'—':'依赖：'+m.upstream,'small'),cell('div',m.recommended_input,'small'));if(m.notes)t.title=m.notes;tr.append(t);frag.append(tr)}els.rows.append(frag);els.found.textContent=`当前显示 ${models.length} / ${all.length} 项 · Patch ${models.filter(x=>x.level==='Patch').length} · WSI ${models.filter(x=>x.level==='WSI').length}`;find('table-sub').textContent=models.length+' curated entries';els.empty.hidden=models.length>0;return models;}
function csvQuote(x){let s=String(x??'');if(/[\n\r",]/.test(s))s='"'+s.replace(/"/g,'""')+'"';return s;}
find('download').addEventListener('click',()=>{const fields=['name','year','level','inference_modality','pretrain_modality','feature_dim','feature_definition','paper_url','weight_url','code_url','weight_access','upstream','recommended_input','notes','paper_kind'];const lines=[fields.join(',')].concat(filtered().map(x=>fields.map(k=>csvQuote(x[k])).join(',')));const blob=new Blob(['\ufeff'+lines.join('\r\n')],{type:'text/csv;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='pathology-encoder-atlas-filtered.csv';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1200)});
find('reset').addEventListener('click',()=>{els.q.value='';els.level.value='';els.modality.value='';els.access.value='';els.sort.value='recent';render()});for(const el of [els.q,els.level,els.modality,els.access,els.sort])el.addEventListener(el===els.q?'input':'change',render);render();
</script>
</body>
</html>
'''
raw=json.dumps(models,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
html=TEMPLATE.replace('__EMBEDDED_MODELS__',raw)
(ROOT/'index.html').write_text(html,encoding='utf-8')
print(f'Built README, standalone HTML and CSV for {len(models)} records')
