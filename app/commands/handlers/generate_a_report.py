import chainlit as cl

from app.commands.schemas.base import CommandResponse


async def command_generate_a_report(msg) -> CommandResponse:
    answer = cl.Message(content="")
    content = f"Generating report for {msg.content}..."
    await answer.stream_token(content)
    await answer.send()
    return CommandResponse(need_to_interrupt=True)
