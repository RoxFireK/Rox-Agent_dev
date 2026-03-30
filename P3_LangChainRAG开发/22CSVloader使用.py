from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path ="data/stu.csv",
    csv_args={
        "delimiter": ",",    #指定分隔符
        "quotechar": '"',   #指定带有分隔符文本的引号包围是单引号还是双引号
        #为数据添加表头，如果没有表头，可以添加以进行标注
        "fieldnames": ['name','age','gender','hobby']
    },
    encoding = "utf-8"          #指定编码为utf-8
)

# 批量加载 .load() ->  [document,document,....]
#documents = loader.load()

#for document in documents:
    #print(type(documents),document)

#懒加载  .lazy_load()   迭代器[Document]
for document in loader.lazy_load():
    print(document)