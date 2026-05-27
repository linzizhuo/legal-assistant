from abc import ABC, abstractmethod
import json
import numpy as np
import faiss
from pathlib import Path
from core.registry import Registry

class BaseVectorStore(ABC):
    """向量数据库抽象基类"""

    @abstractmethod
    def add(self, vectors: np.ndarray, metadatas: list[dict]) -> None:
        ...

    @abstractmethod
    def save(self, dir_path: str | Path) -> None:
        ...

    @abstractmethod
    def load(self, dir_path: str | Path):
        ...

    @abstractmethod
    def get_total_count(self) -> int:
        ...


class FAISSVectorStore(BaseVectorStore):
    """基于 FAISS 的本地向量存储"""

    def __init__(self, dim: int = 768):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.metadata: list[dict] = []

    def add(self, vectors: np.ndarray, metadatas: list[dict]) -> None:
        """添加向量和对应的元数据"""
        assert vectors.shape[1] == self.dim, f"维度不匹配: 期望 {self.dim}, 实际 {vectors.shape[1]}"
        assert vectors.shape[0] == len(metadatas), "向量数量与元数据数量不一致"

        self.index.add(vectors)
        self.metadata.extend(metadatas)

    def search(self, query_vector: np.ndarray, k: int = 10) -> list[dict]:
        """搜索 top-k 相似向量，返回 [{"score": ..., "metadata": ...}, ...]"""
        scores, indices = self.index.search(query_vector, k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append({
                "score": float(score),
                "metadata": self.metadata[idx],
            })
        return results

    def save(self, dir_path: str | Path) -> None:
        """保存 FAISS 索引和元数据到磁盘"""
        dir_path = Path(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(dir_path / "index.faiss"))

        with open(dir_path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def load(self, dir_path: str | Path):
        """从磁盘加载 FAISS 索引和元数据"""
        dir_path = Path(dir_path)

        self.index = faiss.read_index(str(dir_path / "index.faiss"))
        self.dim = self.index.d

        with open(dir_path / "metadata.json", "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        return self

    def get_total_count(self) -> int:
        return self.index.ntotal


vector_store_registry = Registry[BaseVectorStore]()