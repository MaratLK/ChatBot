from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '7554855033:AAHc_cSdbEDvwErgZzQ218Wb07PkoFy1Q_E'

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [InlineKeyboardButton("ТОП-10 фактов о талантливом Константине Валерьевиче", callback_data='option1')],
    [InlineKeyboardButton("Команда о Константине Валерьевиче", callback_data='option2')],
    [InlineKeyboardButton("Пожелания нашему Константину Валерьивичу", callback_data='option3')],
    [InlineKeyboardButton("Зарядиться энергией команды", callback_data='option4')],
    [InlineKeyboardButton("Тест 360", callback_data='option5')]
]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выберите опцию:", reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'option1':
        await query.message.reply_text("Топ")
    elif query.data == 'option2':
        await query.message.reply_text("42 факта о Константине!")
    elif query.data == 'option3':
        await query.message.reply_text("Оставьте пожелание для Константина!")
    elif query.data == 'option4':
        await query.message.reply_text("Вот интересное видео!")
    elif query.data == 'option5':
        await query.message.reply_text("Вот контактные данные!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == '__main__':
    main()
