import os
import logging
import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.methods import TelegramMethod
from nats.aio.client import Client
from aiogram import Bot, Dispatcher, Router, F, types

from aiogram_nats import create_nats_fsm_storage

TOKEN = os.getenv("BOT_TOKEN")

router = Router()


@router.message(F.text)
async def process_text_message(message: types.Message, state: FSMContext) -> TelegramMethod:
    data = await state.get_data()
    count = data.get("count", 0) + 1
    await state.update_data(count=count)

    return message.reply(f"You have sent {count} messages. \nYour message: {message.text}")


async def main():
    # You have to create stream and consumer manually
    # With following buckets:
    # - fsm_states_aiogram
    # - fsm_data_aiogram
    nc = Client()
    await nc.connect("nats://localhost:4222")
    storage = await create_nats_fsm_storage(nc)

    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    bot = Bot(TOKEN)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
