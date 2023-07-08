from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
import os, logging, aioschedule, asyncio

load_dotenv('.env')

bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer("Hello World")

async def send_message2():
    chat = -988585481
    message = "from aiogram import load_dotenv"
    await bot.send_message(chat, message)

async def send_message():
    chat = -988585481
    message = "SPAM CHAT"
    await bot.send_message(chat, message)

async def scheduler():
    aioschedule.every(1).seconds.do(send_message)
    aioschedule.every(1).seconds.do(send_message2)
    aioschedule.every().wednesday.at("19:47").do(send_message)
    while True:
        # await asyncio.sleep()
        await aioschedule.run_pending()

async def on_startup(_):
    asyncio.create_task(scheduler())

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)