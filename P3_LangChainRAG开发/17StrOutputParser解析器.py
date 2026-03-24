from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage

parser = StrOutputParser()
#可以将AIMessage类型转换为基础字符串
#可以加入chain作为组件存在(runnable接口子类)
model = ChatTongyi(model = "qwen3-max")
prompt = PromptTemplate.from_template(
    "我邻居姓:{lastname},刚生了{gender},请起名,仅告知我名字无需其他内容。"
)

chain = prompt | model | parser | model | parser
res:str = chain.invoke({"lastname":"张","gender":"女儿"})
print(res)
print(type(res))
