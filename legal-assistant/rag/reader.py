# 读写文件的接口
from pathlib import Path

def scan_files(data_dir: str = "data/raw") -> list[Path]:
    """扫描目录下所有 .txt 文件，返回排序后的路径列表"""
    root = Path(__file__).resolve().parent.parent
    target = root / data_dir
    # 扫描所有 .txt 文件并按文件名排序
    return sorted(target.rglob("*.txt"))

def read_lines(file_path: Path) -> list[str]:
    """读取单个文件，返回非空行列表（去掉空行和首尾空白）"""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 去掉每行首尾空白，过滤掉空行
    return [line.strip() for line in lines if line.strip()]

def iter_all_files(data_dir: str = "data/raw"):
    """生成器，逐个 yield (file_path, lines)，适合大目录"""
    # TODO: 后续实现
    raise NotImplementedError