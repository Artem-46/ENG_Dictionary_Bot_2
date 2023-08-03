from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from aiogram import types

import random
import json
import asyncio


async def on_startup(_):
    print('Бот вышел в онлайн')

# Загружаем данные со словами и их переводами из файла dic.json
with open('dic.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

with open('read.json', 'r', encoding='utf-8') as file:
    read_dic = json.load(file)

read_key = list(read_dic.keys())
read_value = list(read_dic.values())

correct_answers = 0
wrong_answers = 0
error = 0

# Инициализируем бота и диспетчер
# @dictionary_46Bot
bot = Bot('6368563334:AAFOKxjgPVBe7JVIsfXTQa705txgSLSz97s')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определяем состояния (states)


class MyStates:
    QUESTION = 'question'
    QUESTION_RUS = 'question_rus'

# Функция для отправки следующего вопроса с переводом


async def send_question(message: types.Message):
    key, value = random.choice(list(data.items()))
    await message.answer(f'{key}  --->\nВведите перевод:',  parse_mode='html')
    await dp.current_state(user=message.from_user.id).set_state('question')
    await dp.current_state(user=message.from_user.id).update_data(key=key, value=value)

# Обработчик команды /start


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('/ENG-RUS',))
    markup.add(types.KeyboardButton('/RUS-ENG'))
    markup.add(types.KeyboardButton('NEW WORD'))
    markup.add(types.KeyboardButton('/show_dict'))
    await message.answer(f'Привет, {message.from_user.first_name} 🖐️!\nЯ буду задавать слова, и ты должен написать их перевод.\nТы готов? Выбери режим тренировки 🎰.', reply_markup=markup)

# Обработчик команды /show_dict


@dp.message_handler(commands=['show_dict'])
async def show_dictionary(message: types.Message):
    # Создаем текстовое сообщение со всеми словами и их переводами из словаря
    text = '\n'.join([f'{key} --> {value}' for key, value in data.items()])
    await message.answer(f'Вот весь словарь:\n\n{text}')

# Обработчик команды /RUS-ENG


@dp.message_handler(commands=['RUS-ENG'])
async def play(message: types.Message):
    await message.answer('Отлично! Давай начнем 💬.')
    await message.answer('Для завершения тренировки напиши слово - "stop"')
    await asyncio.sleep(1)
    await send_question(message)
    await dp.current_state(user=message.from_user.id).set_state(MyStates.QUESTION)
    await asyncio.sleep(1)

# Обработчик текстовых сообщений


@dp.message_handler(state=MyStates.QUESTION, content_types=types.ContentTypes.TEXT)
async def check_answer(message: types.Message, state: FSMContext):
    global correct_answers, wrong_answers, error
    state_data = await state.get_data()
    key = state_data.get('key')
    value = state_data.get('value')
    if key is None or value is None:
        await message.answer('Произошла ошибка. Начни игру снова, написав /play.')
        await state.finish()
        return

    user_answer = message.text.strip()

    if user_answer.lower() == value.lower():
        correct_answers += 1
        error = 0
        await message.answer('✅ Верно!')
        await send_question(message)

    elif user_answer.lower() == 'stop':
        await message.answer('Тренировка окончена!')
        await asyncio.sleep(1)
        await show_results(message)
        await state.finish()
        return

    else:
        if error < 1:
            error += 1
            await message.answer('❌ Попробуй еще раз.')

        else:
            wrong_answers += 1
            error = 0
            await message.answer(f'{message.from_user.first_name}, не тупи!')
            await message.answer('🤦')
            await message.answer(f'Правильный ответ : <b>{value.upper()}</b>', parse_mode='html')
            await asyncio.sleep(1)
            await send_question_rus(message)


async def show_results(message: types.Message):
    await message.answer(f'Правильных ответов: {correct_answers}\nНеправильных ответов: {wrong_answers}')
    await bot.send_video(message.chat.id, video=open('NdR.mp4', 'rb'), caption='Красавчик!')


