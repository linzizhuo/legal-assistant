# Legal Assistant

法律智能助手项目 — 基于语义检索的中国法律条文搜索引擎。

## 目录结构

```
legal-assistant/
├── core/
│   ├── registry.py       # 通用注册器（工厂模式）
│   └── __init__.py
├── rag/
│   ├── reader.py         # 文件读取接口
│   ├── parser.py         # 法律条文解析器
│   ├── embedder.py       # 嵌入模型（抽象 + 实现）
│   ├── vector_store.py   # 向量存储（抽象 + 实现）
│   └── pipeline.py       # 索引构建与检索管线
├── models/
│   └── law.py            # LegalArticle Pydantic model
├── config/
│   └── config.toml       # 配置文件（注册映射 + 参数）
├── tools/
│   ├── download_laws.py  # 法律条文下载工具
│   └── test_parser.py    # 解析测试脚本
├── data/
│   ├── raw/              # 177 部法律条文（原始文本）
│   └── index/            # 构建后 FAISS 索引 + 元数据
├── build_index.py        # 离线索引构建脚本
├── main.py               # 在线入口
├── pyproject.toml        # 项目配置（uv）
├── .python-version
└── .env                  # 环境变量
```

## 数据

已下载 **177 部**中国现行法律，涵盖宪法、民法典、诉讼法、民商法、经济法、行政法、社会法、网络安全法等，共 **14,451 条**法律条文。

每条格式：`《中华人民共和国民法典》第八条规定，民事主体从事民事活动，不得违反法律，不得违背公序良俗。`

## 使用

```bash
# 同步依赖
uv sync

# 如果连接 HuggingFace 超时，先设置国内镜像源：
export HF_ENDPOINT=https://hf-mirror.com

# 离线构建语义索引（首次需下载约 500MB 嵌入模型）
uv run python build_index.py

# 搜索法律条文
uv run python main.py "遗赠扶养协议有什么效力"

# 测试解析
uv run python tools/test_parser.py

# 更新法律条文数据
uv run python tools/download_laws.py
```

## 设计

- **分层抽象**：`BaseEmbedder` / `BaseVectorStore` 接口类方便切换不同实现
- **注册器模式**：通过 `Registry[T]` + TOML 配置文件管理具体实现类，新增实现只需改配置
- **惰性加载**：嵌入模型首次使用时加载，避免无谓内存占用
- **续行合并**：跨行法律条文自动合并
- **格式兼容**：同时支持 `《法律名》第X条` 标准格式和 `第X条` 宪法格式
 