"""LangChain 检索器 — 包装现有关联检索为 LangChain BaseRetriever"""

from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from rag.embedder import BaseEmbedder
from rag.vector_store import BaseVectorStore


class LawRetriever(BaseRetriever):
    """将现有的 find_articles 包装为 LangChain 检索器"""
    embedder: BaseEmbedder
    store: BaseVectorStore
    k: int = 10

    def _get_relevant_documents(self, query: str) -> list[Document]:
        query_vec = self.embedder.encode([query])
        results = self.store.search(query_vec, k=self.k)
        return [
            Document(
                page_content=r["metadata"]["content"],
                metadata={
                    "law_name": r["metadata"]["law_name"],
                    "article_number": r["metadata"]["article_number"],
                    "score": r["score"],
                },
            )
            for r in results
        ]
