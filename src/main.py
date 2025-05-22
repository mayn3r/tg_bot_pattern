import asyncio
import config  # noqa: F401

from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tortoise import Tortoise, run_async

from core.bot import bot, dp
from app.schedulers import add_schedulers
from app.routers import events, callbacks
from app.middlewares import middlewares


scheduler = AsyncIOScheduler()


async def init_db() -> None:
    """Инициализация базы данных"""
    
    logger.debug('Инициализация базы данных..')
    
    await Tortoise.init(
        db_url="sqlite://database/users.db",
        modules={
            'models': ['app.db_models']
        }
    )
    
    await Tortoise.generate_schemas()
    logger.info('Tortoise inited!')



async def main() -> None:
    scheduler.start()
    add_schedulers()
    
    # await bot.delete_webhook(drop_pending_updates=True)
    # logger.debug("Webhook has been deleted")
    
    # Add middleware
    for middleware in middlewares:
        dp.message.middleware(middleware())
    
    dp.include_routers(*events.routers, *callbacks.routers)
        

    logger.debug('Bot started!')
    await dp.start_polling(bot)



if __name__ == "__main__":
    run_async(init_db())
    asyncio.run(main())