from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb_select_mode = [
    [
        KeyboardButton("Музыка"), KeyboardButton("Музыка по таймкодам"),
    ],
    [
        KeyboardButton("Видео")
    ]
]

kb_start_download = [
    [
        KeyboardButton("Завершить и загрузить")
    ]
]

select_mode_keyboard = ReplyKeyboardMarkup(input_field_placeholder="ТИП ЗАГРУЗКИ",
                                           resize_keyboard=True,
                                           keyboard=kb_select_mode)
start_download_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb_start_download)
