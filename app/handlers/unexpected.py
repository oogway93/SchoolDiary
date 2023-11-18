from aiogram import Router
from aiogram.types import Message

from app.keyboards import reply as kb

router = Router()


@router.message()
async def unexpected_message_handler(message: Message):
    """
    Хэндлер, вызывающийся при непонятных боту сообщениях.
    :param message: Message
    """
    await message.reply(
        text='Я вас не понял. \n\nВыберите одну из доступных команд:',
        reply_markup=kb.main
    )
