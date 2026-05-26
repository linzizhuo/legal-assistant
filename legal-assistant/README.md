# Legal Assistant

法律智能助手项目。

## 目录结构

```
legal-assistant/
├── agent/         # Agent + LLM 调用
├── rag/           # 检索、重排序、向量库
├── models/        # Pydantic 模型
├── data/          # 法律条文原始文件
├── main.py        # 入口
├── pyproject.toml  # Python 项目配置（uv）
├── .python-version
└── .env           # 环境变量
```

## 开发

```bash
# 同步依赖
uv sync

# 运行
uv run python main.py
```
