import chainlit as cl

from app.commands.schemas.base import CommandProcessorResponse


class CommandsProcessor:
    def __init__(self, router):
        self.router = router

    async def process(self, msg: cl.Message) -> CommandProcessorResponse:
        if msg.command in self.router:
            return await self.router[msg.command](msg)
        else:
            return CommandProcessorResponse(False, None, [])


def register_commands(commands_definitions):
    commands = []
    router = {}
    for command in commands_definitions:
        command_copy = command.copy()
        commands.append(command_copy)
        if "__handler" in command_copy:
            router[command["id"]] = command_copy["__handler"]
            del command_copy["__handler"]
    return commands, router
