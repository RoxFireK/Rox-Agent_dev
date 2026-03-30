from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader(
    file_path = "data/pdf2.pdf",
    mode = "single",      #默认为page模式,每个页面形成一个Document文档对象
    #single:不管多少页只返回一个document对象
    password = "itheima"
)
#PyPDFLoader 进行pdf文件内容的分割
i = 0
for doc in loader.lazy_load():
    i +=1
    print(doc)
    print("="*20,i)