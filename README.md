# Legal Assistant

法律智能助手项目 — 基于 RAG 的中文法律条文检索系统。

## 项目状态

- ✅ **数据采集**：已从 `taburise/Chinese-Laws-folk` 下载 **177 部**中国现行法律条文
- 🔄 **RAG 流水线**：开发中（解析 → 向量化 → FAISS 检索）

## 目录结构

```
legal-assistant/
├── agent/              # Agent + LLM 调用
├── rag/                # 检索、重排序、向量库
├── models/             # Pydantic 模型
├── data/
│   └── raw/            # 177 部法律条文（.txt）
├── tools/
│   └── download_laws.py # 法律条文批量下载工具
├── main.py             # 入口
├── pyproject.toml      # 项目配置（uv）
└── .env                # 环境变量
```

## 快速开始

```bash
cd legal-assistant

# 安装依赖
uv sync

# 运行
uv run python main.py
```

## 法律条文下载

```bash
python tools/download_laws.py
```

从 `taburise/Chinese-Laws-folk` 逐文件下载 177 部法律，格式为 `《法律名》第X条规定，...`，每条独立成行。
