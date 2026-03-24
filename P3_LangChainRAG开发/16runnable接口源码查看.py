from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
prompt = PromptTemplate.from_template("你是一个ai助手")
model = Tongyi(model = "qwen3-max")

chain = prompt | model | prompt | model
chain.invoke()
chain.stream()

print(type(chain))
#<class 'langchain_core.runnables.base.RunnableSequence'>无论如何叠加，类型总为RunnableSequence