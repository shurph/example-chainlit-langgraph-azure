from app.commands.handlers.generate_a_report import command_generate_a_report
from app.commands.handlers.haha import command_haha
from app.commands.handlers.send_me_files import command_send_me_files

commands_definitions = [
    {
        "id": "Generate a report #",
        "icon": "book-text",
        "description": "Generate a report # (enter a number here to proceed)",
        "button": False,
        "persistent": False,
        "__handler": command_generate_a_report,
    },
    {
        "id": "Send me files",
        "icon": "paperclip",
        "description": "Send me files",
        "button": True,
        "persistent": False,
        "__handler": command_send_me_files,
    },
    {
        "id": "Haha!",
        "icon": "smile-plus",
        "description": "Haha!",
        "button": True,
        "persistent": True,
        "__handler": command_haha,
    },
    {
        "id": "Pure!",
        "icon": "puzzle",
        "description": "Pure!",
        "button": True,
        "persistent": True,
    },
]
