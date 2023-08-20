from aiogram import types, Dispatcher
from create_bot import dp, bot
import openai
from aiogram.dispatcher.storage import FSMContext

class MyStates:
    GPT = 'g'


current_conversation = {}  # Словарь для хранения состояний беседы

# @dp.callback_query_handler(lambda query: query.data == 'GPT')
async def gpt(callback_query: types.CallbackQuery):
    if callback_query.message.chat.id in current_conversation:
        await bot.send_message(callback_query.message.chat.id, "Ты уже ведешь беседу с GPT. Когда закончишь, используй команду /reset.")
    else:
        current_conversation[callback_query.message.chat.id] = "gpt"
        await bot.send_message(callback_query.message.chat.id, "Давай устроим с тобой диалог с GPT. Когда закончишь, используй команду /reset.")

@dp.message_handler(commands=['reset'])
async def reset(message: types.Message):
    if message.chat.id in current_conversation:
        del current_conversation[message.chat.id]
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.row(types.InlineKeyboardButton('GPT', callback_data='GPT'), types.InlineKeyboardButton('ENG-RUS', callback_data='ENG'))
        await message.answer("Беседа завершена. Возвращаемся в основное меню.", reply_markup=markup)
    else:
        await message.answer("Ты не ведешь беседу с GPT. Используй команду /start для начала.")

@dp.message_handler(content_types=['text'])
async def handle_message(message: types.Message):
    if message.chat.id in current_conversation and current_conversation[message.chat.id] == "gpt":
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=message.text,
            max_tokens=150,
            temperature=0.7,
            n=1,
            stop=None
        )
        if response and response.choices:
            reply = response.choices[0].text.strip()
        else:
            reply = 'Что-то пошло не так!'
        await bot.send_message(message.chat.id, reply)
    else:
        await bot.send_message(message.chat.id, "Я не понял, о чем ты. Если хочешь начать диалог с GPT, используй команду /start.")


def register_handlers_gpt(dp: Dispatcher):

  dp.register_callback_query_handler(gpt, lambda query: query.data == 'GPT')