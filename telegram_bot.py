from aiogram import *
from bot_token import TELEGRAM_API_TOKEN
bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я продаю билеты. Напиши /help чтобы посмотреть, что я умею")

executor.start_polling(dp, skip_updates=True)