import os
import sys
import io

#
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
print("RUNNABLE_BASE_URL: ", os.getenv("RUNNABLE_BASE_URL"))

#
from IPython.display import display, Markdown
def print_content(data):
    for char in data:
        print(char, end="", flush=True)

#
from langserve import RemoteRunnable
def remote_runnable(runnable, params = [], base_url = os.getenv("RUNNABLE_BASE_URL"), debug=os.getenv("DEBUG_MODE")):
    chain = RemoteRunnable(f"{base_url}/{runnable}")
    def ask(*args):
        kwargs = dict(zip(params, args))
        if debug:
            print_content(chain.stream(kwargs))
        else:
            return chain.invoke(kwargs)
    return ask

# 导出这些单轮对话的工具
gpt35 = remote_runnable("langserve/gpt35", ["question"])
gpt4 = remote_runnable("langserve/gpt4", ["question"])
tongyi = remote_runnable("langserve/tongyi", ["question"])
chatglm = remote_runnable("langserve/chatglm6b", ["question"])