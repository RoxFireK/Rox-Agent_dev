from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

model = ChatTongyi(model = "qwen3-max")
str_parser = StrOutputParser()
first_prompt = PromptTemplate.from_template(
    "我邻居姓:{lastname},刚生了{gender},请帮忙起名字，仅生成一个名字，并告知我名字，不需额外信息。"
)

second_prompt = PromptTemplate.from_template(
    "姓名{name},请帮我解析含义。"
)
#入参:AIMessage->dict ({"name":"xxx"})
#在链中加入自定义函数
#my_func = RunnableLambda(lambda ai_msg:{"name":ai_msg.content})

chain = first_prompt | model | (lambda ai_msg:{"name":ai_msg.content}) | second_prompt | model | str_parser

for chunk in chain.stream({"lastname":"张","gender":"女孩"}):
    print(chunk,end = "",flush = True)