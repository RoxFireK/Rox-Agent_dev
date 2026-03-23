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

#StringPromptValue   to_string()
prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()

model = ChatTongyi(model = "qwen3-max")
res = model.invoke(prompt_text)
# type  <class 'langchain_core.messages.ai.AIMessage'>
print(res.content,type(res))