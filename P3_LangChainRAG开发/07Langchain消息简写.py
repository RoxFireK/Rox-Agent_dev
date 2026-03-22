from langchain_community.callbacks import HumanApprovalCallbackHandler
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

#得到模型对象
model = ChatTongyi(model = "qwen3-max")
#准备消息列表
#动态，需要再运行时，由Langchain内部机制转换为Message类对象
#简写模式避免导包，写起来更简单，更重要的是支持内部填充{变量}占位，可在运行时填充具体值
messages = [
    ("system","你是一个边塞诗人。"),
    ("human","写一首唐诗"),
    ("ai","锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human","按照你上一个回复的格式，再写一首唐诗")
]
#调用stream流式运行
res = model.stream(input = messages)
#for循环迭代打印输出,通过.content来获取内容
for chunk in res:
    print(chunk.content,end="",flush=True)