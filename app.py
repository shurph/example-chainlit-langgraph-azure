import os
import uuid
from typing import Literal

import chainlit as cl
from dotenv import load_dotenv
from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

load_dotenv()


@tool
def get_weather(city: Literal["nyc", "sf", "berezino", "paris", "moscow"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    elif city == "berezino":
        return "It's always sunny in berezino"
    elif city == "paris":
        return "It's might be rainy in paris"
    else:  # for "moscow" case: I'm unable to fetch the weather for Moscow due to a technical issue.
        raise AssertionError("Unknown city")


@tool
def get_similar_sessions(topic):
    """

    Use this function to get a list of sessions that are potentially relevant for the specified topic.
    The sessions are provided in the format of `id|title|abstract|speakers|location (city)|start-time|end-time`.

    """
    return """001|Advances in AI Research|A deep dive into the latest AI advancements and their applications.|Dr. Jane Smith|NYC|2025-06-10T10:00:00|2025-06-10T11:00:00
002|Ethics in Machine Learning|Discussion on ethical dilemmas in ML deployments.|Prof. Alan Doe|Berezino|2025-06-10T11:30:00|2025-06-10T12:30:00
003|Neural Networks for Beginners|Introductory session on how neural networks work.|Dr. Emily Tan|Berezino|2025-06-10T13:00:00|2025-06-10T14:00:00
004|Future of Quantum Computing|Exploring how quantum technologies will reshape computing in the next decade.|Dr. Max Lee|NYC|2025-06-10T14:30:00|2025-06-10T15:30:00
005|Design Thinking in Tech|Learn how to apply design thinking principles to build user-centric products.|Anna Petrova|Moscow|2025-06-10T16:00:00|2025-06-10T17:00:00
006|Cybersecurity Trends 2025|Review of the top threats and protection strategies in cybersecurity.|Michael Chen|Kazan|2025-06-11T09:00:00|2025-06-11T10:00:00
007|Building Scalable Microservices|Best practices for designing and maintaining scalable microservices architecture.|Sarah Khan|San Francisco|2025-06-11T10:30:00|2025-06-11T11:30:00
008|AI in Healthcare|Case studies on how AI is transforming diagnostics and treatment.|Dr. Ahmed Saleh|Warsaw|2025-06-11T12:00:00|2025-06-11T13:00:00
009|Blockchain Beyond Crypto|Discover how blockchain is being applied outside of cryptocurrency.|Elena Morozova|Berlin|2025-06-11T13:30:00|2025-06-11T14:30:00
010|Inclusive Product Development|Creating products that serve diverse users and promote accessibility.|Tariq Johnson|New York City|2025-06-11T15:00:00|2025-06-11T16:00:00
011|Deep Reinforcement Learning|Dive into algorithms and real-world uses of reinforcement learning.|Prof. Li Wei|Paris|2025-06-12T09:00:00|2025-06-12T10:00:00
012|Serverless Architecture Demystified|Pros, cons, and practical tips for serverless infrastructure.|Nina Kuznetsova|Moscow|2025-06-12T10:30:00|2025-06-12T11:30:00
013|Tech & Climate Change|How emerging technologies are tackling environmental challenges.|Carlos Mendes|Mexico City|2025-06-12T12:00:00|2025-06-12T13:00:00
014|Mental Health in Tech|Strategies to maintain well-being in high-stress tech environments.|Rachel Kim|San Francisco|2025-06-12T13:30:00|2025-06-12T14:30:00
015|The Art of Code Reviews|Techniques for effective, respectful, and helpful code reviews.|Igor Petrov|Saint Petersburg|2025-06-12T15:00:00|2025-06-12T16:00:00
016|Women in STEM Leadership|Panel on breaking barriers and leading innovation.|Panel: Dr. Laura Singh, Amara Okafor|Minsk|2025-06-12T16:30:00|2025-06-12T17:30:00
017|ML Ops in Practice|Deploying and maintaining machine learning models in production.|Viktor Ivanov|Paris|2025-06-13T09:00:00|2025-06-13T10:00:00
018|How to Pitch a Tech Startup|Insights on crafting a compelling pitch for investors.|Jasmine Ortega|Almaty|2025-06-13T10:30:00|2025-06-13T11:30:00"""


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


def node_call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


def node_call_final_model(state: MessagesState):
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


tools = [get_similar_sessions, get_weather]
node_tool_node = ToolNode(tools=tools)
model = model.bind_tools(tools)


workflow = StateGraph(MessagesState)

workflow.add_node("first model", node_call_model)
workflow.add_node("tools", node_tool_node)
workflow.add_node("final model", node_call_final_model)
workflow.add_edge(START, "first model")
workflow.add_conditional_edges(
    "first model",
    condition_should_continue("tools", "final model"),
)
workflow.add_edge("tools", "first model")
workflow.add_edge("final model", END)

checkpointer = MemorySaver()

graph = workflow.compile(checkpointer=checkpointer)

commands = []

if os.getenv("SHOW_COMMANDS"):
    commands = [
        {
            "id": "Generate a chat conversation report #",
            "icon": "book-text",
            "description": "Generate a chat conversation report # (enter a number here to proceed)",
            "button": False,
            "persistent": False,
        },
        {
            "id": "Send me files",
            "icon": "paperclip",
            "description": "Send me files",
            "button": True,
            "persistent": False,
        },
    ]


@cl.on_chat_start
async def start():
    await cl.context.emitter.set_commands(commands)


async def send_file(file_path: str, file_name: str):
    elements = [
        cl.File(
            name=file_name,
            path=file_path,
            display="inline",
        ),
    ]

    await cl.Message(content="Here is the file you requested", elements=elements).send()


async def process_commands(msg: cl.Message):
    final_answer = cl.Message(content="")
    need_to_interrupt = True
    if msg.command == "Generate a chat conversation report #":
        content = f"Generating report for {msg.content}..."
        await final_answer.stream_token(content)
        return need_to_interrupt

    if msg.command == "Send me files":
        content = "Sending files..."

        await final_answer.stream_token(content)
        filename = f"report_{msg.content}.txt"
        await send_file("./public/reports/report.txt", filename)

        await final_answer.send()
        return need_to_interrupt


class CustomAsyncCallbackHandler(cl.AsyncLangchainCallbackHandler):
    pass

@cl.on_message
async def on_message(msg: cl.Message):
    config = {
        "configurable": {"thread_id": cl.context.session.id},
        "run_id": uuid.uuid4(),
    }
    final_answer = cl.Message(content="")

    need_to_interrupt = await process_commands(msg)
    if need_to_interrupt:
        return

    custom_handler = CustomAsyncCallbackHandler(_schema_format="original+chat")

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
        if metadata["langgraph_node"] == "final model":
            pass
            await final_answer.stream_token(msg.content)

        if metadata["langgraph_node"] == "first model":
            await final_answer.stream_token(msg.content)

        if isinstance(msg, HumanMessage):
            await final_answer.stream_token("Human said: " + msg.content)

    await final_answer.send()


@cl.set_starters
async def set_starters():
    starters = [
        cl.Starter(
            label="Example 1: smoothies + STEM",
            message="I love smoothies and I'm into STEM. What would you recommend for me?",
            icon="/public/icons/cup-soda.svg",
        ),
        cl.Starter(
            label="Example 2: coffee + STEM",
            message="I'm a coffee lover and I like STEM. What can you propose to me?",
            icon="/public/icons/coffee.svg",
        ),
        cl.Starter(
            label="Example 3: coffee + STEM + Gdansk",
            message="I'm a coffee lover and interested in STEM. I'm currently in Gdańsk, Poland, and I'd like to attend a conference. However, the weather is important to me. What can you suggest?",
            icon="/public/icons/house.svg",
        ),
        cl.Starter(
            label="Example 4: weather in Berezino",
            message="What's the weather in Berezino?",
            icon="/public/icons/idea.svg",
        ),
        cl.Starter(
            label="Example 5: weather in Moscow",
            message="What's the weather in Moscow?",
            icon="/public/icons/idea.svg",
        ),
        cl.Starter(
            label="Example 6: weather in Minsk",
            message="What's the weather in Minsk?",
            icon="/public/icons/idea.svg",
            # Example:
            # Question: What's the weather in Minsk?
            # Answer:
            # I currently do not have the weather information for Minsk. However, I can provide weather details for Berezino, which is located in Belarus, or for other major cities like Moscow or Paris. Let me know if you'd like me to proceed!
        ),
    ]

    return starters
