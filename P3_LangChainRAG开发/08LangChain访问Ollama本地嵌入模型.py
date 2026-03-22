from langchain_ollama import OllamaEmbeddings

#创建模型对象  不传model默认用的是 text-embeddings-v1
#命令行命令下载模型ollama pull qwen3-embedding:8b
model = OllamaEmbeddings(model="qwen3-embedding:8b")

#不用invoke stream
#embed_query embed_documents
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你","我稀饭你","晚上吃啥"]))