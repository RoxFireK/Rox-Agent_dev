from openai import OpenAI
#获取client对象
client = OpenAI(
    base_url="http://localhost:11434/v1"
)
#调用模型
response = client.chat.completions.create(
    #模型名称一定要是正确的
    model="qwen3-vl:8b",
    #message即历史记录，可以组织历史消息
    messages=[  # type: ignore
        {"role":"system","content":"你是一个ai助理,回答简洁,不输出空白字符"},
        {"role":"user","content":"小明有一条宠物狗"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"小红有三只宠物猫"},
        {"role":"assistant","content":"好的"},
        {"role":"user","content":"总共有几只宠物呢？"}
    ],
    #开启流式输出
    stream = True
)
for chunk in response:
    if chunk.choices and chunk.choices[0].delta:
        content = chunk.choices[0].delta.content
        if content:
            print(
                chunk.choices[0].delta.content,
                end =" ",       #每一段之间以空格分隔
                flush = True    #立刻刷新缓冲区
            )