from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

#Chroma 向量数据库 (轻量级)
#确保langchain-chroma chromadb 安装
vector_store = Chroma(
    collection_name = "test",  #当前向量存储的名字
    embedding_function=DashScopeEmbeddings(),  #嵌入模型
    persist_directory="./chroma_db"   #指定数据存放的文件夹
)

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source",    # 指定本条数据的来源是哪里,适配数据库
)

documents = loader.load()

#向量存储的 新增、删除、检索
#==========新增==========
vector_store.add_documents(
    documents = documents,        #被添加的文档,类型:list[document]
    ids = ["id"+str(i) for i in range(1,len(documents)+1)]                       #给添加的文档提供id(字符串) list[str]
)

#==========删除==========  传入[id,id,...]
vector_store.delete(["id1","id2"])

#==========检索==========  返回类型list[Document]
result = vector_store.similarity_search(
    "Python是不是简单易学",
    3,   #检索几个结果
    #过滤器，只过滤指定表头
    filter = {"source":"title"}
)

print(result)