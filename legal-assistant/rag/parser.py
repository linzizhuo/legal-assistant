import re
from pathlib import Path
from models.law import LegalArticle

# 标准格式：《法律名称》第X条【标题】内容
# 宪法格式：第X条 内容（无《法律名称》前缀）
PATTERN = re.compile(
    r'(?:《(?P<law_name>[^》]+)》.*?)?'            # 可选的《法律名称》
    r'第(?P<article_num>[一二三四五六七八九十百千万零\d]+)条'  # 第X条（必选）
    r'(?:【(?P<article_title>[^】]+)】)?'         # 可选的【标题】
    r'[，,。\s]*'                                  # 条文前面的标点
    r'(?P<content>.*)'                             # 条文正文
)

# 匹配"第X条"（用于合并续行时判断是否为新条文）
ARTICLE_START = re.compile(r'第[一二三四五六七八九十百千万零\d]+条')


def _extract_law_name(file_path: str) -> str | None:
    """从文件名提取法律名称：中华人民共和国XX法.txt → 中华人民共和国XX法"""
    name = Path(file_path).stem
    if name.startswith("中华人民共和国"):
        return name
    return None


def _parse_article_line(line: str, default_law_name: str | None = None) -> LegalArticle | None:
    """将一行法律条文解析为 LegalArticle，失败返回 None"""
    match = PATTERN.match(line)
    if not match:
        return None

    content = match.group("content").strip()
    # 内容为空（比如"第一章 总纲"）直接跳过
    if not content or len(content) < 4:
        return None

    law_name = match.group("law_name") or default_law_name
    if not law_name:
        return None

    return LegalArticle(
        law_name=law_name,
        article_number="第" + match.group("article_num") + "条",
        article_title=match.group("article_title"),
        content=content,
    )


def _merge_continuation_lines(lines: list[str]) -> list[str]:
    """将续行合并到所属的条文中"""
    merged = []
    current = ""
    for line in lines:
        # 跳过章节标题（第一章、第一节等）
        if re.match(r'^第[一二三四五六七八九十百千万零\d]+[章节编]', line):
            continue
        if ARTICLE_START.search(line):
            if current:
                merged.append(current)
            current = line
        elif current:
            current += line
    if current:
        merged.append(current)
    return merged


def extract_articles(lines: list[str], source_file: str = "") -> list[LegalArticle]:
    """从法律文本行中提取所有法律条文"""
    lines = _merge_continuation_lines(lines)
    default_name = _extract_law_name(source_file) if source_file else None
    articles = []
    for line in lines:
        article = _parse_article_line(line, default_law_name=default_name)
        if article is not None:
            articles.append(article)
    return articles