from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

flag_russia = '\U0001F1F7\U0001F1FA'
flag_uzbekistan = '\U0001F1FA\U0001F1FF'


WEB_APP_URL = ''


def text_main_menu():

    text_main = ('👋 Привет! Добро пожаловать в бот с эксклюзивными рецептами.\n\n'
                '🍽️ Здесь ты найдёшь проверенные, вкусные и оригинальные рецепты блюд — от завтраков до десертов. Каждый рецепт доступен для покупки прямо в боте.')

    keyboard_main = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='👤 Личный кабинет')],
            [KeyboardButton(text='🍽️ Рецепты')],
            [KeyboardButton(text='🧺 Корзина')],
            [KeyboardButton(text='⚙️ Настройки')],
        ],
        resize_keyboard=True,
    )

    return text_main, keyboard_main


def text_user_profile():

    text_profile = '👋 Добро пожаловать в личный кабинет, здесь вы можете получить свою историю покупок и квитанции оплат'

    keyboard_profile = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📜 Истории покупок')],
            [KeyboardButton(text='💳 Квитанции оплат')],
            [KeyboardButton(text='🔙 Назад')],
        ],
        resize_keyboard=True,
    )

    return text_profile, keyboard_profile


def text_rehearsals_menu():

    text_rehearsals = 'Открыть каталог рецептов 👇'

    keyboard_rehearsals = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🍽️ Каталог', web_app=WebAppInfo(url=WEB_APP_URL))]
        ]
    )

    return text_rehearsals, keyboard_rehearsals


def text_basket_menu():

    text_basket = 'Открыть вашу корзину 👇'

    keyboard_basket = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🧺 Корзина', web_app=WebAppInfo(url=WEB_APP_URL))],
        ]
    )

    return text_basket, keyboard_basket


def text_settings_menu(lang):

    text_settings = 'Для смены языка нажмите на кнопку ниже'

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
                [KeyboardButton(text=f'{flag_russia} РУ')],
                [KeyboardButton(text='🔙 Orqaga')],
            ],
            resize_keyboard=True
        )
        return text_settings, keyboard_settings_uz

    return  text_settings, None
