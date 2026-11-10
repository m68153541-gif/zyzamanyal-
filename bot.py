import asyncio
import logging
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# ===================== НАСТРОЙКИ =====================
TOKEN = "8770882017:AAGwGisD6Pjy9xQESCc1x2Bnsv1gVBlNCHg"  # потом заменишь

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
# Приглушаем болтливые логи httpx
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# ===================== ТЕКСТЫ =====================

START_TEXT = (
    "📖 *Последний шанс*\n"
    "───────────────\n\n"
    "История одного человека, который слишком сильно полюбил — "
    "и слишком дорого за это заплатил.\n\n"
    "Это не просто рассказ. Это мануал, оставленный сообществом *zark* "
    "как память о том, кто был, но кем уже не станет.\n\n"
    "💔 *Не привязывай свои чувства к чужому человеку.*\n\n"
    "Выбери главу и пройди этот путь вместе с ним 👇"
)

CHAPTERS = {
    "ch1": (
        "🕯 *Глава 1 — Начало*\n"
        "───────────────\n\n"
        "Все хоть раз думали: «Как же скучно просто жить» — "
        "и начинали искать дело по душе.\n\n"
        "Так случилось и с человеком, которому сообщество посвятило этот мануал. "
        "Всё началось с того, что наш герой влюбился — по-настоящему. "
        "Будучи наивным, он попал в сеть под названием *«Ревард»*.\n\n"
        "Именно влюблённость сыграла большую роль — ведь на этом чувстве "
        "очень легко играть человеком. 😔\n\n"
        "Там, куда попал наш герой, трудно выбиться в люди. Но под эйфорическим "
        "чувством, не осознавая, к чему это приведёт, он начал создавать и придумывать.\n\n"
        "✨ Успех рос так же, как и любовь.\n\n"
        "_Сообщество zark, глава 1_"
    ),
    "ch2": (
        "🏆 *Глава 2 — Победы*\n"
        "───────────────\n\n"
        "Победы и первая узнаваемость часто негативно влияют на людей… "
        "Но не в случае нашего героя.\n\n"
        "Победы ему принёс не здравый смысл, а чувства, которые окрыляли "
        "и заставляли двигаться дальше. 🚀\n\n"
        "Первый успех пришёл в июле 2026 года: он выпустил на ковёр первые "
        "проекты и набрал первого человека в свою команду.\n\n"
        "Но смысл герою приносило только чувство любви — как казалось тогда, "
        "взаимной. 💌\n\n"
        "_Сообщество zark, глава 2_"
    ),
    "ch3": (
        "🌑 *Глава 3 — Выгорание*\n"
        "───────────────\n\n"
        "После успеха, как правило, приходит первая чёрная полоса. "
        "И не только в работе или соцсетях — в жизни полная неразбериха "
        "и резкие повороты событий.\n\n"
        "В начале августа у нашего героя появляется первый наплыв хейтеров. "
        "Но, несмотря на доброту — самого доброго на рынке, — наплыв его не сломал. "
        "Всё по той же причине: любовь. 💔\n\n"
        "Стоит подметить: пока человек летает от счастья, он часто закрывает глаза "
        "на минусы — ему кажется, что мир любит его, а судьба благословенна.\n\n"
        "Но пришло время разочарований. *11 августа 2026 года* наш герой нашёл в себе "
        "силы честно сказать правду о своих чувствах той самой — из-за которой всё и началось.\n\n"
        "⚡ Крах. Это не взаимно.\n\n"
        "Мир героя начал рушиться. Смысл продолжать дальше исчезал. Он не мог найти "
        "себе места, не мог понять, что именно с ним произошло. Никто не щадил — "
        "некому было выговориться, рассказать, что он чувствует.\n\n"
        "После долгих мучений и попыток всё вернуть, под давлением людей, герой решил "
        "покинуть *«Ревард»*. То, ради чего он просыпался каждое утро, рухнуло в один день. 🥀\n\n"
        "_Сообщество zark, глава 3_"
    ),
    "ch4": (
        "🌫 *Глава 4 — Осознание*\n"
        "───────────────\n\n"
        "Эх, настигла героя участь всевышняя —\n"
        "осознал он спустя недели мучительных дней:\n"
        "нельзя привязывать чувства к чужому человеку,\n"
        "ведь не факт, что он оправдает твои ожидания.\n\n"
        "Но мир уже не тот…\n"
        "И герой не тот…\n\n"
        "Вывод он вывел в своей голове —\n"
        "но какой ценой, скажи, какой?\n"
        "Больше не будет прежним заниматься он,\n"
        "сколько судеб себе испортил — не сосчитать.\n\n"
        "И не хочет наш герой меняться —\n"
        "закрылся в себе он, бедняга.\n"
        "Но кто, кроме него, будет лечить?\n"
        "Как осознать ошибки, если не жить?\n\n"
        "«Реварда» не будет. Остынет герой —\n"
        "и больше никого никогда не полюбит… 💔\n\n"
        "_Сообщество zark, глава 4_"
    ),
}

