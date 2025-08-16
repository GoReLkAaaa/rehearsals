from aiogram import Router

from bot.handler.handler_ru import rehearsals_ru_logic_handler
from bot.handler.handler_uz import rehearsals_uz_logic_handler


main_router = Router()


rehearsals_ru_logic_handler(main_router)
rehearsals_uz_logic_handler(main_router)