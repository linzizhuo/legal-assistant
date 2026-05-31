"""CLI 交互式法律问答 — 加载索引 → 构建对话链 → 一问一答"""

import os
from dotenv import load_dotenv
load_dotenv()
import tomllib
from pathlib import Path


ROOT = Path(__file__).parent.parent

from agent.chain import build_chain
from agent.retriever import LawRetriever
from rag.embedder import embedder_registry
from rag.vector_store import vector_store_registry


def _load_retriever(k: int = 10) -> LawRetriever:
    """从配置文件 + 已构建的索引构建检索器"""
    with open(ROOT / "config" / "config.toml", "rb") as f:
        config = tomllib.load(f)

    embedder_registry.register_from_config(config["embedder"]["registry"])
    vector_store_registry.register_from_config(config["vector_store"]["registry"])

    embedder = embedder_registry.create(
        config["embedder"]["type"],
        model_name=config["embedder"]["model_name"],
    )
    store = vector_store_registry.create(
        config["vector_store"]["type"],
        dim=config["vector_store"]["dim"],
    )
    store.load(ROOT / "data" / "index")
    return LawRetriever(embedder=embedder, store=store, k=k)


def main():
    load_dotenv()

    print("法律智能助手 — 输入问题开始对话（输入 exit 退出）")
    print("-" * 50)

    retriever = _load_retriever(k=10)
    chain = build_chain(retriever)

    while True:
        question = input("\n您的问题: ").strip()
        if question.lower() in ("exit", "quit", "退出"):
            break
        if not question:
            continue

        answer = chain.ask(question)
        print(f"\n回答: {answer}")


if __name__ == "__main__":
    main()
