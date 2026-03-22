from langchain_community.callbacks import HumanApprovalCallbackHandler
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

#得到模型对象
model = ChatTongyi(model = "qwen3-max")
#准备消息列表
#静态，一步到位，直接得到Message类的类对象
messages = [
    SystemMessage(content="你是一个边塞诗人。"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照你上一个回复的格式，再写一首唐诗")
]
#调用stream流式运行
res = model.stream(input = messages)
#for循环迭代打印输出,通过.contnt来获取内容
for chunk in res:
    print(chunk.content,end="",flush=True)
