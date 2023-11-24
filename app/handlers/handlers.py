import logging
import typing
from datetime import datetime

import aiosqlite
from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command

from app.handlers import tasks
from app.keyboards import reply as kb
from app.database import utils

router = Router()

answers1 = ["Да", "Нет"]
answers2 = ["Да", "Нет"]

available_classes = ['10а', '10б', '9а', '9б', '9в', '9г']
available_days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']


class Form(StatesGroup):
    """ Форма ответов на вопросы """
    answers1 = State()
    answers2 = State()
    choosing_class = State()


class Schedule(StatesGroup):
    """ Расписание  """
    choosing_class = State()
    choosing_day = State()


@router.message(CommandStart())
async def start_handler(message: Message) -> Message:
    """
    Приветствующий хэндлер.
    :param message: Message
    """
    await message.answer(f'{hbold("Добро пожаловать в SchoolDiary")}\n\n'
                         'Этот бот позволяет получить расписание твоего класса на любой день недели.\n'
                         'Также ты можешь настроить уведомление, чтобы быть в курсе какие у тебя завтра уроки.\n\n'
                         f'{hbold("Доступные команды:")} \n\nРасписание \nКонтакты \nАдмин-панель \nУведомления',
                         reply_markup=kb.main
                         )
    user_id = message.from_user.id
    username = message.from_user.username
    await utils.insert_user_sql(user_id, username)

    # для разработчика
    logging.info(msg='Выходные данные: ' + str(user_id))
    logging.info(msg='Выходные данные: ' + str(username))


@router.message(F.text.lower() == 'уведомления')
async def form_answer1(message: Message, state: FSMContext) -> typing.NoReturn:
    """
    Форма, спрашивающая "Получать расписание...".
    :param state: FSMContext
    :param message: Message
    """
    await message.answer(text='Вы хотите получать расписания следующего учебного дня в 18:00?',
                         reply_markup=kb.tf_btns)
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
    await message.answer(text="Вы хотите получать расписания на текущий учебный день в 7:00?", reply_markup=kb.tf_btns)
    await state.set_state(Form.answers2)
    logging.info(msg='Выходные данные: ' + message.text)  # для разработчика


@router.message(Form.answers2, F.text.in_(answers2))
async def form_choosing_classes(message: Message, state: FSMContext):
    """
    Хэндлер, реализуюший выбор класса
    :param message: Message
    :param state: FSMContext
    """
    await state.update_data(chosen_answer2=message.text)
    await message.answer(
        text='Выберите свой класс для отправки расписания:',
        reply_markup=kb.classes
    )
    await state.set_state(Form.choosing_class)


@router.message(Form.choosing_class, F.text.lower().in_(available_classes))
async def form_data(message: Message, state: FSMContext) -> typing.Callable:
    """
    Результаты опроса.
    :param message: Message
    :param state: FSMContext
    """
    user_id = message.from_user.id
    await state.update_data(chosen_class=message.text)
    user_data = await state.get_data()
    if user_data['chosen_answer1'] == 'Да':
        await utils.insert_class_and_isActive_sql(user_id, user_data['chosen_class'], 1)
    elif user_data['chosen_answer1'] == 'Нет':
        await utils.insert_class_and_isActive_sql(user_id, user_data['chosen_class'], 0)

    if user_data['chosen_answer2'] == 'Да':
        await utils.insert_isActive2_sql(user_id, 1)
    elif user_data['chosen_answer2'] == 'Нет':
        await utils.insert_isActive2_sql(user_id, 0)

    await message.answer("Сохранено.", reply_markup=kb.main)
    await state.clear()


async def send_notifications_each_day_18_handler(bot: Bot) -> Message:
    """
    Хэндлер, вызывающий задачу и передающий параметры в 18:00.
    :param bot: Bot
    """
    async with aiosqlite.connect('schoolDiary.db') as db:
        async with db.execute("""SELECT user_id, class FROM users WHERE is_active=?;""", (1,)) as cursor:
            async for query in cursor:
                user_id, class_name = query
                weekdays = {1: 'понедельник', 2: 'вторник', 3: 'среда', 4: 'четверг', 5: 'пятница', 6: 'суббота'}
                data = utils.collection.find_one({"class_name": class_name})

                day = datetime.now().isoweekday()
                day_now = ''
                if day <= 5:
                    day_now = weekdays.get(day + 1, 'Error')
                if day == 7:
                    day_now = weekdays.get(1)
                get_schedule = data['schedule'][day_now]
                counter = 0
                message = ''

                for subject in get_schedule:
                    counter += 1
                    message += str(counter) + ') '
                    message += subject.capitalize() + '\n'
                await tasks.send_notifications_18_task(bot, message, user_id)


