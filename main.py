import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
APP_URL = os.environ.get("APP_URL")  # например: https://mybot.onrender.com
if not BOT_TOKEN or not APP_URL:
    raise RuntimeError("Установите BOT_TOKEN и APP_URL в переменных окружения")

WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{APP_URL}{WEBHOOK_PATH}"
PORT = int(os.environ.get("PORT", 8000))
HOST = "0.0.0.0"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Привет", "Помощь")
    await message.answer("👋 Привет! Я бот на aiogram.\nНапиши мне что-то или нажми кнопку.", reply_markup=kb)

@dp.message_handler(commands=["help"])
async def help_cmd(message: types.Message):
    await message.answer("Доступные команды:\n/start — приветствие\n/help — помощь")

@dp.message_handler(lambda m: m.text == "Привет")
async def reply_hello(message: types.Message):
    await message.answer("Привет! Как дела?")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Эхо: {message.text}")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")

async def on_shutdown(dp):
    logging.info("Удаляем webhook...")
    await bot.delete_webhook()
    await bot.close()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=HOST,
        port=PORT,
    )
