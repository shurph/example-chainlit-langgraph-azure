import chainlit as cl

from app.commands.schemas.base import CommandResponse


async def command_send_me_files(msg) -> CommandResponse:
    answer = cl.Message(content="")
    content = "Sending files..."

    await answer.stream_token(content)
    filename = f"report_{msg.content}.txt"
    await send_file("./public/reports/report.txt", filename)

    await answer.send()
    return CommandResponse(need_to_interrupt=True)


async def send_file(file_path: str, file_name: str):
    elements = [
        cl.File(
            name=file_name,
            path=file_path,
            display="inline",
        ),
    ]

    await cl.Message(content="Here is the file you requested", elements=elements).send()
