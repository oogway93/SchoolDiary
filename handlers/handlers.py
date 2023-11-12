from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold

from database.utils import insert_user_sql
from handlers import tasks
from keyboards import reply

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f'{hbold("Добро пожаловать в SchoolDiary")}\n\n'
                         'Этот бот позволяет получить расписание твоего класса на любой день недели.\n'
                         'Также ты можешь настроить уведомление, чтобы быть в курсе какие у тебя завтра уроки.\n\n'
                         'Доступные команды: /расписание'
                         )
    user_id = message.from_user.id
    username = message.from_user.username
    await insert_user_sql(user_id, username)


@router.message(F.text.lower() == 'уведомление')
async def send_schedule_on_time_handler(message: Message, bot: Bot) -> Message:
    """
    Хэндлер, спрашивающий "Получать расписание...'
    :param message: Message
    :param bot: Bot
    """
    await message.answer(text='Вы хотите получать расписания на каждый учебный день недели в 18:00?',
                         reply_markup=reply.tf_btns)
    if message.text == "Да":
        await message.delete()
        await send_notifications_each_day_handler(bot)

    await message.answer(text="Вы хотите получать уведомления за 5 минут до начала урока?", reply_markup=reply.tf_btns)
    if message.text == "Да":
        await message.delete()
        await send_notifications_before_lesson(bot)


async def send_notifications_each_day_handler(bot: Bot):
    """
    Хэндлер, вызывающий задачу и передающий параметры.
    :param bot: Bot
    """
    message = "Привет. Твое расписание на завтра..."
    await tasks.send_notifications_task(bot, message)


async def send_notifications_before_lesson(bot: Bot):
    """
    Хэндлер, вызывающий задачу и передающий параметры.
    :param bot: Bot
    """
    message = "Через 5 минут урок!!! Скорей на занятия"
    await tasks.send_notifications_task(bot, message)

# async def notifications(bot: Bot):
#     """
#     Фабрика хэндлеров с оповещениями
#     :param bot: Bot
#     """
#     await send_notifications_handler(bot)
