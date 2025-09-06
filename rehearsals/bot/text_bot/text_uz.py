from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

flag_russia = '\U0001F1F7\U0001F1FA'
flag_uzbekistan = '\U0001F1FA\U0001F1FF'


WEB_APP_URL = 'https://bot.nextgen.uz/'


def text_main_menu_uz():

    text_main = ('👋 Salom! Eksklyuziv retseptlar botiга xush kelibsiz.\n\n'
                '🍽️ Bu yerda siz ishonchli, mazali va noodatiy taom retseptlarini topasiz — nonushtalardan tortib desertlargacha. Har bir retseptni bot orqali xarid qilish mumkin.')

    keyboard_main = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='👤 Shaxsiy kabinet')],
            [KeyboardButton(text='🍽️ Retseptlar')],
            [KeyboardButton(text='🧺 Savat')],
            [KeyboardButton(text='⚙️ Sozlamalar')],
        ],
        resize_keyboard=True,
    )

    return text_main, keyboard_main


def text_user_profile():

    text_profile = '👋 Shaxsiy kabinetга xush kelibsiz, bu yerda siz xaridlar tarixingizni va toʻlov kvitansiyalarini olishingiz mumkin'

    keyboard_profile = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📜 Xaridlar tarixi')],
            [KeyboardButton(text='💳 Toʻlov kvitansiyalari')],
            [KeyboardButton(text='🔙 Orqaga')],
        ],
        resize_keyboard=True,
    )

    return text_profile, keyboard_profile


def text_rehearsals_menu():

    text_rehearsals = 'Retseptlar katalogini oching 👇'

    keyboard_rehearsals = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🍽️ Katalog', web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

    return text_rehearsals, keyboard_rehearsals


def text_basket_menu():

    text_basket = 'Sizning savatingizni oching 👇'

    keyboard_basket = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🧺 Savat', web_app=WebAppInfo(url=WEB_APP_URL))],
        ]
    )

    return text_basket, keyboard_basket


def text_settings_menu_uz(lang):

    text_settings = 'Tilni o‘zgartirish uchun quyidagi tugmani bosing'

    if lang == 'ru':
        keyboard_settings_ru = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=f'{flag_uzbekistan} O`Z')],
                [KeyboardButton(text='🔙 Назад')],
            ],
            resize_keyboard=True
        )
        return text_settings, keyboard_settings_ru
    elif lang == 'uz':
        keyboard_settings_uz = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text=f'{flag_russia} RU')],
                [KeyboardButton(text='🔙 Orqaga')],
            ],
            resize_keyboard=True
        )
        return text_settings, keyboard_settings_uz

    return text_settings, None
