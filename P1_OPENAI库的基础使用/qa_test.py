from openai import OpenAI
import time
import streamlit as st


#标题
st.title("智能客服")
#分割行
st.divider()

#第一句话输出
if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好，有什么可以帮助你的吗？"}]
#显示对话记录
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

#在页面最下方提供用户输入栏
prompt = st.chat_input()

if prompt:
    #在页面输出用户的提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})
    # 获取client对象
    client = OpenAI(
        base_url="http://localhost:11434/v1"
    )
    # 调用模型
    response = client.chat.completions.create(
        # 模型名称一定要是正确的
        model="qwen3-vl:8b",
        messages=[{"role":"user","content":prompt}],
    )

    #AI回答
    with st.spinner("少女祈祷中......"):
        time.sleep(1)
        st.chat_message("assistant").write(response.choices[0].message.content)
        st.session_state["message"].append({"role":"assistant","content":response.choices[0].message.content})