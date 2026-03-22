from langchain_core.prompts import PromptTemplate
#zero_shot
#判断需要哪种模型:单次对话用llm,多次对话需要上下文用对话模型
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},你帮我起个名字，简单回答."
)
model = Tongyi(model = "qwen-max")
#调用.format方法注入信息到prompt_template里
prompt_text = prompt_template.format(lastname = "张",gender = "女儿")
res = model.invoke(input = prompt_text)
"""chain = prompt_template | model
res = chain.invoke(input = {"lastname":"张","gender":"女儿"}"""
print(prompt_text)
print(res)