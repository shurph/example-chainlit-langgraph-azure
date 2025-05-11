import uuid

import chainlit as cl
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage
from langgraph.graph.state import CompiledStateGraph

from app.commands.processor import CommandsProcessor


async def message_processor(
    msg: cl.Message,
    graph: CompiledStateGraph,
    # graph,
    commands_processor: CommandsProcessor,
    callback_handler: cl.AsyncLangchainCallbackHandler,
):
    config = {
        "configurable": {"thread_id": cl.context.session.id},
        "run_id": uuid.uuid4(),
    }
    final_answer = cl.Message(content="")

    response = await commands_processor.process(msg)
    if response.need_to_interrupt:
        return

    custom_handler = callback_handler

    for msg, metadata in await cl.make_async(graph.stream)(
        {"messages": [HumanMessage(content=msg.content)]},
        stream_mode="messages",
        config=RunnableConfig(
            callbacks=[custom_handler],
            **config,
        ),
    ):
        if not msg.content:
            continue
        if isinstance(msg, HumanMessage):
            continue
        if metadata["langgraph_node"] == "node_final_model":
            await final_answer.stream_token(msg.content)

        if metadata["langgraph_node"] == "node_first_model":
            await final_answer.stream_token(msg.content)

    await final_answer.send()
