# Legal Assistant

法律智能助手项目。

## 目录结构

```
legal-assistant/
├── backend/                   # 后端服务（FastAPI）
│   ├── app/
│   │   ├── main.py            # FastAPI 入口
│   │   ├── rag/               # 检索、重排序、向量库
│   │   ├── agent/             # Agent + LLM 调用
│   │   └── models/            # Pydantic 模型
│   ├── pyproject.toml         # Python 项目配置（uv）
│   ├── .python-version        # Python 版本锁定（3.12）
│   └── requirements.txt
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── views/             # 页面
│   │   ├── components/        # 组件
│   │   └── api/               # API 调用
│   └── package.json
└── README.md
```

## 开发

### 后端

使用 [uv](https://docs.astral.sh/uv/) 管理 Python 依赖和虚拟环境。

```bash
cd backend

# 同步依赖并创建虚拟环境
uv sync

# 添加新依赖
uv add <package-name>

# 启动开发服务器
uv run uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
```
