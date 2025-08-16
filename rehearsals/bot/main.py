import asyncio
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv
load_dotenv()

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rehearsals.settings')
django.setup()

from config.config_bot import bot, dp
from router.router_bot import main_router


dp.include_router(main_router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())