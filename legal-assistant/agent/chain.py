import os
from langchain_deepseek import ChatDeepSeek

# 压缩的提示词
CONDENSE_PROMPT = (
    "根据聊天历史，把用户的问题重写为包含上下文的独立问题，直接输出问题不要解释。\n"
    "聊天历史：{history}\n用户问题：{question}\n独立问题："
)
# 问答的提示词
QA_PROMPT = (
    "你是一位中国法律助手。根据以下法律条文回答问题。"
    "若条文不足请如实说明，不要编造。引用时注明法律名和条款号。\n\n"
    "条文：\n{context}\n\n问题：{question}\n回答："
)

from dotenv import load_dotenv
load_dotenv()

# 构建一个问答智能体
def build_chain(retriever):
    llm = ChatDeepSeek(model=os.getenv("LLM_MODEL", "deepseek-chat"), temperature=0)
    return LawChain(llm, retriever)

class LawChain:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever
        self.history = [] # 历史记录 [(问,答)]
    def ask(self, question: str) -> str:
        # 1. 有聊天历史先重写问题
        if self.history:
            history_text = "\n".join(
                f"问：{q}\n答：{a}" for q, a in self.history
            )
            rewritten = self.llm.invoke(
                CONDENSE_PROMPT.format(history=history_text, question=question)
            ).content.strip()
        else:
            rewritten = question

        #2. 检索相关法条
        docs = self.retriever._get_relevant_documents(rewritten)
        context = "\n\n".join(
            f"——《{d.metadata['law_name']}》第{d.metadata['article_number']}条——\n{d.page_content}"
            for d in docs
        )

        # 3. 生成回答
        answer = self.llm.invoke(
            QA_PROMPT.format(context=context, question=question)
        ).content.strip()

        # 4. 记入历史
        self.history.append((question, answer))
        return answer