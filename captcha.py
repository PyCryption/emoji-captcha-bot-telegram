from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import random
import datetime

def generate_captcha_message(context: CallbackContext):
    emojis = ['🍎', '🚗', '🌈', '🏀', '🐱', '🍕', '🎸', '📘', '👻', '🚀', '😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇']
    target_emoji = random.choice(emojis)
    context.user_data['target_emoji'] = target_emoji

    random.shuffle(emojis)
    emojis[:8] = random.sample(emojis, 8)
    if target_emoji not in emojis[:8]:
        emojis[random.randint(0, 7)] = target_emoji

    keyboard = [[InlineKeyboardButton(emoji, callback_data=emoji) for emoji in emojis[i:i+3]] for i in range(0, 9, 3)]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return f'Выберите {target_emoji}, чтобы пройти капчу.', reply_markup

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    now = datetime.datetime.now()

    if 'captcha_passed' in context.user_data and (now - context.user_data['captcha_passed']).total_seconds() < 3600:
        update.message.reply_text("Привет! Вы уже прошли капчу, можете использовать бота.")
        return

    message, reply_markup = generate_captcha_message(context)
    update.message.reply_text(message, reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == context.user_data.get('target_emoji'):
        context.user_data['captcha_passed'] = datetime.datetime.now()
        query.edit_message_text(text="Вы прошли капчу!")
    else:
        message, reply_markup = generate_captcha_message(context)
        query.edit_message_text(text=message, reply_markup=reply_markup)

def main():
    updater = Updater("6960200328:AAFTO8TwLsMMZS_tFAuUbjqGqUcBXccG608", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
