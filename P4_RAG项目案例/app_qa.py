import time
from rag import RagService
import streamlit as st
import config_data as config
#标题
st.title("智能客服")
#分割行
st.divider()

#第一句话输出
if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好，有什么可以帮助你的吗？"}]

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

#显示对话记录
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

#在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:
    #在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    ai_res_list = []
    #AI回答
    with st.spinner("少女祈祷中......"):
        #由于stream模式下的res_stream是一个迭代器，最后输出完全部内容内部不会存储任何字段
        res_stream = st.session_state["rag"].chain.stream({"input": prompt},config.session_config)
        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        st.chat_message("assistant").write_stream(capture(res_stream,ai_res_list))
        #.join:所有字符串连成一个完整字符串
        st.session_state["message"].append({"role":"assistant","content":"".join(ai_res_list)})
