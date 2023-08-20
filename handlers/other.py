from aiogram import types, Dispatcher
from create_bot import dp, bot
import openai

# Обработчик команды /start

#@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(types.InlineKeyboardButton('RUS-ENG', callback_data='RUS-ENG'), types.InlineKeyboardButton('ENG-RUS', callback_data='ENG-RUS'))
    markup.row(types.InlineKeyboardButton(
        'Показать словарь', callback_data='all_dic'), types.InlineKeyboardButton(
        'ChatGPT', callback_data='GPT'))
    await message.answer(f'Привет, {message.from_user.first_name} 🖐️!\n\nВыбери режим тренировки 🎰.', reply_markup=markup)
    # await message.delete()

def register_handler_other(dp : Dispatcher):

  dp.register_message_handler(start, content_types=types.ContentType.TEXT)
 