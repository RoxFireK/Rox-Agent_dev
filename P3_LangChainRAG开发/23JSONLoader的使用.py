from langchain_community.document_loaders import JSONLoader

#python的JSON模块默认为utf-8不需要单独设置
loader = JSONLoader(
    file_path = "./data/stu_json_lines.json",
    jq_schema=".name",
    # 上面两个必填s
    # .表示根、[]表示数组
    # .name 表示从根取name的值
    # .hobby[1]表示取hobby对应数组的第二个元素
    # .[]表示取数组内的每个字典(json对象)
    # .[].name表示取数组内每个字典(json)对象的name对应的值

    text_content = False, #告知JSONLoader 我抽取的内容不是字符串
    json_lines = True     #告知JSONLoader 这是一个JSONLines文件(每一行都是一个独立的标准JSON)
)

document = loader.load()
print(document)