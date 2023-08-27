from aiogram import types
from aiogram import Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.storage import FSMContext
import random
import json
import asyncio


# Определяем состояния (states)


class MyStates:
    QUESTION = 'question'
    QUESTION_RUS = 'question_rus'


# Загружаем данные словарей
with open('data.json', 'r', encoding='utf-8') as file:
    data_list = json.load(file)

with open('adverb.json', 'r', encoding='utf-8') as file:
    adverb_list = json.load(file)

with open('other.json', 'r', encoding='utf-8') as file:
    other_list = json.load(file)

# Загружаем данные со словами и их переводами из файла phrases.json
with open('phrases.txt', 'r', encoding='utf-8') as file:
    phrases = [line.strip() for line in file]

random_phrase = random.choice(phrases)
correct_answers = 0
wrong_answers = 0
error = 0
finish = 0
user_answer = "NONE"
user_states = {}
chat_id = 0
user_message_ids = []

# Обработчик команды /RUS-ENG /ENG-RUS

# @dp.callback_query_handler(lambda query: query.data == 'RUS-ENG')


async def dictionary_rus(callback_query: types.CallbackQuery):
    global chat_id
    chat_id = callback_query.message.chat.id
    user_markup = callback_query.data
    markup = types.InlineKeyboardMarkup(row_width=3)
    if user_markup == 'RUS-ENG':
        bt1 = types.InlineKeyboardButton('Глаголы', callback_data='data_rus')
        bt2 = types.InlineKeyboardButton(
            'Предлоги', callback_data='adverb_rus')
        bt3 = types.InlineKeyboardButton(
            'Прочие слова', callback_data='other_rus')
    else:
        bt1 = types.InlineKeyboardButton('Глаголы', callback_data='data_eng')
        bt2 = types.InlineKeyboardButton(
            'Предлоги', callback_data='adverb_eng')
        bt3 = types.InlineKeyboardButton(
            'Прочие слова', callback_data='other_eng')
    markup.row(bt1, bt2, bt3)
    await callback_query.message.edit_text('Выбери словарь:', reply_markup=markup)

# Функция для отправки следующего вопроса с переводом RUS-ENG


async def send_question_rus(message: types.Message, state: FSMContext, user_id: int):
    global user_answer
    if user_answer == 'data_rus':
        dictionary = data_list
    if user_answer == 'adverb_rus':
        dictionary = adverb_list
    if user_answer == 'other_rus':
        dictionary = other_list
    eng_rus_data = {value: key for key, value in dictionary.items()}
    key, value = random.choice(list(eng_rus_data.items()))
    await message.answer(f'Введите перевод:\n\n{key}  --->')
    user_message_ids.append(message.message_id)
    user_message_ids.append(message.message_id+2)
    user_states[user_id] = MyStates.QUESTION_RUS
    await state.set_state(MyStates.QUESTION_RUS)
    await dp.current_state(user=user_id).update_data(key=key, value=value)

# Выбираем словарь


