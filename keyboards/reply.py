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
    selective=True
)
