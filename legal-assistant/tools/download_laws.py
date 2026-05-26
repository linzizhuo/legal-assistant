"""
批量下载 taburise/Chinese-Laws-folk 的法律条文（跳过 git clone）

下载链接格式:
  https://media.githubusercontent.com/media/taburise/Chinese-Laws-folk/refs/heads/main/{文件名}?download=true

用法:
    python tools/download_laws.py
"""

import os
import time
import urllib.request
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

REPO_OWNER = "taburise"
REPO_NAME = "Chinese-Laws-folk"
BRANCH = "main"
BASE_URL = f"https://media.githubusercontent.com/media/{REPO_OWNER}/{REPO_NAME}/refs/heads/{BRANCH}/"

# 177 个法律文件列表（从 GitHub API 获取并缓存）
LAW_FILES = [
    "中华人民共和国反家庭暴力法.txt",
    "中华人民共和国反恐怖主义法.txt",
    "中华人民共和国反有组织犯罪法.txt",
    "中华人民共和国反洗钱法.txt",
    "中华人民共和国反电信网络诈骗法.txt",
    "中华人民共和国反间谍法.txt",
    "中华人民共和国反食品浪费法.txt",
    "中华人民共和国可再生能源法.txt",
    "中华人民共和国合伙企业法.txt",
    "中华人民共和国商业银行法.txt",
    "中华人民共和国商标法.txt",
    "中华人民共和国噪声污染防治法.txt",
    "中华人民共和国固体废物污染环境防治法.txt",
    "中华人民共和国国境卫生检疫法.txt",
    "中华人民共和国国家情报法.txt",
    "中华人民共和国国家通用语言文字法.txt",
    "中华人民共和国国防交通法.txt",
    "中华人民共和国国防动员法.txt",
    "中华人民共和国国防教育法.txt",
    "中华人民共和国国际刑事司法协助法.txt",
    "中华人民共和国土地管理法.txt",
    "中华人民共和国土壤污染防治法.txt",
    "中华人民共和国城乡规划法.txt",
    "中华人民共和国城市房地产管理法.txt",
    "中华人民共和国城市维护建设税法.txt",
    "中华人民共和国基本医疗卫生与健康促进法.txt",
    "中华人民共和国境外非政府组织境内活动管理法.txt",
    "中华人民共和国增值税法.txt",
    "中华人民共和国外商投资法.txt",
    "中华人民共和国大气污染防治法.txt",
    "中华人民共和国契税法.txt",
    "中华人民共和国妇女权益保障法.txt",
    "中华人民共和国学位法.txt",
    "中华人民共和国安全生产法.txt",
    "中华人民共和国审计法.txt",
    "中华人民共和国宪法.txt",
    "中华人民共和国家庭教育促进法.txt",
    "中华人民共和国密码法.txt",
    "中华人民共和国对外贸易法.txt",
    "中华人民共和国就业促进法.txt",
    "中华人民共和国居民身份证法.txt",
    "中华人民共和国工会法.txt",
    "中华人民共和国广告法.txt",
    "中华人民共和国建筑法.txt",
    "中华人民共和国引渡法.txt",
    "中华人民共和国律师法.txt",
    "中华人民共和国循环经济促进法.txt",
    "中华人民共和国慈善法.txt",
    "中华人民共和国护照法.txt",
    "中华人民共和国拍卖法.txt",
    "中华人民共和国招标投标法.txt",
    "中华人民共和国放射性污染防治法.txt",
    "中华人民共和国政府采购法.txt",
    "中华人民共和国教师法.txt",
    "中华人民共和国教育法.txt",
    "中华人民共和国数据安全法.txt",
    "中华人民共和国文物保护法.txt",
    "中华人民共和国旅游法.txt",
    "中华人民共和国无障碍环境建设法.txt",
    "中华人民共和国期货和衍生品法.txt",
    "中华人民共和国未成年人保护法.txt",
    "中华人民共和国枪支管理法.txt",
    "中华人民共和国标准化法.txt",
    "中华人民共和国核安全法.txt",
    "中华人民共和国档案法.txt",
    "中华人民共和国森林法.txt",
    "中华人民共和国残疾人保障法.txt",
    "中华人民共和国母婴保健法.txt",
    "中华人民共和国民事诉讼法.txt",
    "中华人民共和国民办教育促进法.txt",
    "中华人民共和国民法典.txt",
    "中华人民共和国民用航空法.txt",
    "中华人民共和国气象法.txt",
    "中华人民共和国水土保持法.txt",
    "中华人民共和国水污染防治法.txt",
    "中华人民共和国水法.txt",
    "中华人民共和国治安管理处罚法.txt",
    "中华人民共和国法律援助法.txt",
    "中华人民共和国注册会计师法.txt",
    "中华人民共和国测绘法.txt",
    "中华人民共和国海上交通安全法.txt",
    "中华人民共和国海事诉讼特别程序法.txt",
    "中华人民共和国海关法.txt",
    "中华人民共和国海南自由贸易港法.txt",
    "中华人民共和国海商法.txt",
    "中华人民共和国海域使用管理法.txt",
    "中华人民共和国海岛保护法.txt",
    "中华人民共和国海洋环境保护法.txt",
    "中华人民共和国海警法.txt",
    "中华人民共和国消费者权益保护法.txt",
    "中华人民共和国消防救援衔条例.txt",
    "中华人民共和国消防法.txt",
    "中华人民共和国涉外民事关系法律适用法.txt",
    "中华人民共和国深海海底区域资源勘探开发法.txt",
    "中华人民共和国清洁生产促进法.txt",
    "中华人民共和国渔业法.txt",
    "中华人民共和国港口法.txt",
    "中华人民共和国湿地保护法.txt",
    "中华人民共和国烟叶税法.txt",
    "中华人民共和国烟草专卖法.txt",
    "中华人民共和国煤炭法.txt",
    "中华人民共和国特种设备安全法.txt",
    "中华人民共和国献血法.txt",
    "中华人民共和国环境保护法.txt",
    "中华人民共和国环境保护税法.txt",
    "中华人民共和国环境影响评价法.txt",
    "中华人民共和国现役军官法.txt",
    "中华人民共和国生物安全法.txt",
    "中华人民共和国电力法.txt",
    "中华人民共和国电子商务法.txt",
    "中华人民共和国电子签名法.txt",
    "中华人民共和国电影产业促进法.txt",
    "中华人民共和国畜牧法.txt",
    "中华人民共和国疫苗管理法.txt",
    "中华人民共和国监狱法.txt",
    "中华人民共和国石油天然气管道保护法.txt",
    "中华人民共和国矿产资源法.txt",
    "中华人民共和国矿山安全法.txt",
    "中华人民共和国社会保险法.txt",
    "中华人民共和国社区矫正法.txt",
    "中华人民共和国票据法.txt",
    "中华人民共和国禁毒法.txt",
    "中华人民共和国种子法.txt",
    "中华人民共和国科学技术普及法.txt",
    "中华人民共和国科学技术进步法.txt",
    "中华人民共和国税收征收管理法.txt",
    "中华人民共和国突发事件应对法.txt",
    "中华人民共和国粮食安全保障法.txt",
    "中华人民共和国精神卫生法.txt",
    "中华人民共和国红十字会法.txt",
    "中华人民共和国统计法.txt",
    "中华人民共和国网络安全法.txt",
    "中华人民共和国老年人权益保障法.txt",
    "中华人民共和国耕地占用税法.txt",
    "中华人民共和国职业教育法.txt",
    "中华人民共和国职业病防治法.txt",
    "中华人民共和国能源法.txt",
    "中华人民共和国航道法.txt",
    "中华人民共和国船舶吨税法.txt",
    "中华人民共和国节约能源法.txt",
    "中华人民共和国草原法.txt",
    "中华人民共和国药品管理法.txt",
    "中华人民共和国著作权法.txt",
    "中华人民共和国行政处罚法.txt",
    "中华人民共和国行政复议法.txt",
    "中华人民共和国行政强制法.txt",
    "中华人民共和国行政许可法.txt",
    "中华人民共和国行政诉讼法.txt",
    "中华人民共和国计量法.txt",
    "中华人民共和国证券投资基金法.txt",
    "中华人民共和国证券法.txt",
    "中华人民共和国资产评估法.txt",
    "中华人民共和国资源税法.txt",
    "中华人民共和国车船税法.txt",
    "中华人民共和国车辆购置税法.txt",
    "中华人民共和国进出口商品检验法.txt",
    "中华人民共和国进出境动植物检疫法.txt",
    "中华人民共和国退役军人保障法.txt",
    "中华人民共和国道路交通安全法.txt",
    "中华人民共和国邮政法.txt",
    "中华人民共和国野生动物保护法.txt",
    "中华人民共和国铁路法.txt",
    "中华人民共和国银行业监督管理法.txt",
    "中华人民共和国长江保护法.txt",
    "中华人民共和国防沙治沙法.txt",
    "中华人民共和国防洪法.txt",
    "中华人民共和国防震减灾法.txt",
    "中华人民共和国青藏高原生态保护法.txt",
    "中华人民共和国非物质文化遗产法.txt",
    "中华人民共和国预备役人员法.txt",
    "中华人民共和国预算法.txt",
    "中华人民共和国预防未成年人犯罪法.txt",
    "中华人民共和国食品安全法.txt",
    "中华人民共和国驻外外交人员法.txt",
    "中华人民共和国高等教育法.txt",
    "中华人民共和国黄河保护法.txt",
    "中华人民共和国黑土地保护法.txt",
]