async def send_question_rus(message: types.Message):
    eng_rus_data = {value: key for key, value in data.items()}
    key, value = random.choice(list(eng_rus_data.items()))
    await message.answer(f'{key}  --->\nВведите перевод:',  parse_mode='html')
    await dp.current_state(user=message.from_user.id).set_state('question')
    await dp.current_state(user=message.from_user.id).update_data(key=key, value=value)

# Обработчик команды /ENG-RUS


@dp.message_handler(commands=['ENG-RUS'])
async def play(message: types.Message):
    await message.answer('Отлично! Давай начнем 💬.')
    await message.answer('Для завершения тренировки напиши слово - "stop"')
    await asyncio.sleep(1)
    await send_question_rus(message)
    await dp.current_state(user=message.from_user.id).set_state(MyStates.QUESTION_RUS)
    await asyncio.sleep(1)

# Обработчик текстовых сообщений


@dp.message_handler(state=MyStates.QUESTION_RUS, content_types=types.ContentTypes.TEXT)
async def check_answer(message: types.Message, state: FSMContext):
    global correct_answers, wrong_answers, error
    state_data = await state.get_data()
    key = state_data.get('key')
    value = state_data.get('value')
    if key is None or value is None:
        await message.answer('Произошла ошибка. Начни игру снова, написав /play.')
        await state.finish()
        return

    user_answer = message.text.strip()

    if user_answer.lower() == value.lower():
        correct_answers += 1
        error = 0
        await message.answer('✅ Верно!')
        await send_question_rus(message)

    elif user_answer.lower() == 'stop':
        await message.answer('Тренировка окончена!')
        await asyncio.sleep(1)
        await show_results(message)
        await state.finish()
        return

    else:
        if error < 1:
            error += 1
            await message.answer('❌ Попробуй еще раз.')

        else:
            wrong_answers += 1
            error = 0
            await message.answer(f'{message.from_user.first_name}, не тупи!')
            await message.answer('🤦')
            await message.answer(f'Правильный ответ : <b>{value.upper()}</b>', parse_mode='html')
            await asyncio.sleep(1)
            await send_question_rus(message)

# Обработчик кнопки /read


@ dp.message_handler(commands=['read'])
async def read_book(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    bt1 = types.InlineKeyboardButton('Моя семья', callback_data='clik_0')
    bt2 = types.InlineKeyboardButton('Школьные обеды', callback_data='clik_1')
    bt3 = types.InlineKeyboardButton('Жираф', callback_data='clik_2')
    markup.row(bt2).row(bt1, bt3)
    await message.answer('Выбери рассказ:', reply_markup=markup)
    await asyncio.sleep(1)


@ dp.callback_query_handler(lambda query: query.data == 'clik_0')
async def clik_0_callback(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_wight=1)
    markup.add(types.InlineKeyboardButton(
        'Показать перевод', callback_data='tyt_2'))
    await callback_query.message.answer(read_key[0], reply_markup=markup)


@ dp.callback_query_handler(lambda query: query.data == 'clik_1')
async def clik_1_callback(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_wight=1)
    markup.add(types.InlineKeyboardButton(
        'Показать перевод', callback_data='tyt_2'))
    await callback_query.message.answer(read_key[1], reply_markup=markup)


@ dp.callback_query_handler(lambda query: query.data == 'clik_2')
async def clik_2_callback(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_wight=1)
    markup.add(types.InlineKeyboardButton(
        'Показать перевод', callback_data='tyt_2'))
    await callback_query.message.answer(read_key[2], reply_markup=markup)


@ dp.callback_query_handler(lambda query: query.data == 'tyt_0')
async def tyt_0(callback_query: types.CallbackQuery):
    await callback_query.message.answer(read_value[0])


@ dp.callback_query_handler(lambda query: query.data == 'tyt_1')
async def tyt_1(callback_query: types.CallbackQuery):
    await callback_query.message.answer(read_value[1])


@ dp.callback_query_handler(lambda query: query.data == 'tyt_2')
async def tyt_2(callback_query: types.CallbackQuery):
    await callback_query.message.answer(read_value[2])

# Запускаем бота

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup)


# await asyncio.sleep(2)
#       await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
