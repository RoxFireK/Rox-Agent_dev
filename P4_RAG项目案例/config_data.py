#需要多次修改的变量应单独设置文件进行保存和调用
md5_path = "./md5.text"

#Chroma
collection_name = "rag"
persist_directory = "./chroma_db"

#spliter
chunk_size = 1000
chunk_overlap = 100
separator = ["\n\n","\n",",",".","!","?","，","。","！","？"," "]
max_split_char_number = 1000
