import os
import threading

from dotenv import load_dotenv
from flask import Flask

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8286503966

FORCE_CHANNEL = "@samir_420_amreka"

CHANNELS = {
    "📢 کانال ۱": "https://t.me/new_otp_1",
    "📢 کانال ۲": "https://t.me/TempNumOfficial",
    "📢 کانال ۳": "https://t.me/starkempiremain",
}

SITES = {
    "🌐 VirtualSMSNumbers": "https://virtualsmsnumbers.com/",
    "🌐 BuySMSNumbers": "https://buysmsnumbers.com/",
    "🌐 SMSario": "https://smsario.com/",
    "🌐 TemporarySMSNumber": "https://temporarysmsnumber.com/",
}

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "VIRTUAL NUMBER BOT IS ONLINE"


@web_app.route("/health")
def health():
    return "OK"


def run_web():
    port = int(os.getenv("PORT", "10000"))
    web_app.run(host="0.0.0.0", port=port)


def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ["🌐 بهترین سایت‌ها"],
            ["📢 کانال ۱", "📢 کانال ۲"],
            ["📢 کانال ۳", "👤 سازنده ربات"],
        ],
        resize_keyboard=True,
    )


def join_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📢 عضویت در کانال",
                    url="https://t.me/samir_420_amreka",
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ بررسی عضویت",
                    callback_data="check_join",
                )
            ],
        ]
    )


async def is_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        member = await context.bot.get_chat_member(
            chat_id=FORCE_CHANNEL,
            user_id=user_id,
        )

        return member.status in (
            "member",
            "administrator",
            "creator",
        )

    except Exception as e:
        print(f"Membership check error: {e}")
        return False


async def send_join_message(update: Update):
    text = (
        "🔒 برای استفاده از ربات ابتدا باید عضو کانال ما شوید.\n\n"
        "1️⃣ روی «عضویت در کانال» بزنید.\n"
        "2️⃣ عضو کانال شوید.\n"
        "3️⃣ سپس روی «بررسی عضویت» بزنید. 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=join_keyboard(),
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_member(update, context):
        await send_join_message(update)
        return

    await update.message.reply_text(
        "✨ به ربات بهترین سایت‌های شماره مجازی خوش آمدید.\n\n"
        "از منوی زیر گزینه موردنظرت را انتخاب کنید 👇",
        reply_markup=main_keyboard(),
    )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if await is_member(update, context):
        await query.message.reply_text(
            "✅ عضویت شما تأیید شد.\n\n"
            "حالا می‌توانید از ربات استفاده کنید. 👇",
            reply_markup=main_keyboard(),
        )
    else:
        await query.message.reply_text(
            "❌ هنوز عضویت شما تأیید نشده است.\n\n"
            "ابتدا عضو کانال شوید و دوباره بررسی کنید.",
            reply_markup=join_keyboard(),
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_member(update, context):
        await send_join_message(update)
        return

    text = update.message.text

    if text == "🌐 بهترین سایت‌ها":
        buttons = []

        for name, url in SITES.items():
            buttons.append(
                [
                    InlineKeyboardButton(
                        name,
                        url=url,
                    )
                ]
            )

        await update.message.reply_text(
            "🌐 بهترین سایت‌های شماره مجازی\n\n"
            "یکی از سایت‌ها را انتخاب کنید 👇",
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    elif text in CHANNELS:
        url = CHANNELS[text]

        await update.message.reply_text(
            f"{text}\n\n"
            "برای ورود روی دکمه زیر بزنید 👇",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🚀 ورود به کانال",
                            url=url,
                        )
                    ]
                ]
            ),
        )

    elif text == "👤 سازنده ربات":
        await update.message.reply_text(
            "👤 سازنده ربات\n\n"
            "𝑺𝑨𝑴𝑰𝑹 𝟒𝟐𝟎\n\n"
            "برای ارتباط با سازنده روی دکمه زیر بزنید 👇",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "💬 ارتباط با سازنده",
                            url="https://t.me/samir_khass",
                        )
                    ]
                ]
            ),
        )

    else:
        await update.message.reply_text(
            "👇 لطفاً یکی از گزینه‌های منو را انتخاب کنید.",
            reply_markup=main_keyboard(),
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set")

    threading.Thread(
        target=run_web,
        daemon=True,
    ).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(
            check_join,
            pattern="^check_join$",
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    app.add_error_handler(error_handler)

    print("VIRTUAL NUMBER BOT IS RUNNING...")

    app.run_polling()


if __name__ == "__main__":
    main()
