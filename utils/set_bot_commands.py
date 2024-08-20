from aiogram import types

from loader import bot


async def set_default_commands():
    commands = [
            types.BotCommand(command="start", description="Launch the bot"),
            types.BotCommand(command="help", description="help"),
        ]
    await bot.set_my_commands(
        commands, types.BotCommandScopeDefault()
    )
