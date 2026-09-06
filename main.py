import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, message
from aiogram.filters import CommandStart
from zxcvbn import zxcvbn

import secrets

#Insert your Telegram bot token there:
BOT_TOKEN = secrets.BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

#Easy level from 0 to 4
STATUSES = {
    0: "🔴 Very bad! Too easy to guess",
    1: "🟠 Bad. Not safe",
    2: "🟡 Normal. But you can make it better.",
    3: "🟢 Good! A strong password.",
    4: "🔵 Super! Very strong and safe."
}

#Simple welcome message
@dp.message(CommandStart())
async def start_cmd(message:Message):
    await message.answer(
        "✌️Hi! I am a Password Checker Bot.\n\n"
        "Send me any text, and I will check your password! 🔒\n\n"
        "⚠️ *Rule:* Do not send your real passwords to bots! Type a fake or similar password.️"
    )

#Easy logic for checking
@dp.message(F.text)
async def check_password(message:Message):
    password = message.text

    #Try to delete the user's password for safety
    try:
        await message.delete()
    except Exception:
        pass

    #Start of inspection
    #Length check
    if len(password) < 8:
        await message.answer(
            f"📊 *Your Password Report:*\n\n"
            f"Status: 🔴 Too short!\n\n"
            f"💡 *Tip:* Your password must have *at least 8 characters*.\n\n"
        )
        return
    if len(password) > 16:
        await message.answer(
            f"📊 *Your Password Report:*\n\n"
            f"Status: 🔴 Too long!\n\n"
            f"💡 *Tip:* Your password must be between 8 and 16 characters*.\n\n"
        )
        return

    #Check for the presence of a letter and a number
    has_digit = any(char.isdigit() for char in password)
    has_letter = any(char.isalpha() for char in password)

    if not has_digit or not has_letter:
        await message.answer(
            f"📊 *Your Password Report:*\n\n"
            f"Status: 🟠Too simple!\n\n"
            f"💡 *Tip:* A safe password must include *both digits and letters*."
        )
        return
    #End of check

    #If basic rules passed, launching smart analysis zxcvbn for word patterns
    analysis = zxcvbn(password)
    score = analysis['score']
    result_text = STATUSES[score]
    crack_time = analysis['crack_times_display']['offline_fast_hashing_1e10_per_second']

    #Simple report text
    final_message = f"📊 *Your Password Report:*\n\n" \
                    f"Status:{result_text}\n\n" \
                    f"🕑 _Time to hack:_ '{crack_time}'\n\n" \
                    f"🧹 _Note: I deleted your message for security._"

    await message.answer(final_message, parse_mode="Markdown")

async def main():
    print("Bot is running! Open Telegram and type /start")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())