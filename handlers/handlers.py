import aiosqlite
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Bot
from aiogram.utils.markdown import hbold

from keyboards import reply
from database.utils import insert_user_sql
from handlers import tasks

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
    username = message.from_user.username
    await insert_user_sql(user_id, username)


# async def noon_print(bot: Bot):
#     async with aiosqlite.connect('schoolDiary.db') as db:
#         async with db.execute("""SELECT user_id FROM users;""") as cursor:
#             async for users in cursor:
#                 for user in list(users):
#                     await bot.send_message(user, text='lalala')

# async def noon_print(bot: Bot):
#     user_id_list = await get_users_sql()
#     async for user in user_id_list:
#         await bot.send_message(user, text='lalala')

async def send_notifications_handler(bot: Bot):
    message = 'Привет. Твое расписание на завтра...'
    await tasks.send_notifications_task(bot, message)