FINAL_TEXT = (
    "📜 *Общество*\n"
    "───────────────\n\n"
    "Этот мануал каждый сохранит себе как память. Нашему герою осталось совсем немножко.\n\n"
    "Создан он ради того, чтобы никто не попал в такую ситуацию, как он. "
    "Неумение отпускать человека и сильная привязанность убили талант — "
    "конечно, через время мы забудем его, но прежним его не увидеть.\n\n"
    "🕯 _Сообщество zark, архив 2026_"
)

# ===================== КЛАВИАТУРЫ =====================

def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📖 Глава 1 — Начало", callback_data="ch1")],
        [InlineKeyboardButton("🏆 Глава 2 — Победы", callback_data="ch2")],
        [InlineKeyboardButton("🌑 Глава 3 — Выгорание", callback_data="ch3")],
        [InlineKeyboardButton("🌫 Глава 4 — Осознание", callback_data="ch4")],
        [InlineKeyboardButton("📜 Общество / Архив", callback_data="final")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_menu() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("⬅️ Назад к главам", callback_data="menu")]]
    return InlineKeyboardMarkup(keyboard)


# ===================== ХЕНДЛЕРЫ =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        START_TEXT,
        parse_mode="Markdown",
        reply_markup=main_menu(),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu":
        await query.edit_message_text(
            START_TEXT,
            parse_mode="Markdown",
            reply_markup=main_menu(),
        )
    elif data in CHAPTERS:
        await query.edit_message_text(
            CHAPTERS[data],
            parse_mode="Markdown",
            reply_markup=back_menu(),
        )
    elif data == "final":
        await query.edit_message_text(
            FINAL_TEXT,
            parse_mode="Markdown",
            reply_markup=back_menu(),
        )


# ===================== ЗАПУСК =====================

def build_application() -> Application:
    """Создаёт Application с увеличенными таймаутами для long-polling."""
    return (
        Application.builder()
        .token(TOKEN)
        # Таймауты для getUpdates (long-polling) — Telegram держит соединение до 30 сек
        .get_updates_read_timeout(60.0)
        .get_updates_connect_timeout(15.0)
        .get_updates_pool_timeout(10.0)
        # Общие таймауты для остальных API-запросов
        .read_timeout(30.0)
        .connect_timeout(10.0)
        .pool_timeout(5.0)
        .build()
    )


def main():
    while True:
        try:
            app = build_application()
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CallbackQueryHandler(button_handler))
            logger.info("✅ Бот запущен и слушает Telegram...")
            app.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=False,
                close_loop=False,
            )
        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Бот остановлен вручную.")
            break
        except Exception as e:
            logger.error(f"💥 Бот упал: {e}. Перезапуск через 10 секунд...", exc_info=True)
            time.sleep(10)


if __name__ == "__main__":
    main()
