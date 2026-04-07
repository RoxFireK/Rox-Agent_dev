"""
基于streamlit完成WEB网页上传服务
"""
import time

#当页面元素发生变化，则代码重新执行一遍
import streamlit as st
from knowledge_base import KnowledgeBaseService
#添加网页标题
st.title("知识库更新服务")

# file_uploader
# type指定文件格式
# accept_multiple_files是否接受多个文件上传
uploader_file = st.file_uploader(
    "请上传TXT文件",
    type = ['txt'],
    accept_multiple_files = False,
)

#session_state就是一个字典
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    #提取文件信息
    file_name = uploader_file.name  #获取文件名
    file_type = uploader_file.type  #获取文件类型
    file_size = uploader_file.size/1024  #获取文件大小(KB)

    st.subheader(f"文件名:{file_name}")
    st.write(f"格式:{file_type} | 大小:{file_size:.2f} KB")
    # 获取内容
    # get_value->bytes->decode('utf-8')
    text = uploader_file.getvalue().decode("utf-8")

    #在spinner内的代码执行过程中，会有一个转圈动画
    with st.spinner("载入知识库中..."):
        time.sleep(1)
    result = st.session_state["service"].upload_by_str(text,file_name)
    st.write(result)
    #st.write(text)

    #st.session_state["counter"] += 1
    #里面用双引号外面用单引号,引号不能重复
    #print(f'上传了{st.session_state["counter"]}个文件')

#如何运行
#打开终端
#d:
#cd D:\AIagent\P4_RAG项目案例
#conda activate agent_dev
#streamlit run app_file_uploader.py
