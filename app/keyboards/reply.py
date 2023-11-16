from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

tf_btns = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да'),
            KeyboardButton(text='Нет')
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
            KeyboardButton(text='Контакты')
        ],

        [
            KeyboardButton(text='Админ-панель')
        ]
    ],
    resize_keyboard=True,
    # input_field_placeholder="Да/Нет",
    selective=True,
    # one_time_keyboard=True
)

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Изменить расписание'),
        ],

        # [
        #     KeyboardButton(text='Сделать объявление')
        # ]
    ],
    resize_keyboard=True,
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
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Отмена')
        ],
    ],
    resize_keyboard=True,
)
