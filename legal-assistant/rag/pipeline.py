"""检索管线 — 只依赖抽象"""

from pathlib import Path
from rag.reader import scan_files, read_lines
from rag.parser import extract_articles
from rag.embedder import BaseEmbedder
from rag.vector_store import BaseVectorStore


def index_all_laws(
    embedder: BaseEmbedder,
    store: BaseVectorStore,
    data_dir: str = "data/raw",
) -> int:
    """读取全部法律文件，逐条解析、生成向量，存入向量库"""
    files = scan_files(data_dir)

    all_articles = []
    for file_path in files:
        lines = read_lines(file_path)
        articles = extract_articles(lines, source_file=str(file_path))
        all_articles.extend(articles)

    texts = [a.content for a in all_articles]
    vectors = embedder.encode(texts)

    metadatas = [
        {
            "law_name": a.law_name,
            "article_number": a.article_number,
            "article_title": a.article_title,
            "content": a.content,
        }
        for a in all_articles
    ]

    store.add(vectors, metadatas)
    return store.get_total_count()


def find_articles(
    query: str,
    embedder: BaseEmbedder,
    store: BaseVectorStore,
    k: int = 10,
) -> list[dict]:
    """检索与查询最相关的法律条文"""
    query_vec = embedder.encode([query])
    return store.search(query_vec, k=k)