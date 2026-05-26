# Legal Assistant

法律智能助手项目。

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
├── .python-version
└── .env                # 环境变量
```

## 数据

已下载 **177 部**中国现行法律，涵盖：

- 宪法、民法典、刑法、各类诉讼法
- 民商法、经济法、行政法、社会法
- 网络安全法、数据安全法等新兴领域法律

每条格式：`《中华人民共和国民法典》第八条规定，民事主体从事民事活动，不得违反法律，不得违背公序良俗。`

## 开发

```bash
# 同步依赖
uv sync

# 运行
uv run python main.py

# 更新法律条文数据
python tools/download_laws.py
```
