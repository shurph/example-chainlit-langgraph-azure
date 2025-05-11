import os
import uuid
from typing import Literal

import chainlit as cl
from dotenv import load_dotenv
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAI as ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from app.commands.definitions import commands_definitions
from app.commands.processor import CommandsProcessor, register_commands
from app.messaging import message_processor
from app.tools.get_similar_sessions import get_similar_sessions
from app.tools.get_weather import get_weather

load_dotenv()


model_config = {
    "openai_api_version": os.environ["AZURE_OPENAI_API_VERSION"],
}
model = AzureChatOpenAI(
    **model_config,
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    # temperature=0,
)
final_model = AzureChatOpenAI(
    **model_config,
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    # temperature=0,
)
final_model = final_model.with_config(tags=["final_node"])


def condition_should_continue(_intermediate_node, _end_node):
    def should_continue(
        state: MessagesState,
    ) -> Literal[
        _intermediate_node,
        _end_node,
    ]:
        messages = state["messages"]
        last_message = messages[-1]
        # If the LLM makes a tool call, then we route to the "tools" node
        if last_message.tool_calls:
            return _intermediate_node
        # Otherwise, we stop (reply to the user)
        return _end_node

    return should_continue


def node_final_model(state: MessagesState):
    messages = state["messages"]
    last_ai_message = messages[-1]
    response = final_model.invoke(
        [
            SystemMessage("Rewrite this in the voice of Al Roker"),
            HumanMessage(last_ai_message.content),
        ]
    )
    # overwrite the last AI message from the agent
    response.id = last_ai_message.id
    return {"messages": [response]}


node_final_model.name = "node_final_model"


def node_first_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


node_first_model.name = "node_first_model"


tools = [get_similar_sessions, get_weather]
node_tools_node = ToolNode(tools=tools, name="my_tools")
model = model.bind_tools(tools)


workflow = StateGraph(MessagesState)

workflow.add_node(node_first_model.name, node_first_model)
workflow.add_node(node_tools_node.name, node_tools_node)

# add a separate final node
workflow.add_node(node_final_model.name, node_final_model)

workflow.add_edge(START, node_first_model.name)
workflow.add_conditional_edges(
    node_first_model.name,
    condition_should_continue(node_tools_node.name, node_final_model.name),
)
workflow.add_edge(node_tools_node.name, node_first_model.name)
workflow.add_edge(node_final_model.name, END)

checkpointer = MemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

commands_buttons, commands_router = register_commands(commands_definitions)
commands_processor = CommandsProcessor(commands_router)


@cl.on_chat_start
async def start():
    await cl.context.emitter.set_commands(commands_buttons)


@cl.on_message
async def on_message(msg: cl.Message):
    custom_callback_handler = cl.AsyncLangchainCallbackHandler(
        _schema_format="original+chat"
    )

    await message_processor(
        msg,
        graph,
        commands_processor,
        custom_callback_handler,
    )


@cl.set_starters
async def set_starters():
    from app.starters.base import starters

    return starters
