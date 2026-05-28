"""
扫描所有法律文件，检查解析情况
"""

import sys
import re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pathlib import Path
from rag.reader import scan_files, read_lines
from rag.parser import parse_lines


def main():
    files = scan_files()
    print(f"共 {len(files)} 个法律文件\n")

    issues = []
    total_articles = 0

    for file_path in files:
        lines = read_lines(file_path)
        articles = parse_lines(lines, source_file=str(file_path))

        total_articles += len(articles)

        # 统计
        total = len(lines)
        parsed = len(articles)
        rate = parsed / total * 100 if total > 0 else 0

        # 检查未匹配的条文
        parsed_nums = set()
        for a in articles:
            m = re.search(r'第(.+)条', a.article_number)
            if m:
                parsed_nums.add(m.group(1))

        unmatched = []
        for i, line in enumerate(lines, 1):
            m = re.search(r'第([一二三四五六七八九十百千万零\d]+)条', line)
            if m and m.group(1) not in parsed_nums:
                unmatched.append((i, line[:60]))

        # 标记有问题的文件
        flag = ""
        if rate < 80:
            flag = " ⚠️ 匹配率偏低"
        if unmatched:
            flag += f" ❌ {len(unmatched)} 条未匹配"

        if flag:
            issues.append((file_path.name, rate, unmatched))

        # 输出
        status = "✅" if not flag else "⚠️"
        print(f"{status} {file_path.name:35s} {total:>4d} 行 → {parsed:>4d} 条 ({rate:5.1f}%){flag}")

    print(f"\n总计: {total_articles} 条法律条文")

    # 汇总问题文件
    if issues:
        print("\n" + "=" * 60)
        print("📋 需要关注的文件:")
        print("=" * 60)
        for name, rate, unmatched in issues:
            print(f"\n⚠️  {name} (匹配率 {rate:.1f}%)")
            for lineno, content in unmatched:
                print(f"      L{lineno}: {content}...")
    else:
        print("\n✅ 全部文件解析正常")


if __name__ == "__main__":
    main()
