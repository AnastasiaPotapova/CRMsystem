import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from collections import defaultdict
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Этапы разговора для отчетов
FIO, DATE, TITLE, VISITORS, NOTES = range(5)

# Этапы для опроса готовности
READINESS_START, READINESS_ANSWERING, READINESS_RESULT = range(5, 8)

# Хранение результатов опроса готовности
readiness_results = defaultdict(lambda: defaultdict(int))
user_readiness_answers = {}

# Вопросы опроса готовности
READINESS_QUESTIONS = [
    "Оцените вашу готовность к проведению экскурсии по 10-балльной шкале",
    "Все ли необходимые материалы подготовлены?",
    "Проверили ли вы маршрут экскурсии?",
    "Достаточно ли у вас информации о группе посетителей?",
    "Есть ли у вас вопросы или нужна помощь?",
    "Подтверждаете ли вы готовность провести экскурсию?"
]

# Варианты ответов для опроса готовности
READINESS_OPTIONS = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    ["Да, все готово", "Частично готово", "Нет, нужна помощь"],
    ["Да, полностью проверен", "Частично проверен", "Нет, не проверен"],
    ["Да, полная информация", "Частичная информация", "Нет информации"],
    ["Нет вопросов", "Есть небольшие вопросы", "Нужна помощь"],
    ["✅ Да, подтверждаю готовность", "❌ Нет, не готов"]
]

# Клавиатура для пропуска шага
skip_keyboard = [['Пропустить']]
skip_markup = ReplyKeyboardMarkup(skip_keyboard, one_time_keyboard=True)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Добро пожаловать в систему музея!\n\n'
        'Доступные команды:\n'
        '/new_report - создать отчет об экскурсии\n'
        '/check_readiness - проверить готовность к экскурсии\n'
        '/readiness_stats - статистика готовности\n'
        '/cancel - отменить текущую операцию'
    )

# ========== ФУНКЦИИ ДЛЯ ОТЧЕТОВ ==========

def new_report(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Создание отчета об экскурсии. Введите ФИО экскурсовода:',
        reply_markup=ReplyKeyboardRemove()
    )
    return FIO

def fio(update: Update, context: CallbackContext) -> int:
    context.user_data['fio'] = update.message.text
    update.message.reply_text('Введите дату экскурсии (например, 01.01.2023):')
    return DATE

def date(update: Update, context: CallbackContext) -> int:
    context.user_data['date'] = update.message.text
    update.message.reply_text('Введите название экскурсии:')
    return TITLE

def title(update: Update, context: CallbackContext) -> int:
    context.user_data['title'] = update.message.text
    update.message.reply_text('Введите количество посетителей:')
    return VISITORS

def visitors(update: Update, context: CallbackContext) -> int:
    context.user_data['visitors'] = update.message.text
    update.message.reply_text(
        'Добавьте особые отметки (или нажмите "Пропустить"):',
        reply_markup=skip_markup
    )
    return NOTES

def notes(update: Update, context: CallbackContext) -> int:
    if update.message.text != 'Пропустить':
        context.user_data['notes'] = update.message.text
    else:
        context.user_data['notes'] = 'Не указано'
    
    # Формируем отчет
    report = (
        f"📊 Новый отчет об экскурсии:\n\n"
        f"👤 ФИО: {context.user_data['fio']}\n"
        f"📅 Дата: {context.user_data['date']}\n"
        f"🏛️ Экскурсия: {context.user_data['title']}\n"
        f"👥 Посетители: {context.user_data['visitors']}\n"
        f"📝 Особые отметки: {context.user_data['notes']}"
    )
    
    update.message.reply_text(
        report,
        reply_markup=ReplyKeyboardRemove()
    )
    
    logger.info("Создан новый отчет: %s", report)
    
    return ConversationHandler.END

# ========== ФУНКЦИИ ДЛЯ ОПРОСА ГОТОВНОСТИ ==========

