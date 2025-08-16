import os


from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from dotenv import load_dotenv

from mainapp.models import Product

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
from bot.text_bot.text_ru import (text_main_menu,
                                  text_user_profile,
                                  text_rehearsals_menu,
                                  product_keyboard,
                                  next_page_keyboard,
                                  remove_button,
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
    async def rehearsals_menu(message: Message, state: FSMContext):

        await message.answer(
            text_rehearsals_menu()[0],
            reply_markup=text_rehearsals_menu()[1]
        )

        await state.set_state(MainMenu.REHEARSALS)


    # Обработка выбора категории
    @router.message(F.text.in_(['🥣 Первые блюда', '🍲 Вторые блюда', '🍰 Десерты', '🍹 Напитки']))
    async def category_handler(message: Message):
        category_map = {
            '🥣 Первые блюда': 'first',
            '🍲 Вторые блюда': 'second',
            '🍰 Десерты': 'dessert',
            '🍹 Напитки': 'drink'
        }
        category = category_map[message.text]

        products = await get_products_by_category(category, 0, 3)
        total_count = await get_products_count(category)

        if not products:
            await message.answer("В этой категории пока нет блюд.")
            return


        for product in products:

            if product.image:
                image_path = product.image.path
                photo = FSInputFile(image_path)

                await message.answer_photo(
                    photo=photo,
                    caption=f"🍽 {product.name_ru}\n{product.description_ru}\n Цена рецепта - {product.price} сумм",
                    reply_markup=product_keyboard(product.id)
                )
            else:
                await message.answer(
                    f"🍽 {product.name_ru}\n{product.description_ru}\n Цена рецепта - {product.price} сумм",
                    reply_markup=product_keyboard(product.id)
                )

        # Кнопка "Далее"
        next_kb = next_page_keyboard(category, 0, total_count)
        if next_kb:
            await message.answer(
                "Показать ещё блюда:",
                reply_markup=next_kb
            )


    # Пагинация
    @router.callback_query(F.data.startswith("next_"))
    async def next_page_handler(callback: CallbackQuery):
        _, category, page_str = callback.data.split("_")
        page = int(page_str)

        products = await get_products_by_category(category, page * 3, 3)
        total_count = await get_products_count(category)

        for product in products:

            if product.image:
                image_path = product.image.path
                photo = FSInputFile(image_path)

                await callback.message.answer_photo(
                    photo=photo,
                    caption=f"🍽 {product.name_ru}\n{product.description_ru}\n Цена рецепта - {product.price} сумм",
                    reply_markup=product_keyboard(product.id)
                )
            else:
                await callback.message.answer(
                    f"🍽 {product.name_ru}\n{product.description_ru}\n  Цена рецепта - {product.price} сумм",
                    reply_markup=product_keyboard(product.id)
                )

        next_kb = next_page_keyboard(category, page, total_count)

        if next_kb:
            await callback.message.answer(
                "Показать ещё блюда:",
                reply_markup=next_kb
            )

        await callback.answer()


    @router.callback_query(F.data.startswith("addcart_"))
    async def add_to_cart_handler(callback: CallbackQuery):
        product_id = int(callback.data.split("_")[1])

        try:
            user = await get_or_create_new_user(callback.from_user.id)
            product = await get_product(product_id)

        except Product.DoesNotExist:
            await callback.answer(
                "Товар не найден",
                show_alert=True
            )
            return

        except Exception as e:
            await callback.answer(
                "Ошибка при добавлении в корзину",
                show_alert=True
            )
            return

        added = await add_to_cart(user, product)

        if added:
            await callback.message.edit_reply_markup(
                reply_markup=remove_button(product_id)
            )
            await callback.answer(
                "Товар добавлен в корзину ✅",
                show_alert=True
            )
        else:
            await callback.answer(
                "Этот товар уже в корзине",
                show_alert=True
            )


    @router.callback_query(F.data.startswith("delcart_"))
    async def remove_from_cart_handler(callback: CallbackQuery):
        product_id = int(callback.data.split("_")[1])

        try:
            user = await get_or_create_new_user(callback.from_user.id)
            product = await get_product(product_id)

        except Product.DoesNotExist:
            await callback.answer(
                "Товар не найден",
                show_alert=True
            )
            return

        removed = await remove_from_cart(user, product)


        if removed:
            await callback.message.edit_reply_markup(
                reply_markup=product_keyboard(product_id)
            )
            await callback.answer(
                "Товар удалён из корзины ❌",
                show_alert=True
            )
        else:
            await callback.answer(
                "Этого товара нет в корзине",
                show_alert=True
            )


    @router.message(lambda message: message.text == '🧺 Корзина')
    async def basket_menu(message: Message, state: FSMContext):
        await state.set_state(MainMenu.BASKET)

        items  = await get_basket_items(message.from_user.id)
        price_product = []

        if not items:
            await message.answer("Ваша корзина пуста 🛒")
            return

        for item in items:
            product = item.product
            await message.answer(
                f"🍽 {product.name_ru}\n Цена рецепта {product.price} сумм",
                reply_markup=remove_button(product.id)
            )
            price_product.append(product.price)
        await message.answer(
            text_basket_menu(sum(price_product))[0],
            reply_markup=text_basket_menu(sum(price_product))[1]
        )


    @router.callback_query(F.data.startswith("delcart_"))
    async def remove_from_basket(callback: CallbackQuery):
        product_id = int(callback.data.split("_")[1])

        user = await get_or_create_new_user(callback.from_user.id)
        product = await get_product(product_id)

        removed = await remove_from_cart(user, product)

        if not removed:
            await callback.answer("Товара нет в корзине", show_alert=True)
            return

        # Получаем актуальный список товаров
        items = await get_basket_items(callback.from_user.id)

        if not items:
            await callback.message.edit_text("🛒 Ваша корзина пуста")
            return

        # Собираем обновлённый текст и кнопки
        text = "🛒 Ваша корзина:\n\n"
        keyboard = InlineKeyboardBuilder()

        for item in items:
            product = item.product
            text += f"• {product.name_ru} — {product.price} сум\n"
            keyboard.button(
                text=f"❌ Удалить {product.name_ru}",
                callback_data=f"delcart_{product.id}"
            )

        keyboard.adjust(1)

        # Обновляем текущее сообщение
        await callback.message.edit_text(
            text,
            reply_markup=keyboard.as_markup()
        )

        await callback.answer("Товар удалён из корзины ❌")


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


