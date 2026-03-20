#langchain_ollama
from langchain_ollama import OllamaLLM
model = OllamaLLM(model="qwen3-vl:8b")
#invoke: 调用模型，一次性返回完整结果
res = model.invoke(input="你是谁，你能做什么?")
print(res)