import re
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = "8311144021:AAEaWam3rs71Rorr5kATSIL5kRXmC0LgkRQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Oddiy xotira (real loyiha uchun DB ishlat)
users = {}  # phone_number : user_id

# 📲 Telefon so‘rash tugmasi
phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📲 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
  "👮‍♂️ *QR Nazorat Bot* 👮‍♀️\n\n"
    "Bu bot orqali siz farzandingizning qachon *qo‘v markazga* kirganini va *chiqqanini* bilib turishingiz mumkin.\n\n"
    "📲 Ro‘yxatdan o‘tish uchun telefon raqamingizni yuboring 👇",
        reply_markup=phone_kb
    )

@dp.message(lambda m: m.contact is not None)
async def save_phone(message: types.Message):
    phone = message.contact.phone_number
    users[phone] = message.from_user.id
    await message.answer("✅ Siz ro‘yxatdan o‘tdingiz!", reply_markup=types.ReplyKeyboardRemove())

# 📢 KANALDAN KELGAN XABAR
@dp.channel_post()
async def channel_handler(message: types.Message):
    text = message.text or ""

    # Telefon raqam topish (+998...)
    phones = re.findall(r"\+998\d{9}", text)

    for phone in phones:
        if phone in users:
            user_id = users[phone]
            await bot.send_message(
                user_id,
                f"📩 Farzandingilz oqv markazga kirb keldi:\n\n{text}"
            )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
