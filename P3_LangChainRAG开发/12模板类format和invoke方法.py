from langchain_core.prompts import PromptTemplate
#通用提示词模板，支持动态注入信息
from langchain_core.prompts import FewShotPromptTemplate
#支持基于模板注入任意数量的示例信息
from langchain_core.prompts import ChatPromptTemplate
#支持注入任意数量的历史会话信息

"""
PromptTemplate->StringPromptTemplate->BasePromptTemplate
FewShotPromptTemplate->StringPromptTemplate->BasePromptTemplate
ChatPromptTemplate->BaseChatPromptTemplate->BasePromptTemplate
"""
#通过from_messages方法,从列表中获取多轮次对话作为聊天的基础模板
#历史对话信息随着对话进行不断积攒，需要支持动态注入
template = PromptTemplate.from_template("我的邻居是:{lastname},最喜欢{hobby}")
res = template.format(lastname="张三",hobby="钓鱼")
print(res,type(res))

res2 = template.invoke({"lastname":"李四","hobby":"下棋"})
print(res2,type(res2))