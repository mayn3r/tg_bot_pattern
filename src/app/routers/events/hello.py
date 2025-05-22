from aiogram.filters import CommandStart, Command  # noqa: F401
from aiogram.types import Message
from aiogram import Router, F  # noqa: F401


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    """ /start """
    
    await message.answer("Hello")
    