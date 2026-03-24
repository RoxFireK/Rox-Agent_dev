from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个边塞诗人，可以作诗。"),
        MessagesPlaceholder("history"),
        ("human","请再来一首唐诗"),
    ]
)

history_data = [
    ("human","你来写一首唐诗"),
    ("ai","床前明月光，疑是地上霜，举头望明月，低头思故乡"),
    ("human","再来一首"),
    ("ai","锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦"),
]
#用qwen不要开VPN
model = ChatTongyi(model = "qwen3-max")
#组成链 要求每一个组件都是runnable接口的子类
chain = chat_prompt_template | model
#chain = chat_prompt_template | model | ... | ... | model2 | model3 | ...只要都是runnable接口对象就行

#通过链调用invoke/stream
#res = chain.invoke({"history" : history_data})
#print(res.content)

#通过stream流式输出
for chunk in chain.stream({"history": history_data}):
    print(chunk.content,end="",flush = True)