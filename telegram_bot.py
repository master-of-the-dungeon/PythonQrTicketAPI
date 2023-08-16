import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from bot_token import TELEGRAM_API_TOKEN
from yoomoney import Client

# YooMoney API credentials
shop_id = 'your_shop_id'
secret_key = 'your_secret_key'
client = Client(shop_id, secret_key)

# Telegram bot token
bot_token = 'your_bot_token'
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Create a payment request
async def create_payment(amount, description, order_id):
    payment = client.create_payment(amount, description, order_id=order_id)
    return payment

# Get payment status
async def get_payment_status(payment_id):
    payment_info = client.get_payment(payment_id)
    return payment_info.status

# Command handler to start payment
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    payment_info = await create_payment(1000, "Sample Payment", str(message.from_user.id))
    payment_id = payment_info.id
    payment_url = payment_info.confirmation.confirmation_url
    await message.reply(f"Click the link to complete the payment: {payment_url}")

# Command handler to check payment status
@dp.message_handler(commands=['check'])
async def check_payment(message: types.Message):
    payment_id = message.get_args()
    payment_status = await get_payment_status(payment_id)
    await message.reply(f"Payment status: {payment_status}")

# Run the bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
