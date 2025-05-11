import asyncio

import chainlit as cl

from app.commands.schemas.base import CommandResponse


async def command_haha(msg: cl.Message) -> CommandResponse:
    answer = cl.Message(content="")
    await answer.stream_token("Want to hear")
    await asyncio.sleep(0.14)
    await answer.stream_token(" a")
    await asyncio.sleep(0.5)
    await answer.stream_token(" joke")
    await asyncio.sleep(0.14)
    await answer.stream_token(f" about {msg.content}?")
    await asyncio.sleep(0.14)
    await answer.send()
    await asyncio.sleep(0.14)
    await answer.stream_token("\nHaha!")
    await answer.send()
    return CommandResponse(need_to_interrupt=True)
