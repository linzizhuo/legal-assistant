"""离线索引构建 — 运行一次即可"""
import tomllib
from pathlib import Path
from rag.embedder import embedder_registry
from dotenv import load_dotenv
from rag.vector_store import vector_store_registry
from rag.pipeline import index_all_laws as _index_all_laws
# 读取配置。
load_dotenv()
ROOT = Path(__file__).parent
# 保证绝对路径。
config_path = ROOT / "config" / "config.toml"
index_path = ROOT / "data" / "index"

def build_law_index():
    with open(config_path, "rb") as f:
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

    total = _index_all_laws(embedder, store)
    store.save(index_path)
    print(f"索引构建完成，共 {total} 条")

if __name__ == "__main__":
    build_law_index()