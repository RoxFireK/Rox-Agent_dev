from openai import OpenAI
#获取client对象
client = OpenAI(
    base_url="http://localhost:11434/v1"
)
#调用模型
response = client.chat.completions.create(
    #模型名称一定要是正确的
    model="qwen3-vl:8b",   # type: ignore
    messages=[  # type: ignore
        #system 设定模型行为和规则
        {"role":"system","content":"你是一个python编程专家，并且不说废话简单回答"},
        #设定模型的回答，由用户设定
        {"role":"assistant","content":"我是编程大师，人狠话不多，你要问什么?"},
        #用户的提问
        {"role":"user","content":"输出1-10数字，使用python代码"}
    ],
    #开启流式输出
    stream = True
)
for chunk in response:
    print(
        chunk.choices[0].delta.content,
        end =" ",       #每一段之间以空格分隔
        flush = True    #立刻刷新缓冲区
    )