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

from bot.sync_def.logic_handler_models_func import (get_or_create_new_user,
                                                    get_product,
                                                    get_basket_items,
                                                    add_to_cart,
                                                    remove_from_cart,
                                                    get_language_user,
                                                    set_lang,
                                                    get_products_by_category,
                                                    get_products_count
                                                    )
from bot.text_bot.text_uz import (
                                                        text_main_menu_uz,
                                                        text_user_profile,
                                                        text_rehearsals_menu,
                                                        text_basket_menu,
                                                        text_settings_menu_uz,
                                                    )
from bot.text_bot.text_ru import text_main_menu
from bot.state.state_bot import MainMenu


flag_russia = '\U0001F1F7\U0001F1FA'


def rehearsals_uz_logic_handler(router: Router):

    @router.message(Command('start'))
    async def start_message_handler(message: Message, state: FSMContext):
        user = message.from_user.full_name
        tg_id = message.from_user.id

        await get_or_create_new_user(tg_id)

        await message.answer(
            f'{user} {text_main_menu_uz()[0]}',
            reply_markup=text_main_menu_uz()[1]
        )
        await state.set_state(MainMenu.MAIN_WINDOW)

    @router.message(lambda message: message.text == '👤 Shaxsiy kabinet')
    async def personal_account_handler(message: Message, state: FSMContext):

        await state.set_state(MainMenu.PERSONAL_ACCOUNT)

        user = message.from_user.full_name

        await message.answer(
            f'{user} {text_user_profile()[0]}',
            reply_markup=text_user_profile()[1]
        )

    @router.message(lambda message: message.text == '🍽️ Retseptlar')
    async def rehearsals_menu(message: Message, state: FSMContext):

        await message.answer(
            text_rehearsals_menu()[0],
            reply_markup=text_rehearsals_menu()[1]
        )

        await state.set_state(MainMenu.REHEARSALS)

    @router.message(lambda message: message.text == '🧺 Savat')
    async def basket_menu(message: Message, state: FSMContext):
        await state.set_state(MainMenu.BASKET)

        basket = await get_basket_items(message.from_user.id)
        if not basket:
            await message.answer(
                'Savat bo‘sh'
            )
        else:
            await message.answer(
                f'{basket}{text_basket_menu()[0]}',
                reply_markup=text_basket_menu()[1]
            )

    @router.message(lambda message: message.text == '⚙️ Sozlamalar')
    async def settings_menu(message: Message, state: FSMContext):
        await state.set_state(MainMenu.SETTINGS)

        language_user = await get_language_user(message.from_user.id)
        text, keyboard = text_settings_menu_uz(language_user)

        await message.answer(text, reply_markup=keyboard)


    @router.message(lambda message: message.text == f'{flag_russia} RU')
    async def set_language_handler_uz(message: Message):
        user_id = message.from_user.id
        user = message.from_user.full_name

        await set_lang(user_id, 'ru')

        await message.answer(
            f'{user} {text_main_menu()[0]}',
            reply_markup=text_main_menu()[1]
        )

    @router.message(lambda message: message.text == '🔙 Orqaga')
    async def backward(message: Message, state: FSMContext):
        current_state = await state.get_state()
        user = message.from_user.full_name

        if current_state == MainMenu.PERSONAL_ACCOUNT:
            await state.set_state(MainMenu.MAIN_WINDOW)
            await message.answer(
                f'{user} {text_main_menu_uz()[0]}',
                reply_markup=text_main_menu_uz()[1]
            )
        elif current_state == MainMenu.REHEARSALS:
            await message.answer(
                f'{user} {text_main_menu_uz()[0]}',
                reply_markup=text_main_menu_uz()[1]
            )
        elif current_state == MainMenu.BASKET:
            await message.answer(
                f'{user} {text_main_menu_uz()[0]}',
                reply_markup=text_main_menu_uz()[1]
            )
        elif current_state == MainMenu.SETTINGS:
            await message.answer(
                f'{user} {text_main_menu_uz()[0]}',
                reply_markup=text_main_menu_uz()[1]
            )
