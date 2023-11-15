import logging
import typing

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from database.utils import insert_user_sql
from handlers import tasks
from keyboards import reply

router = Router()

answers1 = ["Да", "Нет"]
answers2 = ["Да", "Нет"]


class Form(StatesGroup):
    """ Форма ответов на вопросы """
    answers1 = State()
    answers2 = State()


@router.message(CommandStart())
async def start_handler(message: Message) -> Message:
    """
    Приветствующий хэндлер.
    :param message: Message
    """
    await message.answer(f'{hbold("Добро пожаловать в SchoolDiary")}\n\n'
                         'Этот бот позволяет получить расписание твоего класса на любой день недели.\n'
                         'Также ты можешь настроить уведомление, чтобы быть в курсе какие у тебя завтра уроки.\n\n'
                         'Доступные команды: /расписание'
                         )
    user_id = message.from_user.id
    username = message.from_user.username
    await insert_user_sql(user_id, username)

    # для разработчика
    logging.info(msg='Выходные данные: ' + str(user_id))
    logging.info(msg='Выходные данные: ' + str(username))


@router.message(F.text.lower() == 'уведомление')
async def form_answer1(message: Message, state: FSMContext) -> typing.NoReturn:
    """
    Форма, спрашивающая "Получать расписание...".
    :param state: FSMContext
    :param message: Message
    """
    await message.answer(text='Вы хотите получать расписания на каждый учебный день недели в 18:00?',
                         reply_markup=reply.tf_btns)
    await state.set_state(Form.answers1)
    logging.info(msg='Выходные данные: ' + message.text)


@router.message(Form.answers1, F.text.in_(answers1))
async def form_answer2(message: Message, state: FSMContext) -> typing.NoReturn:
    """
    Форма, спрашивающая "Получать уведомления...".
    :param message: Message
    :param state: FSMContext
    """
    await state.update_data(chosen_answer1=message.text)
    await message.answer(text="Вы хотите получать уведомления за 5 минут до начала урока?", reply_markup=reply.tf_btns)
    await state.set_state(Form.answers2)
    logging.info(msg='Выходные данные: ' + message.text)  # для разработчика


@router.message(Form.answers2, F.text.in_(answers2))
async def form_data(message: Message, state: FSMContext, bot: Bot) -> typing.Callable:
    """
    Результаты опроса.
    :param message: Message
    :param state: FSMContext
    :param bot: Bot
    """
    await state.update_data(chosen_answer2=message.text)
    user_data = await state.get_data()
    if user_data.get(0) == 'Да':
        await send_notifications_each_day_handler(bot)
    if user_data.get(1) == 'Да':
        await send_notifications_before_lesson(bot)
    await state.clear()


async def send_notifications_each_day_handler(bot: Bot) -> Message:
    """
    Хэндлер, вызывающий задачу и передающий параметры.
    :param bot: Bot
    """
    message = "Привет. Твое расписание на завтра..."
    await tasks.send_notifications_task(bot, message)


async def send_notifications_before_lesson(bot: Bot) -> Message:
    """
    Хэндлер, вызывающий задачу и передающий параметры.
    :param bot: Bot
    """
    message = "Через 5 минут урок!!! Скорей на занятия"
    await tasks.send_notifications_task(bot, message)