def download_file(filename: str, target_path: Path) -> bool:
    """通过 media.githubusercontent.com 下载单个文件"""
    from urllib.parse import quote
    url = BASE_URL + quote(filename) + "?download=true"

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Python",
            })
            resp = urllib.request.urlopen(req, timeout=60)
            content = resp.read()
            if len(content) < 50:
                # 太短可能是 LFS 指针文件，重试
                print(f"    文件过小 ({len(content)} bytes)，可能有问题，但已保存")
            target_path.write_bytes(content)
            return True
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            print(f"    下载失败: {e}")
            return False
    return False


def try_update_file_list() -> list[str] | None:
    """尝试从 GitHub API 获取最新文件列表，失败则返回 None"""
    try:
        url = "https://api.github.com/repos/taburise/Chinese-Laws-folk/contents/"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Python",
            "Accept": "application/vnd.github+json",
        })
        resp = urllib.request.urlopen(req, timeout=10)
        files = json.loads(resp.read())
        txt_files = sorted([
            f["name"] for f in files
            if isinstance(f, dict) and f["name"].endswith(".txt")
        ])
        if txt_files:
            print(f"  API 获取到 {len(txt_files)} 个文件")
            return txt_files
    except Exception:
        pass
    return None


def main():
    print("=" * 60)
    print("法律条文批量下载工具")
    print(f"数据源: {REPO_OWNER}/{REPO_NAME}")
    print(f"保存到: {DATA_DIR}")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 获取文件列表（优先 API，失败用缓存的）
    print("\n📋 获取文件列表...")
    files = try_update_file_list()
    if files is None:
        files = LAW_FILES
        print(f"  使用内置列表（{len(files)} 个文件）")
    else:
        print(f"  GitHub API 获取成功")

    # 检查已下载的文件
    existing = set(os.listdir(DATA_DIR)) if DATA_DIR.exists() else set()
    to_download = [f for f in files if f not in existing]
    if not to_download:
        total = len(os.listdir(DATA_DIR))
        print(f"\n✅ 全部 {total} 个文件已下载完毕，无需重复下载。")
        return

    print(f"需要下载 {len(to_download)} 个文件（已跳过 {len(files) - len(to_download)} 个已存在的）\n")
    print("-" * 60)

    # 逐个下载
    success = 0
    fail = 0
    for i, name in enumerate(to_download, 1):
        target = DATA_DIR / name
        print(f"[{i:3d}/{len(to_download):3d}] {name}")

        ok = download_file(name, target)
        if ok:
            size = target.stat().st_size
            print(f"      ✅ {size / 1024:.1f} KB")
            success += 1
        else:
            fail += 1

        # 礼貌性间隔
        if i % 5 == 0:
            time.sleep(0.3)

    # 汇总
    print("-" * 60)
    print(f"\n📊 下载完成:")
    print(f"   ✅ 成功: {success}")
    print(f"   ❌ 失败: {fail}")
    print(f"   📁 保存位置: {DATA_DIR}")

    # 显示已下载的文件
    downloaded = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".txt"))
    print(f"\n📄 共 {len(downloaded)} 个法律文件:")
    for f in downloaded:
        fsize = os.path.getsize(DATA_DIR / f) / 1024
        print(f"   {f} ({fsize:.1f} KB)")


if __name__ == "__main__":
    main()
