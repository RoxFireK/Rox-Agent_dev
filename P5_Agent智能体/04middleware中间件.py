from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime

@tool(description="查询天气,传入城市名称字符串，返回字符串天气信息")
def get_weather(city:str) -> str:
    return "晴天"

"""
1.agent执行前
2.agent执行后
3.model执行前
4.model执行后
5.工具执行中
6.模型执行中
"""

@before_agent
def log_before_agent(state:AgentState,runtime:Runtime)->None:
    print(f"[before agent]agent启动,并附带{len(state['messages'])}消息")

@after_agent
def log_after_agent(state:AgentState,runtime:Runtime)->None:
    print(f"[after agent]agent结束,并附带{len(state['messages'])}消息")

@before_model
def log_before_model(state:AgentState,runtime:Runtime)->None:
    print(f"[before model]模型即将调用,并附带{len(state['messages'])}消息")

@before_model
def log_before_model(state:AgentState,runtime:Runtime)->None:
    print(f"[after model]模型即将调用,并附带{len(state['messages'])}消息")

@after_model
def log_after_model(state:AgentState,runtime:Runtime)->None:
    print(f"[after model]模型调用结束,并附带{len(state['messages'])}消息")

@wrap_model_call
def model_call_hook(request,handler):
    print("模型已调用")
    return handler(request)

@wrap_tool_call
def monitor_tool(request,handler):
    print(f"工具执行:{request.tool_call['name']}")
    print(f"工具执行传入参数:{request.tool_call['args']}")
    return handler(request)

agent = create_agent(
    model = ChatTongyi(model = "qwen3-max"),  #智能体大脑LLM
    tools = [get_weather],   #向智能体提供工具列表
    middleware = [log_before_agent, log_after_agent, log_before_model, log_after_model, model_call_hook, monitor_tool]
)

res = agent.invoke(
    {
        "messages":[
            {"role":"user","content":"武汉今天天气如何，如何穿衣"},
        ]
    }
)
print("**************\n",res)