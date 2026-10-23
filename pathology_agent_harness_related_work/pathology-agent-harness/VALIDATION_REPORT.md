# 交付前验证记录

日期：2026-09-17。

## 实际执行的检查

下载助手的 10 项离线单元测试全部通过：PDF 头/结束标记、HTML 失败响应、路径穿越、
链接条目拒绝、正规 tar 解包、单文件 TeX、注释处理、verbatim 保留、inline verb 保留、旧稿隔离与原文保留。
测试使用临时目录和合成字节，不包含论文下载、病理推理或 LLM 调用。

项目结构检查通过：六篇笔记和版本元数据齐全；文内相对 Markdown 链接可定位；没有未填写模板占位符。
BibTeX 收录六篇论文与两篇工程资料；预印本和工程资料类型已分开。

## 本次不能验证的内容

网络下载没有成功端到端运行；远程端点未来可用性无法由离线测试保证。
六篇原 PDF 与六份 LaTeX 均未在本地归档，检查器会如实列出。
全部论文/模型 baseline 状态 NOT_RUN；没有临床数据、性能、显存或 API 成本实测。

## 下载助手限制

PDF 检查为文件格式基础校验，不是完整渲染验证。源码清理不是完整 TeX 解析器，可能保留一些注释，
也不保证编译语义不变；原始压缩包及 `.orig` 应保留，用来核对正式引用。
作者解包文件放到 `source/upstream/`，避免覆盖本地状态 README。
下载到第三方论文/源码后仍应遵守其许可，不能因工具成功下载就假定可再分发。

## 检查器输出

```json
{
  "status": "PASS",
  "paper_count": 6,
  "missing_local_pdfs": [
    "react",
    "pathlab",
    "acp_bench",
    "pathnavigate",
    "pathpocket",
    "ahe"
  ],
  "missing_local_latex": [
    "react",
    "pathlab",
    "acp_bench",
    "pathnavigate",
    "pathpocket",
    "ahe"
  ],
  "meaning": "PASS is structure validation, not completed downloads or scientific experiments.",
  "errors": []
}
```
