from app.database import utils
from config import ADMIN_ID
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.keyboards import reply as kb
from config import ADMIN_ID

available_classes = ['10а', '10б', '9а', '9б', '9в', '9г']
available_days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']


class ScheduleAdmin(StatesGroup):
    admin_choosing_class = State()
    admin_choosing_day = State()
    admin_changing_schedule = State()


router = Router()


@router.message(F.text.lower() == 'админ-панель')
async def admin_panel_handler(message: Message):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer(
            text='Добро пожаловать в админ-панель. \n\nВыберите действие:',
            reply_markup=kb.admin_panel
        )

    else:
        await message.reply(
            text='У вас недостаточно прав. \n\nВыберите одну из доступных команд:',
            reply_markup=kb.main
        )


@router.message(F.text.lower() == 'изменить расписание')
async def schedule_handler(message: Message, state: FSMContext):
    if message.from_user.id == int(ADMIN_ID):
        await message.answer(
            text='Выберите класс:',
            reply_markup=kb.classes
        )

        await state.set_state(ScheduleAdmin.admin_choosing_class)

    else:
        await message.reply(
            text='Я вас не понял. \n\nВыберите одну из доступных команд:',
            reply_markup=kb.main
        )


@router.message(ScheduleAdmin.admin_choosing_class, F.text.lower().in_(available_classes))
async def admin_class_chosen_handler(message: Message, state: FSMContext):
    await state.update_data(chosen_class=message.text.upper())
    await message.answer(
        text='Выберите день недели:',
        reply_markup=kb.days
    )

    await state.set_state(ScheduleAdmin.admin_choosing_day)


@router.message(ScheduleAdmin.admin_choosing_class)
async def class_chosen_incorrectly_handler(message: Message):
    await message.answer(
        text='Извините, но такого класса не существует в нашей школе.',
        reply_markup=kb.classes
    )


@router.message(ScheduleAdmin.admin_choosing_day, F.text.lower().in_(available_days))
async def admin_day_chosen_handler(message: Message, state: FSMContext):
    await state.update_data(chosen_day=message.text.lower())
    await message.answer(
        text=f'Введите новое расписание: \n\n{hbold("Каждый новый предмет вводите после пробела")}.\n{hbold("Учтите, что порядок предметов очень важен.")}\n\n{hbold("Пример ввода: информатика алгебра биология")}',
        reply_markup=kb.cancel
    )

    await state.set_state(ScheduleAdmin.admin_changing_schedule)


@router.message(ScheduleAdmin.admin_choosing_day)
async def day_chosen_incorrectly(message: Message):
    await message.answer(
        text='Извините, но в данный день не проводятся уроки.',
        reply_markup=kb.days
    )


@router.message(ScheduleAdmin.admin_changing_schedule, F.text)
async def admin_schedule_changed(message: Message, state: FSMContext):
    user_data = await state.get_data()
    chosen_class = user_data['chosen_class']
    chosen_day = user_data['chosen_day']

    utils.update_schedule(chosen_class, chosen_day, message.text.lower())

    await message.answer(
        text=f'Расписание в(о) {hbold(chosen_day)} у {hbold(chosen_class)} успешно изменено.',
        reply_markup=kb.main
    )

    await state.clear()
