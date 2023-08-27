from aiogram import types, Dispatcher
from create_bot import dp
import json
import asyncio

# Загружаем данные со словами и их переводами из файла read.json
with open('text.json', 'r', encoding='utf-8') as file:
    data_text = json.load(file)


read_key = list(data_text.keys())
read_value = list(data_text.values())


# Обработчик кнопки /read


# @ dp.message_handler(commands=['read'])
async def read_book(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=3)
    bt1 = types.InlineKeyboardButton('Моя семья', callback_data='clik_0')
    bt2 = types.InlineKeyboardButton('Школьные обеды', callback_data='clik_1')
    bt3 = types.InlineKeyboardButton('Жираф', callback_data='clik_2')
    markup.row(bt2).row(bt1, bt3)
    await callback_query.message.answer('Выбери рассказ:', reply_markup=markup)
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


def register_handlers_read(dp: Dispatcher):

    dp.register_callback_query_handler(
        read_book, lambda query: query.data == 'read')