@dp.callback_query_handler(lambda query: query.data == 'data_rus' or query.data == 'adverb_rus' or query.data == 'other_rus')
async def play_rus_eng(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    global user_answer
    user_answer = callback_query.data
    await callback_query.message.answer('Отлично! Давай начнем 💬.\n\nДля завершения тренировки напиши слово - "stop"')
    user_message_ids.append(callback_query.message.message_id+1)
    await asyncio.sleep(1)
    await send_question_rus(callback_query.message, state, user_id)
    user_states[user_id] = MyStates.QUESTION_RUS
    await asyncio.sleep(1)

# Обработчик текстовых сообщений


@dp.message_handler(state=MyStates.QUESTION_RUS, content_types=types.ContentTypes.TEXT)
async def check_answer_rus(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if state == MyStates.QUESTION_RUS:
        await process_answer_rus(message, user_id)
    else:
        await message.answer('Сбой состояний!')


async def process_answer_rus(message: types.Message, user_id: int):
    global correct_answers, wrong_answers, error, finish
    state = dp.current_state(user=user_id)
    state_data = await state.get_data()
    key = state_data.get('key')
    value = state_data.get('value')
    print(key, value)
    user_answer = message.text.strip()

    if finish == 10:
        await message.answer('Тренировка окончена!\n ... Идёт чистка чата!')
        user_message_ids.append(message.message_id)
        user_message_ids.append(message.message_id+1)
        finish = 0
        await asyncio.sleep(1)
        await show_results(message)
        await state.finish()
        return

    elif user_answer.lower() == 'stop':
        finish = 0
        await message.answer('Тренировка окончена!\n ... Идёт чистка чата!')
        user_message_ids.append(message.message_id)
        user_message_ids.append(message.message_id+1)
        await asyncio.sleep(1)
        await show_results(message)
        await state.finish()
        return

    elif value is not None and user_answer.lower() == value.lower():
        correct_answers += 1
        finish += 1
        error = 0
        await message.answer('✅ Верно!')
        await send_question_rus(message, state, user_id)
        user_message_ids.append(message.message_id+1)

    else:
        if error < 1:
            error += 1
            await message.answer('❌' + random_phrase)
            user_message_ids.append(message.message_id)
            user_message_ids.append(message.message_id+1)

        else:
            wrong_answers += 1
            error = 0
            await message.answer(f'Правильный ответ : <b>{value.upper()}</b>.\nЗапомни и повтори!', parse_mode='html')
            user_message_ids.append(message.message_id)
            user_message_ids.append(message.message_id+1)
            await asyncio.sleep(1)


# Функция для отправки следующего вопроса с переводом ENG-RUS

async def send_question_eng(message: types.Message, state: FSMContext, user_id: int):
    global user_answer
    if user_answer == 'data_eng':
        dictionary = data_list
    if user_answer == 'adverb_eng':
        dictionary = adverb_list
    if user_answer == 'other_eng':
        dictionary = other_list
    key, value = random.choice(list(dictionary.items()))
    await message.answer(f'Введите перевод:\n\n{key}  --->')
    user_message_ids.append(message.message_id)
    user_message_ids.append(message.message_id+2)
    user_states[user_id] = MyStates.QUESTION
    await state.set_state(MyStates.QUESTION)
    await dp.current_state(user=user_id).update_data(key=key, value=value)

# Выбираем словарь


@dp.callback_query_handler(lambda query: query.data == 'data_eng' or query.data == 'adverb_eng' or query.data == 'other_eng')
async def play_eng_rus(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    global user_answer
    user_answer = callback_query.data
    await callback_query.message.answer('Отлично! Давай начнем 💬.\n\nДля завершения тренировки напиши слово - "stop"')
    user_message_ids.append(callback_query.message.message_id+1)
    await asyncio.sleep(1)
    await send_question_eng(callback_query.message, state, user_id)
    user_states[user_id] = MyStates.QUESTION
    await asyncio.sleep(1)

# Обработчик текстовых сообщений


@dp.message_handler(state=MyStates.QUESTION, content_types=types.ContentTypes.TEXT)
async def check_answer(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    if state == MyStates.QUESTION:
        await process_answer_eng(message, user_id)
    else:
        await message.answer('Сбой состояний!')


async def process_answer_eng(message: types.Message, user_id: int):
    global correct_answers, wrong_answers, error, finish
    state = dp.current_state(user=user_id)
    state_data = await state.get_data()
    key = state_data.get('key')
    value = state_data.get('value')
    print(key, value)
    user_answer = message.text.strip()

    if finish == 10:
        await message.answer('Тренировка окончена!\n ... Идёт чистка чата!')
        user_message_ids.append(message.message_id)
        user_message_ids.append(message.message_id+1)
        finish = 0
        await asyncio.sleep(5)
        await show_results(message)
        await state.finish()
        return

    elif user_answer.lower() == 'stop':
        finish = 0
        await message.answer('Тренировка окончена!\n ... Идёт чистка чата!')
        user_message_ids.append(message.message_id)
        user_message_ids.append(message.message_id+1)
        await asyncio.sleep(1)
        await show_results(message)
        await state.finish()
        return

    elif value is not None and user_answer.lower() == value.lower():
        correct_answers += 1
        finish += 1
        error = 0
        await message.answer('✅ Верно!')
        await send_question_eng(message, state, user_id)
        user_message_ids.append(message.message_id+1)

    else:
        if error < 1:
            error += 1
            await message.answer('❌' + random_phrase)
            user_message_ids.append(message.message_id)
            user_message_ids.append(message.message_id+1)

        else:
            wrong_answers += 1
            error = 0
            await message.answer(f'Правильный ответ : <b>{value.upper()}</b>.\nЗапомни и повтори!', parse_mode='html')
            user_message_ids.append(message.message_id)
            user_message_ids.append(message.message_id+1)
            await asyncio.sleep(1)

# Обработчик результата


async def show_results(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(types.InlineKeyboardButton('RUS-ENG', callback_data='RUS-ENG'),
               types.InlineKeyboardButton('ENG-RUS', callback_data='ENG-RUS'))
    markup.row(types.InlineKeyboardButton(
        'Показать словарь', callback_data='all_dic'), types.InlineKeyboardButton(
        'Пополнить словарь', callback_data='NONE'))
    for message_id in user_message_ids:
        try:
            await bot.delete_message(chat_id, message_id)
            print(message_id)
        except Exception as e:
            pass
    user_message_ids.clear()
    await message.answer(f'Правильных ответов: {correct_answers}\nНеправильных ответов: {wrong_answers}', reply_markup=markup)
# await bot.send_video(message.chat.id, video=open('NdR.mp4', 'rb'), caption='Красавчик!')


def register_handlers_trening_words(dp: Dispatcher):

    dp.register_callback_query_handler(
        dictionary_rus, lambda query: query.data == 'RUS-ENG' or query.data == 'ENG-RUS')
    # dp.register_callback_query_handler(dictionary_eng, lambda query: query.data == 'ENG-RUS')
