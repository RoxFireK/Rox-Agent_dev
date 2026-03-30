from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#TextLoader是一个简单的加载器，可以加载txt文件
loader = TextLoader("data/python基础语法.txt",encoding="utf-8")

docs = loader.load()      # [Document]

#递归字符文档分割器
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,     #分段的最大字符数
    chunk_overlap=50,   #分段之间允许重叠字符数
    # 文本自然段落分隔的依据符号
    separators=["\n\n","\n",",",".","!","?","，","。","！","？"," "],
    length_function=len,     #统计字符的依据函数
)

split_docs = splitter.split_documents(docs)
print(len(split_docs))
for doc in split_docs:
    print("=" * 20)
    print(doc)
    print("=" * 20)