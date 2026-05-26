# Legal Assistant

法律智能助手项目。

## 目录结构

```
legal-assistant/
├── legal-assistant/           # 项目主目录
│   ├── backend/               # 后端服务（FastAPI）
│   │   ├── app/
│   │   │   ├── main.py        # FastAPI 入口
│   │   │   ├── rag/           # 检索、重排序、向量库
│   │   │   ├── agent/         # Agent + LLM 调用
│   │   │   └── models/        # Pydantic 模型
│   │   ├── pyproject.toml     # Python 项目配置（uv）
│   │   ├── .python-version   # Python 版本锁定（3.12）
│   │   └── requirements.txt
│   ├── frontend/              # 前端应用
│   │   ├── src/
│   │   │   ├── views/         # 页面
│   │   │   ├── components/    # 组件
│   │   │   └── api/           # API 调用
│   │   └── package.json
│   └── README.md
└── tools/                     # 开发、调试、部署等相关工具脚本
```

## 开发

详见 [legal-assistant/](legal-assistant/) 下的说明。
