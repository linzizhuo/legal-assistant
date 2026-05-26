from pydantic import BaseModel

# 存储法律条文的结构体
class LegalArticle(BaseModel):
    law_name: str           # "中华人民共和国民法典"
    article_number: str     # "第八条"
    article_title: str | None = None  # "抢劫罪"（刑法里有，民法没有）
    content: str            # 条文正文