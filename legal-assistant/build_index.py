"""离线索引构建 — 运行一次即可"""
import tomllib
from pathlib import Path
from rag.embedder import embedder_registry
from dotenv import load_dotenv
from rag.vector_store import vector_store_registry
from rag.pipeline import build_index as _build
# 读取配置。
load_dotenv()
config_path = Path(__file__).parent / "config" / "config.toml"
def run():
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

    total = _build(embedder, store)
    store.save("data/index")
    print(f"索引构建完成，共 {total} 条")

if __name__ == "__main__":
    run()