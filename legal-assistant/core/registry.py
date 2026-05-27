""" 注册表 """
import importlib # 字符串转类对象
from typing import TypeVar, Generic, Type

T = TypeVar("T")

class Registry(Generic[T]):
    def __init__(self):
        self._mapping: dict[str, Type[T]] = {}
    def register(self, name: str, cls: Type[T]) -> None:
        self._mapping[name] = cls
        
    def register_from_config(self, config: dict[str, str]) -> None:
        """从 {别名: 全限定类名} 的配置加载注册表"""
        for name, fqcn in config.items():
            mod_path, cls_name = fqcn.rsplit(".", 1)
            cls = getattr(importlib.import_module(mod_path), cls_name)
            self._mapping[name] = cls    
    
    def create(self, name: str, **kwargs) -> T:
        cls = self._mapping.get(name)
        if cls is None:
            raise KeyError(f"未注册: {name}")
        return cls(**kwargs)