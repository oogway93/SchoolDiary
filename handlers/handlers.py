from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Bot
from aiogram.utils.markdown import hbold

from keyboards import reply

router = Router()

# sending = False


#
# @router.message(F.text.lower() == 'уведомление')
# async def send_schedule_on_time_handler(messsage: Message) -> Message:
#     await messsage.answer(text='Вы хотите получать расписания на каждый день недели в 18:00?',
#                           reply_markup=reply.tf_btns)
#     if messsage.text == 'Да':
#         global sending
#         sending = True
#         await messsage.answer(text='Спасибо!')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'{hbold("Добро пожаловать в SchoolDiary")}\n\n'
                         'Этот бот позволяет получить расписание твоего класса на любой день недели.\n'
                         'Также ты можешь настроить уведомление, чтобы быть в курсе какие у тебя завтра уроки.\n\n'
                         'Доступные команды: /расписание'
                         )
    user_id = message.from_user.id


async def noon_print():
    print('sadijaduhsadsa')
