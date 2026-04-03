#提示词:用户提问->向量库中检索到的参考资料
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

#导入模型
model = ChatTongyi(model = "qwen3-max")
#提示词模板
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主，简洁和专业的回答用户问题，参考资料{context}。"),
        ("user","用户提问:{input}")
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model = "text-embedding-v4"))

#准备向量库的数据
#add_texts 传入一个list[str]
vector_store.add_texts(["减肥就是要少吃多练", "在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"])
input_text = "怎么减肥?"

# langchain中向量存储对象，有一个方法: as_retriever,可以返回一个Runnable接口的子类实例对象,即进行数据库的智能检索，可以处理私有/新知识，减少幻觉，提供可验证来源
# k : 2 如果匹配到，返回的最大条数
retriever = vector_store.as_retriever(search_kwargs={"k":2})

def format_func(docs:list[Document]):
    if not docs:
        return "无相关参考资料"
    formatted_str = "["
    for doc in docs:
        formatted_str +=doc.page_content
    formatted_str += "]"

    return formatted_str

# chain支持callable函数类和mapping字典类，chain里可以放字典
#chain = retriever | prompt |model | StrOutputParser()
#大链嵌套小链 invoke输入给 retriever
chain = (
    {"input":RunnablePassthrough(),"context":retriever | format_func} | prompt | model | StrOutputParser()
)
#invoke为链启动的开始
res = chain.invoke(input_text)
print(res)
"""
retriever:
    输入：用户的提问          str
    输出:向量库的检索结果     list[document]
prompt:
    输入:用户提问+向量库检索结果  dict
    输出:完整的提示词            PromptValue
"""