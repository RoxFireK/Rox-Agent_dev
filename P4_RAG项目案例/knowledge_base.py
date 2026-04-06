"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str:str):
    """检查传入的md5字符串是否已经被处理过了
        return False 表示未处理过这个md5文件
        return True 表示已处理过，已有记录
    """
    if not os.path.exists(config.md5_path):
        # if进入表示文件不存在，肯定没有处理过这个md5文件
        open(config.md5_path,'w',encoding = 'utf-8').close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding = 'utf-8').readlines():
            line = line.strip()        #处理字符串开头和结尾的空白字符(空格、换行、回车、制表)
            if line == md5_str:
                return True           #已处理过
        return False

#md5_str:str ':'起到一个提示参数类型的作用，便于检查和IDE智能补全
def save_md5(md5_str:str):
    """将传入的md5字符串，记录到文件内保存"""
    #with...as f 自动管理文件资源，确保文件在使用完毕后被正确关闭，即使发生异常也会自动关闭 类似于内部实现了一个try finally
    with open(config.md5_path,'a',encoding = 'utf-8') as f:
        f.write(md5_str + '\n')


def get_string_md5(input_str:str,encoding='utf-8'):
    """将传入的字符串转换为md5字符串"""

    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)
    # 创建md5对象 md5_hex = hashlib.md5().update(input_str.encode(encoding=encoding)).hexdigest()
    md5_obj = hashlib.md5()           # 得到md5对象
    md5_obj.update(str_bytes)         # 更新内容(传入即将要转换的字节数组)
    md5_hex = md5_obj.hexdigest()     # 得到md5的十六进制字符串,hex：十六进制
    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True)
        #如果文件夹不存在则创建，如果存在则跳过
        self.chroma = Chroma(
            # 向量存储的实例 chroma向量库对象
            collection_name=config.collection_name,  #数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"), #默认为v1修改为v4
            persist_directory=config.persist_directory,
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size, #表示分割后的每一个文本段最大长度
            chunk_overlap = config.chunk_overlap, #连续文本段之间的字符重叠数量
            separators=config.separator, #自然段落划分的符号
            length_function = len, #使用python自带的len函数做长度统计依据
        )       #文本分割器的对象

    # knowledge_chunks:
    # 存储文本片段，用于向量化存储前的数据准备
    # 类型为list[str]
    def upload_by_str(self,data,filename):
        #将传入的字符串进行向量化，存入向量数据库中
        #先得到传入字符串的md5值
        md5_hex = get_string_md5(data)
        if check_md5(md5_hex):
            return "[跳过]内容已经存在知识库中"
        #大于设定最大长度则进行文本分割
        if len(data)>config.max_split_char_number:
            #变量名 :类型 = 值 ':'仅进行提示作用
            knowledge_chunks: list[str] = self.spliter.split_text(data)
            #返回的是一个列表
        else:
            knowledge_chunks = [data]

        #metadata为每个文本块提供附加信息,便于后期检索，过滤和管理
        metadata = {
            "source":filename,
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"小陈",
        }

        self.chroma.add_texts(    #内容加载到向量库中
            # iterable->list\tuple
            knowledge_chunks,
            metadatas = [metadata for _ in knowledge_chunks],
        )

        #
        save_md5(md5_hex)
        return "[成功]内容已经成功载入向量库"

if __name__ == '__main__':
    # md5特性:只要str一样,md5代码一定一样,并且不管多长md5长度一定固定
    service = KnowledgeBaseService()
    r = service.upload_by_str("凯尔希","testfile")
    print(r)

    #save_md5("8e777f2c6f7f860da463bfb4d8e5b7c6")
    #print(check_md5("8e777f2c6f7f860da463bfb4d8e5b7c6"))

    #r1 = get_string_md5("凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希凯尔希")
    #r2 = get_string_md5("凯尔希")
    #r3 = get_string_md5("阿米娅")

    #print(r1)
    #print(r2)
    #print(r3)