def check_readiness(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    
    # Сбрасываем предыдущие ответы пользователя
    if user_id in user_readiness_answers:
        del user_readiness_answers[user_id]
    
    context.user_data['readiness_question_index'] = 0
    context.user_data['readiness_answers'] = []
    
    update.message.reply_text(
        '🎯 Проверка готовности к экскурсии\n\n'
        'Ответьте на несколько вопросов, чтобы подтвердить вашу готовность.\n'
        'Это поможет обеспечить качественное проведение экскурсии.',
        reply_markup=ReplyKeyboardRemove()
    )
    
    # Задаем первый вопрос
    return ask_next_readiness_question(update, context)

def ask_next_readiness_question(update: Update, context: CallbackContext) -> int:
    question_index = context.user_data['readiness_question_index']
    
    if question_index >= len(READINESS_QUESTIONS):
        # Все вопросы заданы, завершаем опрос
        return calculate_readiness_result(update, context)
    
    question = READINESS_QUESTIONS[question_index]
    options = READINESS_OPTIONS[question_index]
    
    # Создаем клавиатуру с вариантами ответов
    if len(options) <= 3:
        keyboard = [options]  # Все варианты в одном ряду
    else:
        keyboard = [options[i:i+2] for i in range(0, len(options), 2)]  # По 2 кнопки в ряду
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    update.message.reply_text(
        f"❓ Вопрос {question_index + 1}/{len(READINESS_QUESTIONS)}:\n{question}",
        reply_markup=reply_markup
    )
    
    return READINESS_ANSWERING

def receive_readiness_answer(update: Update, context: CallbackContext) -> int:
    answer = update.message.text
    question_index = context.user_data['readiness_question_index']
    
    # Сохраняем ответ
    context.user_data['readiness_answers'].append(answer)
    
    # Записываем в общую статистику
    readiness_results[question_index][answer] += 1
    
    # Переходим к следующему вопросу
    context.user_data['readiness_question_index'] += 1
    
    return ask_next_readiness_question(update, context)

def calculate_readiness_result(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    answers = context.user_data['readiness_answers']
    
    # Анализируем ответы
    readiness_score = 0
    max_score = 10
    
    # Вопрос 1: Оценка готовности (1-10 баллов)
    try:
        q1_score = int(answers[0])
        readiness_score += q1_score
    except:
        q1_score = 5  # Среднее значение при ошибке
    
    # Вопрос 2: Материалы (Да=2, Частично=1, Нет=0)
    if answers[1] == "Да, все готово":
        readiness_score += 2
    elif answers[1] == "Частично готово":
        readiness_score += 1
    
    # Вопрос 3: Маршрут (Да=2, Частично=1, Нет=0)
    if answers[2] == "Да, полностью проверен":
        readiness_score += 2
    elif answers[2] == "Частично проверен":
        readiness_score += 1
    
    # Вопрос 4: Информация о группе (Да=2, Частично=1, Нет=0)
    if answers[3] == "Да, полная информация":
        readiness_score += 2
    elif answers[3] == "Частичная информация":
        readiness_score += 1
    
    # Вопрос 5: Вопросы/помощь (Нет вопросов=2, Вопросы=1, Помощь=0)
    if answers[4] == "Нет вопросов":
        readiness_score += 2
    elif answers[4] == "Есть небольшие вопросы":
        readiness_score += 1
    
    # Вопрос 6: Подтверждение готовности (Да=2, Нет=0)
    if answers[5] == "✅ Да, подтверждаю готовность":
        readiness_score += 2
    
    # Определяем уровень готовности
    percentage = (readiness_score / max_score) * 100
    
    if percentage >= 80:
        status = "✅ ВЫСОКАЯ ГОТОВНОСТЬ"
        recommendation = "Вы полностью готовы к проведению экскурсии!"
    elif percentage >= 60:
        status = "⚠️ СРЕДНЯЯ ГОТОВНОСТЬ"
        recommendation = "В целом готовы, но есть моменты для улучшения."
    else:
        status = "❌ НИЗКАЯ ГОТОВНОСТЬ"
        recommendation = "Рекомендуется отложить экскурсию или обратиться за помощью."
    
    # Формируем детальный отчет
    result_message = (
        f"🎯 РЕЗУЛЬТАТ ПРОВЕРКИ ГОТОВНОСТИ\n\n"
        f"📊 Общий балл: {readiness_score}/{max_score} ({percentage:.0f}%)\n"
        f"🏆 Статус: {status}\n\n"
        f"📋 Детали:\n"
        f"• Самооценка готовности: {answers[0]}/10\n"
        f"• Подготовка материалов: {answers[1]}\n"
        f"• Проверка маршрута: {answers[2]}\n"
        f"• Информация о группе: {answers[3]}\n"
        f"• Наличие вопросов: {answers[4]}\n"
        f"• Подтверждение готовности: {answers[5]}\n\n"
        f"💡 Рекомендация: {recommendation}"
    )
    
    # Сохраняем ответы пользователя
    user_readiness_answers[user_id] = {
        'answers': answers,
        'score': readiness_score,
        'percentage': percentage,
        'status': status,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'username': update.message.from_user.username or 'Без имени'
    }
    
    update.message.reply_text(
        result_message,
        reply_markup=ReplyKeyboardRemove()
    )
    
    logger.info("Пользователь %s завершил проверку готовности с результатом %s/%s", 
                user_id, readiness_score, max_score)
    
    return ConversationHandler.END

def show_readiness_stats(update: Update, context: CallbackContext) -> None:
    if not readiness_results:
        update.message.reply_text("📊 Проверки готовности еще не проводились.")
        return
    
    # Статистика по всем проверкам
    total_checks = len(user_readiness_answers)
    
    if total_checks == 0:
        update.message.reply_text("Нет данных о проверках готовности.")
        return
    
    # Подсчет статистики по статусам
    status_count = defaultdict(int)
    total_percentage = 0
    
    for user_data in user_readiness_answers.values():
        status_count[user_data['status']] += 1
        total_percentage += user_data['percentage']
    
    avg_percentage = total_percentage / total_checks
    
    # Формируем общую статистику
    stats_text = (
        f"📊 СТАТИСТИКА ГОТОВНОСТИ ЭКСКУРСОВОДОВ\n\n"
        f"📈 Всего проверок: {total_checks}\n"
        f"📊 Средний показатель: {avg_percentage:.1f}%\n\n"
        f"🏆 Распределение по статусам:\n"
    )
    
    for status, count in status_count.items():
        percentage = (count / total_checks) * 100
        stats_text += f"• {status}: {count} ({percentage:.1f}%)\n"
    
    # Статистика по последнему вопросу (подтверждение готовности)
    last_question_results = readiness_results[len(READINESS_QUESTIONS)-1]
    total_responses = sum(last_question_results.values())
    
    if total_responses > 0:
        stats_text += f"\n✅ Подтвердили готовность: {last_question_results.get('✅ Да, подтверждаю готовность', 0)}/{total_responses}"
        stats_text += f"\n❌ Не готовы: {last_question_results.get('❌ Нет, не готов', 0)}/{total_responses}"
    
    # Последние 5 проверок
    stats_text += f"\n\n🕒 Последние проверки:\n"
    recent_checks = sorted(user_readiness_answers.items(), 
                          key=lambda x: x[1]['timestamp'], 
                          reverse=True)[:5]
    
    for user_id, data in recent_checks:
        stats_text += f"• {data['timestamp']}: {data['score']}/10 ({data['percentage']:.0f}%) - {data['status']}\n"
    
    update.message.reply_text(stats_text)

# ========== ОБЩИЕ ФУНКЦИИ ==========

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Операция отменена.',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    # Замените 'YOUR_TOKEN' на токен от BotFather
    updater = Updater("YOUR_TOKEN")
    dispatcher = updater.dispatcher

    # ConversationHandler для отчетов
    report_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new_report', new_report)],
        states={
            FIO: [MessageHandler(Filters.text & ~Filters.command, fio)],
            DATE: [MessageHandler(Filters.text & ~Filters.command, date)],
            TITLE: [MessageHandler(Filters.text & ~Filters.command, title)],
            VISITORS: [MessageHandler(Filters.text & ~Filters.command, visitors)],
            NOTES: [MessageHandler(Filters.text & ~Filters.command, notes)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # ConversationHandler для проверки готовности
    readiness_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('check_readiness', check_readiness)],
        states={
            READINESS_ANSWERING: [MessageHandler(Filters.text & ~Filters.command, receive_readiness_answer)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Регистрируем обработчики
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('readiness_stats', show_readiness_stats))
    dispatcher.add_handler(report_conv_handler)
    dispatcher.add_handler(readiness_conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
