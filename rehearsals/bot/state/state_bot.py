"""
    Модуль создания состояния для бота.

    - Создание State

    Импортируемые зависимости:
        - State, StatesGroup

"""

from aiogram.fsm.state import State, StatesGroup


# State состояние для главного меню
class MainMenu(StatesGroup):
    MAIN_WINDOW = State()
    PERSONAL_ACCOUNT = State()
    REHEARSALS = State()
    BASKET = State()
    SETTINGS = State()