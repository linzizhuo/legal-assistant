# Legal Assistant

法律智能助手 — 基于 RAG 的中文法律条文检索与问答系统。

## 项目简介

从公开数据源获取中国现行法律条文，经解析清洗后构建向量索引，实现法律条文的语义检索。上层基于 LangChain 搭建对话框架，支持通过 LLM 进行多轮法律问答。

## 技术栈

| 模块 | 技术 | 说明 |
|------|------|------|
| 数据采集 | GitHub API + `media.githubusercontent.com` | 绕过 Git LFS，逐文件下载 |
| 数据解析 | 正则表达式 + 续行合并 | 支持多种法律文本格式 |
| 嵌入模型 | `sentence-transformers` (`shibing624/text2vec-base-chinese`) | 本地运行，768 维，无需 API Key |
| 向量检索 | FAISS (`IndexFlatIP`) | 内积（余弦）相似度搜索，暴力全量比对 |
| 实现管理 | `Registry[T]` 注册器 + TOML 配置 | 新增实现只需改配置文件 |
| 对话框架 | LangChain 组件 + 自定义 LawChain | 可控的主流程，集成历史重写、检索增强、LLM 生成 |

## 项目状态

- ✅ **数据采集** — 177 部中国现行法律（txt 格式，一行一条，共解析 14,451 条法律条文）
- ✅ **文本解析** — 正则提取法律名、条款号、标题、正文，处理续行合并
- ✅ **嵌入模型** — 本地中文模型封装，支持通过注册器扩展
- ✅ **向量库** — FAISS 索引 + 元数据存储，支持持久化
- ✅ **检索管线** — build_index（离线构建）/ search（在线检索）分离
- ✅ **对话问答** — 基于 LangChain 组件 + ChatDeepSeek 的多轮法律问答，支持聊天历史和问题重写

## 目录结构

```
legal-assistant/
├── core/
│   └── registry.py       # 通用注册器（工厂模式）
├── rag/
│   ├── reader.py         # 文件读取接口
│   ├── parser.py         # 法律条文解析器
│   ├── embedder.py       # 嵌入模型（抽象 + 实现）
│   ├── vector_store.py   # 向量存储（抽象 + 实现）
│   └── pipeline.py       # 索引构建与检索管线
├── agent/
│   ├── retriever.py      # LangChain 检索器（包装现有检索）
│   ├── chain.py          # 自定义 LawChain：重写 + 检索 + 生成 + 记忆
│   └── cli.py            # CLI 交互式法律问答入口
├── models/
│   └── law.py            # 法律条文数据结构
├── config/
│   └── config.toml       # 配置文件（注册映射 + 参数）
├── tools/
│   ├── download_laws.py  # 法律条文下载工具
│   └── test_parser.py    # 解析测试脚本
├── data/
│   ├── raw/              # 177 部法律条文（未跟踪）
│   └── index/            # 构建后 FAISS 索引 + 元数据（未跟踪）
├── build_index.py        # 离线索引构建脚本
├── main.py               # 在线搜索入口
├── pyproject.toml        # 项目配置（uv）
└── README.md
```

## 快速开始

```bash
cd legal-assistant

# 安装依赖
uv sync

# 如果连接 HuggingFace 超时，先设置国内镜像源：
# export HF_ENDPOINT=https://hf-mirror.com

# 离线构建语义索引（首次运行会自动下载约 500MB 嵌入模型）
uv run python build_index.py

# 搜索法律条文
uv run python main.py "遗赠扶养协议有什么效力"

# 多轮法律问答（需配置 LLM API Key）
export DEEPSEEK_API_KEY=sk-xxx
export LLM_MODEL=deepseek-chat
uv run python agent/cli.py

# 测试解析
uv run python tools/test_parser.py
```

> **注意**：`agent/cli.py` 为交互式对话，输入问题后回车等待回答，输入 `exit` 退出。

## 已知问题

- **法律覆盖不完整**：目前收录 177 部（截至 2025 年底中国现行有效法律共 308 部），缺少刑法等基础法律，后续需补充
- **宪法解析率偏低**：因包含目录、序言、章节标题等非条文内容，行级别匹配率约 50%，实际 138 条宪法条文均已正确解析
- **暴力搜索**：当前使用 FAISS `IndexFlatIP` 进行全量暴力比对，精度最高但随数据量增大会越来越慢，后续可切换 `IndexIVFFlat` 等压缩索引
- **全量内存加载**：所有法律条文的向量和元数据均加载到内存，当前规模（约 2 万条）无压力，若扩展到数十万条以上需引入外部存储
