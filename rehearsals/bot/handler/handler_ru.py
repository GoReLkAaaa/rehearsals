import os


from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command


from dotenv import load_dotenv
load_dotenv()


import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rehearsals.settings')
django.setup()


from bot.sync_def.logic_handler_models_func import (
                                                    get_or_create_new_user,
                                                    get_language_user,
                                                    set_lang,
                                                    )
from bot.text_bot.text_ru import (
                                                    text_main_menu,
                                                    text_user_profile,
                                                    text_rehearsals_menu,
                                                    text_basket_menu,
                                                    text_settings_menu,
                                  )
from bot.text_bot.text_uz import text_main_menu_uz
from bot.state.state_bot import MainMenu


flag_uzbekistan = '\U0001F1FA\U0001F1FF'


def rehearsals_ru_logic_handler(router: Router):


    @router.message(Command('start'))
    async def start_message_handler(message: Message, state: FSMContext):
        user = message.from_user.full_name
        tg_id = message.from_user.id

        await get_or_create_new_user(tg_id)


        await message.answer(
            f'{user}{text_main_menu()[0]}',
            reply_markup=text_main_menu()[1]
        )
        await state.set_state(MainMenu.MAIN_WINDOW)


    @router.message(lambda message: message.text == '👤 Личный кабинет')
    async def personal_account_handler(message: Message, state: FSMContext):

        await state.set_state(MainMenu.PERSONAL_ACCOUNT)

        user = message.from_user.full_name

        await message.answer(
            f'{user}{text_user_profile()[0]}',
            reply_markup=text_user_profile()[1]
        )


    @router.message(lambda message: message.text == '📜 Истории покупок')
    async def history_buy_handler(message: Message):
        await message.answer(
            'История пуста'
        )


    @router.message(lambda message: message.text == '💳 Квитанции оплат')
    async def payment_receipts(message: Message):
        await message.answer(
            'У вас нет квитанций оплат'
        )


    @router.message(lambda message: message.text == '🍽️ Рецепты')
    async def rehearsals_menu(message: Message):

        telegram_id = message.from_user.id

        await message.answer(
            text_rehearsals_menu(telegram_id)[0],
            reply_markup=text_rehearsals_menu(telegram_id)[1]
        )


    @router.message(lambda message: message.text == '🧺 Корзина')
    async def basket_menu(message: Message):

        telegram_id = message.from_user.id

        await message.answer(
            text_basket_menu(telegram_id)[0],
            reply_markup=text_basket_menu(telegram_id)[1]
        )


    @router.message(lambda message: message.text == '⚙️ Настройки')
    async def settings_menu(message: Message, state: FSMContext):
        await state.set_state(MainMenu.SETTINGS)

        language_user = await get_language_user(message.from_user.id)
        text, keyboard = text_settings_menu(language_user)

        await message.answer(
            text,
            reply_markup=keyboard
        )


    @router.message(lambda message: message.text == f'{flag_uzbekistan} O`Z')
    async def set_language_handler(message: Message):
        user_id = message.from_user.id
        user = message.from_user.full_name

        await set_lang(user_id, 'uz')

        await message.answer(
            f'{user} {text_main_menu_uz()[0]}',
            reply_markup=text_main_menu_uz()[1]
        )


    @router.message(lambda message: message.text == '🔙 Назад')
    async def backward(message: Message, state: FSMContext):
        current_state = await state.get_state()
        user = message.from_user.full_name

        if current_state == MainMenu.PERSONAL_ACCOUNT:

            await state.set_state(MainMenu.MAIN_WINDOW)

            await message.answer(
                f'{user}{text_main_menu()[0]}',
                reply_markup=text_main_menu()[1]
            )
        elif current_state == MainMenu.REHEARSALS:
            await message.answer(
                f'{user}{text_main_menu()[0]}',
                reply_markup=text_main_menu()[1]
            )
        elif current_state == MainMenu.BASKET:
            await message.answer(
                f'{user}{text_main_menu()[0]}',
                reply_markup=text_main_menu()[1]
            )
        elif current_state == MainMenu.SETTINGS:
            await message.answer(
                f'{user}{text_main_menu()[0]}',
                reply_markup=text_main_menu()[1]
            )


