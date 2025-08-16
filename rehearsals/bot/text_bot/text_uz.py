from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


flag_russia = '\U0001F1F7\U0001F1FA'
flag_uzbekistan = '\U0001F1FA\U0001F1FF'


def text_main_menu_uz():

    text_main = ('👋 Salom! Eksklyuziv retseptlar bilan botga xush kelibsiz.\n\n'
                 '🍽️ Bu yerda siz ishonchli, mazali va original taom retseptlarini topasiz — nonushtalardan tortib desertlargacha. Har bir retseptni bot orqali sotib olishingiz mumkin.')

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

    text_profile = '👋 Shaxsiy kabinetingizga xush kelibsiz, bu yerda siz xaridlar tarixini va toʻlov kvitansiyalarini olishingiz mumkin'

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

    text_rehearsals = 'Quyidagi kerakli toifani tanlang'

    keyboard_rehearsals = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🥣 Birinchi taomlar')],
            [KeyboardButton(text='🍲 Ikkinchi taomlar')],
            [KeyboardButton(text='🍰 Desertlar')],
            [KeyboardButton(text='🍹 Ichimliklar')],
            [KeyboardButton(text='🔙 Orqaga')]
        ]
    )

    return text_rehearsals, keyboard_rehearsals


def product_keyboard(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Savatga qoʻshish", callback_data=f"addcart_{product_id}")]
        ]
    )


def next_page_keyboard(category, page, total):
    if (page + 1) * 3 < total:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="➡ Keyingi", callback_data=f"next_{category}_{page+1}")]
            ]
        )
    return None


def remove_button(product_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Oʻchirish", callback_data=f"delcart_{product_id}")]
        ]
    )


def text_basket_menu(price):

    text_basket = (f'Savatingiz\n'
                   f'Narxi: {price} soʻm')

    keyboard_basket = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='💵 Toʻlash')],
            [KeyboardButton(text='🔙 Orqaga')],
        ],
        resize_keyboard=True,
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
