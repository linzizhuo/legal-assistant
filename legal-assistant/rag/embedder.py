from abc import ABC, abstractmethod
from typing import Optional
import numpy as np


class BaseEmbedder(ABC):
    """嵌入模型抽象基类"""

    @abstractmethod
    def encode(self, texts: list[str]) -> np.ndarray:
        """将文本列表转换为向量，返回 shape=(n, dim) 的 float32 数组"""
        ...

    @abstractmethod
    def get_dimension(self) -> int:
        """返回向量维度"""
        ...


class SentenceTransformerEmbedder(BaseEmbedder):
    """基于 sentence-transformers 的本地中文嵌入模型"""

    def __init__(self, model_name: str = "shibing624/text2vec-base-chinese"):
        self._model_name = model_name
        self._model = None

    def _load_model(self):
        """惰性加载模型"""
        if self._model is not None:
            return
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(self._model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        """编码文本列表，返回 L2 归一化的向量数组"""
        self._load_model()
        embeddings = self._model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        return embeddings.astype(np.float32)

    def get_dimension(self) -> int:
        self._load_model()
        return self._model.get_sentence_embedding_dimension()
