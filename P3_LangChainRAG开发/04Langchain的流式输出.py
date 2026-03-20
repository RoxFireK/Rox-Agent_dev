"""from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model="qwen-max")

#通过stream方法获得逐段流式输出
res = model.stream(input="你是什么，能做什么?")

for chunk in res:
    print(chunk,end="",flush = True)"""

from langchain_ollama import OllamaLLM
model = OllamaLLM(model="qwen3-vl:8b")
res = model.stream(input="你是谁，你能做什么?")
for chunk in res:
    print(chunk,end = "",flush = True)