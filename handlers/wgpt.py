from aiogram import types, Dispatcher
from create_bot import dp, bot
import openai
from aiogram.dispatcher.storage import FSMContext

class MyStates:
    GPT = 'gpt'

user_states = {}
current_conversation = {}  # Словарь для хранения состояний беседы

# @dp.callback_query_handler(lambda query: query.data == 'GPT')
async def gpt(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    if callback_query.message.chat.id in current_conversation:
        await bot.send_message(callback_query.message.chat.id, "Ты уже ведешь беседу с GPT. Когда закончишь, используй команду /reset.")
    else:
        current_conversation[callback_query.message.chat.id] = "gpt"
        await bot.send_message(callback_query.message.chat.id, "Давай устроим с тобой диалог на английском языке на тему летние каникулы.")
        await handle_message_gpt(callback_query.message, state, user_id)
        user_states[user_id] = MyStates.GPT

# Задаем тему в чат

# Функция для отправки следующего ответа bot GPT

# @dp.message_handler(content_types=['text'])
async def handle_message_gpt(message: types.Message, state: FSMContext, user_id: int):
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
    await state.set_state(MyStates.GPT)

@dp.message_handler(state=MyStates.GPT, content_types=types.ContentTypes.TEXT)
async def check_answer_gpt(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if state == MyStates.GPT:
        await process_answer_gpt(message, user_id)
    else:
        await message.answer('Сбой состояний!')

async def process_answer_gpt(message: types.Message, user_id: int):
    state = dp.current_state(user=user_id)
    user_answer = message.text.strip()

    if user_answer.lower() == 'reset':
      markup = types.InlineKeyboardMarkup(row_width=2)
      markup.row(types.InlineKeyboardButton('RUS-ENG', callback_data='RUS-ENG'), types.InlineKeyboardButton('ENG-RUS', callback_data='ENG-RUS'))
      markup.row(types.InlineKeyboardButton(
        'Показать словарь', callback_data='all_dic'), types.InlineKeyboardButton(
        'ChatGPT', callback_data='GPT'))
      await message.answer("Беседа завершена. Возвращаемся в основное меню.", reply_markup=markup)
      await state.finish()
        
    else:
      await handle_message_gpt(message, state, user_id)
        


    

def register_handlers_gpt(dp: Dispatcher):

  dp.register_callback_query_handler(gpt, lambda query: query.data == 'GPT')