async def send_notifications_each_day_7_handler(bot: Bot) -> Message:
    """
    Хэндлер, вызывающий задачу и передающий параметры в 7:00.
    :param bot: Bot
    """
    async with aiosqlite.connect('schoolDiary.db') as db:
        async with db.execute("""SELECT user_id, class FROM users WHERE is_active2=?;""", (1,)) as cursor:
            async for query in cursor:
                user_id, class_name = query
                weekdays = {1: 'понедельник', 2: 'вторник', 3: 'среда', 4: 'четверг', 5: 'пятница', 6: 'суббота'}
                data = utils.collection.find_one({"class_name": class_name})

                day = datetime.now().isoweekday()
                day_now = ''
                if day <= 6:
                    day_now = weekdays.get(day)
                get_schedule = data['schedule'][day_now]
                counter = 0
                message = ''

                for subject in get_schedule:
                    counter += 1
                    message += str(counter) + ') '
                    message += subject.capitalize() + '\n'
                await tasks.send_notifications_7_task(bot, message, user_id)


@router.message(F.text.lower() == 'контакты')
async def contacts_handler(message: Message):
    """
    Хэндлер контакты
    :param message: Message
    """
    await message.answer(
        text='По всем вопросам и предложениям:\n\n@Ensp1r\n@kiddcoding',
        reply_markup=kb.main
    )


@router.message(F.text.lower() == 'расписание')
async def schedule_handler(message: Message, state: FSMContext):
    """
    Хэндлер, реализующий расписание
    :param message: Message
    :param state: FSMContext
    """
    await message.answer(
        text='Выберите свой класс:',
        reply_markup=kb.classes
    )

    await state.set_state(Schedule.choosing_class)


@router.message(Schedule.choosing_class, F.text.lower().in_(available_classes))
async def class_chosen_handler(message: Message, state: FSMContext):
    """
    Хэндлер, реализуюший выбор класса
    :param message: Message
    :param state: FSMContext
    """
    await state.update_data(chosen_class=message.text.upper())
    await message.answer(
        text='Выберите день недели:',
        reply_markup=kb.days
    )

    await state.set_state(Schedule.choosing_day)


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cancel_handler(message: Message, state: FSMContext):
    """
    Хэндлер, реализующий отмену действий.
    :param message: Message
    :param state: FSMContext
    """
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=kb.main
    )


@router.message(Schedule.choosing_class)
async def class_chosen_incorrectly_handler(message: Message):
    """
    Хэндлер, реализующий выбор класса при неправильном вводе
    :param message: Message
    """
    await message.answer(
        text='Извините, но такого класса не существует в нашей школе.',
        reply_markup=kb.classes
    )


@router.message(Schedule.choosing_day, F.text.lower().in_(available_days))
async def day_chosen_handler(message: Message, state: FSMContext):
    """
    Хэндлер, реализующий выбор дня недели
    :param message: Message
    :param state: FSMContext
    """
    user_data = await state.get_data()
    chosen_class = user_data['chosen_class']
    chosen_day = message.text.lower()

    data = utils.collection.find_one({"class_name": chosen_class})

    get_schedule = data['schedule'][chosen_day]

    counter = 0
    result = ''

    for subject in get_schedule:
        counter += 1
        result += str(counter) + ') '
        result += subject.capitalize() + '\n'

    await message.answer(
        text=f'Ваше на расписание на {message.text}: \n\n{result}',
        reply_markup=kb.main
    )

    await state.clear()


@router.message(Schedule.choosing_day)
async def day_chosen_incorrectly_handler(message: Message):
    """
    Хэндлер, реализующий выбор дня недели при неправильном вводе.
    :param message: Message
    """
    await message.answer(
        text='Извините, но в данный день не проводятся уроки.',
        reply_markup=kb.days
    )
