# Legal Assistant

法律智能助手 — 基于 RAG 的中文法律条文检索系统。

## 项目简介

从公开数据源获取中国现行法律条文，经解析清洗后构建向量索引，实现法律条文的语义检索。

## 技术栈

| 模块 | 技术 | 说明 |
|------|------|------|
| 数据采集 | GitHub API + `media.githubusercontent.com` | 绕过 Git LFS，逐文件下载 |
| 数据解析 | 正则表达式 + 续行合并 | 支持多种法律文本格式 |
| 嵌入模型 | `sentence-transformers` (`shibing624/text2vec-base-chinese`) | 本地运行，768 维，无需 API Key |
| 向量检索 | FAISS (`IndexFlatIP`) | 余弦相似度搜索，毫秒级响应 |
| 抽象设计 | 接口类 (`BaseEmbedder` / `BaseVectorStore`) | 方便扩展不同模型和向量库 |

## 项目状态

- ✅ **数据采集** — 177 部中国现行法律（txt 格式，一行一条）
- ✅ **文本解析** — 正则提取法律名、条款号、标题、正文，处理续行合并
- ✅ **嵌入模型** — 本地中文模型封装
- ✅ **向量库** — FAISS 索引 + 元数据存储
- 🔄 **检索流程** — 开发中

## 目录结构

```
legal-assistant/
├── rag/
│   ├── reader.py        # 文件读取接口
│   ├── parser.py        # 法律条文解析器
│   ├── embedder.py      # 嵌入模型（抽象 + 实现）
│   └── vector_store.py  # 向量存储（抽象 + 实现）
├── models/
│   └── law.py           # 法律条文数据结构
├── tools/
│   ├── download_laws.py # 法律条文下载工具
│   └── test_parser.py   # 解析测试脚本
├── data/
│   └── raw/             # 177 部法律条文（未跟踪）
├── main.py              # 入口
├── pyproject.toml        # 项目配置（uv）
└── README.md
```

## 快速开始

```bash
cd legal-assistant

# 安装依赖
uv sync

# 测试解析
uv run python tools/test_parser.py
```

## 已知问题

- **法律覆盖不完整**：目前收录 177 部（截至 2025 年底中国现行有效法律共 308 部），缺少刑法等基础法律，后续需补充
- **宪法解析率偏低**：因包含目录、序言、章节标题等非条文内容，行级别匹配率约 50%，实际 138 条宪法条文均已正确解析
