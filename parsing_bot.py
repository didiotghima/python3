from aiogram import Bot, Dispatcher, types, executor 
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os, requests, logging 

load_dotenv('.env')

bot =Bot(os.environ.get('token'))
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Здраствйте {message.from_user.full_name}, введите /news что получить новости от akipress.org")

@dp.message_handler(commands='news')
async def new(message:types.Message):
    url = 'https://akipress.org/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    news_tag = soup.find_all('a', class_='newslink')
    n = 0
    for news in news_tag:
        n += 1
        await message.answer(f"{n}) {news.text}")

executor.start_polling(dp, skip_updates=True)
