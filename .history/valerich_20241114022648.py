from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from questions import questions

TOKEN = '7659624823:AAEsDUcuT7_ocOMTxN_YcRbZm3CdpusdBhs'

user_data = {}  # Словарь для хранения прогресса пользователя в тесте

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ТОП-10 фактов о талантливом Константине Валерьевиче", callback_data='option1')],
        [InlineKeyboardButton("Команда о Константине Валерьевиче", callback_data='option2')],
        [InlineKeyboardButton("Пожелания нашему Константину Валерьевичу", callback_data='option3')],
        [InlineKeyboardButton("Зарядиться энергией команды", callback_data='option4')],
        [InlineKeyboardButton("Тест 360°", callback_data='test_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выберите опцию:", reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'test_start':
        user_id = query.from_user.id
        user_data[user_id] = {"current_question": 0, "score": 0}
        await send_question(query, context)
    elif query.data.startswith("answer_"):
        await handle_answer(query, context)
    elif query.data == 'go_back':
        await start(update, context)

# Функция для отправки вопроса
async def send_question(query, context):
    user_id = query.from_user.id
    user_info = user_data.get(user_id)

    # Проверка на завершение теста
    if user_info is None or user_info["current_question"] >= len(questions):
        await finish_test(query, context)
        return

    question_data = questions[user_info["current_question"]]

    # Отправляем вопрос и варианты ответов как сообщение
    full_text = f"{question_data['question']}\n\n"
    for option in question_data['options']:
        full_text += f"{option}\n"

    await query.message.reply_text(full_text)

    # Отправляем кнопки с номерами и кнопку "Назад"
    keyboard = [
        [InlineKeyboardButton(f"Вариант {i + 1}", callback_data=f"answer_{i}")]
        for i in range(len(question_data['options']))
    ]
    keyboard.append([InlineKeyboardButton("Вернуться назад", callback_data='go_back')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Выберите ответ:", reply_markup=reply_markup)

# Функция для обработки ответа
async def handle_answer(query, context):
    user_id = query.from_user.id
    user_info = user_data.get(user_id)
    if user_info is None:
        return

    selected_answer = int(query.data.split("_")[1])
    current_question = user_info["current_question"]
    correct_answer = questions[current_question]["correct"]

    if selected_answer == correct_answer:
        user_info["score"] += 1

    user_info["current_question"] += 1

    if user_info["current_question"] < len(questions):
        await send_question(query, context)
    else:
        await finish_test(query, context)

# Функция для завершения теста и вывода результата в процентах
async def finish_test(query, context):
    user_id = query.from_user.id
    user_info = user_data.get(user_id)
    if user_info is None:
        return

    total_questions = len(questions)
    score = user_info["score"]
    percentage = (score / total_questions) * 100

    await query.message.reply_text(
        f"Тест завершён!\nВы набрали {score} из {total_questions} правильных ответов.\n"
        f"Процент правильных ответов: {percentage:.2f}%."
    )
    del user_data[user_id]

    # Возвращаемся к стартовому меню
    await start(query, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == '__main__':
    main()

"""
user_data = {}  # Словарь для хранения прогресса пользователя в тесте

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ТОП-10 фактов о талантливом Константине Валерьевиче", callback_data='option1')],
        [InlineKeyboardButton("Команда о Константине Валерьевиче", callback_data='option2')],
        [InlineKeyboardButton("Пожелания нашему Константину Валерьевичу", callback_data='option3')],
        [InlineKeyboardButton("Зарядиться энергией команды", callback_data='option4')],
        [InlineKeyboardButton("Тест 360°", callback_data='test_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выберите опцию:", reply_markup=reply_markup)

# Обработка нажатий на кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'test_start':
        user_id = query.from_user.id
        user_data[user_id] = {"current_question": 0, "score": 0}
        await send_question(query, context)
    elif query.data.startswith("answer_"):
        await handle_answer(query, context)

# Функция для отправки вопроса
async def send_question(query, context):
    user_id = query.from_user.id
    user_info = user_data.get(user_id)

    if user_info is None or user_info["current_question"] >= len(questions):
        await query.message.reply_text("Тест завершён!")
        return

    question_data = questions[user_info["current_question"]]

    # Отправляем вопрос и варианты ответов как сообщение
    full_text = f"{question_data['question']}\n\n"
    for option in question_data['options']:
        full_text += f"{option}\n"

    await query.message.reply_text(full_text)

    # Отправляем кнопки с номерами
    keyboard = [
        [InlineKeyboardButton(f"Вариант {i + 1}", callback_data=f"answer_{i}")]
        for i in range(len(question_data['options']))
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Выберите ответ:", reply_markup=reply_markup)

# Функция для обработки ответа
async def handle_answer(query, context):
    user_id = query.from_user.id
    user_info = user_data.get(user_id)
    if user_info is None:
        return

    selected_answer = int(query.data.split("_")[1])
    current_question = user_info["current_question"]
    correct_answer = questions[current_question]["correct"]

    if selected_answer == correct_answer:
        user_info["score"] += 1

    user_info["current_question"] += 1

    if user_info["current_question"] < len(questions):
        await send_question(query, context)
    else:
        score = user_info["score"]
        await query.message.reply_text(f"Тест завершён! Вы набрали {score} из {len(questions)}.")
        del user_data[user_id]

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен и готов к работе!")
    app.run_polling()

if __name__ == '__main__':
    main()

"""