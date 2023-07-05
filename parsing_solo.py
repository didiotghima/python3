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
    await message.answer(f"Здраствйте {message.from_user.full_name}, введите /currency что получить курсы на волюты https://www.nbkr.kg/index.jsp?lang=RUS")

@dp.message_handler(commands='currency')
async def curr(message:types.Message):
    url = 'https://valuta.kg/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    news_tag = soup.find_all('<div class="kurs-bar__item">…</div>cy')
    n = 0
    for news in news_tag:
        n += 1
        await message.answer(f"{n}) {news.text}")

executor.start_polling(dp, skip_updates=True)
    

    
