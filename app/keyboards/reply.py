from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tf_btns = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да'),
            KeyboardButton(text='Нет')
        ],
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Да/Нет",
    selective=True,
    one_time_keyboard=True
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Расписание'),
        ],

        [
            KeyboardButton(text='Уведомления'),
            KeyboardButton(text='Контакты')
        ],

        [
            KeyboardButton(text='Админ-панель')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить расписание'),
        ],

        [
            KeyboardButton(text='Сделать объявление')
        ],
        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)

classes = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='10А'),
            KeyboardButton(text='10Б')
        ],

        [
            KeyboardButton(text='9А'),
            KeyboardButton(text='9Б')
        ],

        [
            KeyboardButton(text='9В'),
            KeyboardButton(text='9Г')
        ],

        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)

days = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Понедельник'),
            KeyboardButton(text='Вторник')
        ],

        [
            KeyboardButton(text='Среда'),
            KeyboardButton(text='Четверг')
        ],

        [
            KeyboardButton(text='Пятница'),
            KeyboardButton(text='Суббота')
        ],

        [
            KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отмена')
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)
