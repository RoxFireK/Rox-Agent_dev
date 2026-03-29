import os,json
from typing import Sequence
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
#message_to_dict:单个消息对象(BaseMessage类实例) ->字典
#messages_from_dict:[字典、字典...] ->[消息，消息...]
#AIMessage,HumanMessage,SystemMessage 都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id   #会话id
        self.storage_path = storage_path   #不同会话id存储文件所在的文件夹路径
        self.file_path = os.path.join(self.storage_path,self.session_id) #将文件夹路径和session文件路径连接到一起构成完整的文件路径

        #确保文件夹存在,exist_ok参数确保如果不存在会创建
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列，类似于list,tuple
        all_messages = list(self.messages)   # 已有的消息列表
        all_messages.extend(messages)        # 新的和已有的融合成一个list

        # 将数据同步写入到本地文件当中
        # 类对象写入文件 -> 一堆二进制
        # 为了方便，可以将BaseMessage消息作为字典(借助json模块以json字符串写入文件)
        #官方message_to_dict:单个消息对象(BaseMessage类实例) ->字典

        """new_messages = []
        for message in all_messages:
            d = message_to_dict(message)
            new_messages.append(d)
            下面的代码可以代替这四行"""
        #转化为dict
        new_messages = [message_to_dict(message) for message in all_messages]
        #将数据写入文件
        #以只读模式打开指定路径的文件，并使用UTF-8编码读取内容
        #"r":只读，"w":修改 旧内容舍弃，"a":添加内容到末尾
        with open(self.file_path,"w",encoding="utf-8") as f:
            #在内部进行文件操作
            #把列表信息转成json导入到文件夹中
            json.dump(new_messages,f)

    @property       #@property装饰器将messages方法变成成员属性用
    def messages(self)->list[BaseMessage]:
        # 当前文件内: list[字典]
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                message_data = json.load(f)     #返回值就是 list[字典]
                return messages_from_dict(message_data)
        except FileNotFoundError:
            return []

    def clear(self)->None:
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)




model = ChatTongyi(model = "qwen3-max")
#prompt = PromptTemplate.from_template(
#    "你需要根据会话历史回应用户问题，对话历史:{chat_history},用户提问
#    :{input},请回答"
#)
prompt= ChatPromptTemplate.from_messages(
    [
        ("system","你需要根据会话历史回应用户问题，对话历史:"),
        MessagesPlaceholder("chat_history"),
        ("human","请回答如下问题：{input}")
    ]
)
str_parser = StrOutputParser()

def print_prompt(full_prompt):
    print("="*20,full_prompt.to_string(),"="*20)
    return full_prompt

base_chain = prompt | print_prompt | model | str_parser

#key就是session_id,value就是InMemoryChatHistory类对象
#实现通过对话id获取InMemoryChatHistory类对象
def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")

#创建一个新链，对原有链增强功能，自动附加历史信息
conversation_chain = RunnableWithMessageHistory(
    base_chain,         #被增强的原有链
    get_history,        #通过会话id获取InMemory
    input_messages_key = "input",   #表示用户输入在模板中的占位符
    history_messages_key = "chat_history" #表示历史消息在模板中的占位符
)

if __name__ == "__main__":
    #固定格式，添加Langchain的配置，为当前程序配置所属的session_id
    session_config = {
        "configurable" : {
            "session_id" : "user_001"
        }
    }

    #res = conversation_chain.invoke({"input":"小明有两个猫"},session_config)
    #print("第一次执行:", res)
    #res = conversation_chain.invoke({"input": "小刚有一只狗"}, session_config)
    #print("第二次执行:", res)
    res = conversation_chain.invoke({"input": "总共有几个宠物"}, session_config)
    print("第三次执行:", res)

