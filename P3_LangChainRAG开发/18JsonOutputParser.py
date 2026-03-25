from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

#创建所需解析器
str_parser = StrOutputParser()
#转为字典格式
json_parser = JsonOutputParser()

#创建模型
model = ChatTongyi(model="qwen3-max")

#第一个提示词模板
first_prompt = PromptTemplate.from_template(
    "我的同学专业为{major},刚升入{grade}年级，请帮忙推荐一本专业书籍，并封装为JSON格式返回给我，要求key是book，value就是你推荐的书籍，请严格遵守格式要求。"
)

#第二个提示词模板
second_prompt = PromptTemplate.from_template(
    "书籍:{book},请帮我简要介绍内容。"
)

#构建链   (AIMessage("{book:人工智能书籍}")
# 字典->promptValue->AIMessage->字典->promptValue->AIMessage->字符串
chain = first_prompt | model | json_parser | second_prompt | model | str_parser

for chunk in chain.stream({"major":"人工智能","grade":"大三"}):
    print(chunk,end = "",flush = True)
