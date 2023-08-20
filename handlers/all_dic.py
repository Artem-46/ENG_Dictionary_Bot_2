from aiogram import types, Dispatcher
from create_bot import dp
import json

# Загружаем данные со словами и их переводами из файла read.json
with open('data.json', 'r', encoding='utf-8') as file:
    data_dic= json.load(file)

with open('adverb.json', 'r', encoding='utf-8') as file:
    adverb_dic = json.load(file)

with open('other.json', 'r', encoding='utf-8') as file:
    other_dic = json.load(file)

# Обработчик команды /all_dic

#@dp.callback_query_handler(lambda query: query.data == 'all_dic')
async def all_dictionary(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=3)
    bt1 = types.InlineKeyboardButton('Глаголы', callback_data='data_dic')
    bt2 = types.InlineKeyboardButton('Предлоги', callback_data='adverb_dic')
    bt3 = types.InlineKeyboardButton('Прочие слова', callback_data='other_dic')
    markup.row(bt1, bt2, bt3)
    await callback_query.message.edit_text('Выбери словарь:', reply_markup=markup)
    
@dp.callback_query_handler(lambda query: query.data == 'data_dic')
async def all_dictionary_data(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(types.InlineKeyboardButton('RUS-ENG', callback_data='data_rus'), types.InlineKeyboardButton('ENG-RUS', callback_data='data_eng'))
    text = '\n'.join([f'{key}  -->  {value}' for key, value in data_dic.items()])
    await callback_query.message.answer(f'Глаголы:\n\n{text}\n\nЗакрепи знания:', reply_markup=markup)

@dp.callback_query_handler(lambda query: query.data == 'adverb_dic')
async def all_dictionary_adverb(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(types.InlineKeyboardButton('RUS-ENG', callback_data='adverb_rus'), types.InlineKeyboardButton('ENG-RUS', callback_data='adverb_eng'))
    text = '\n'.join([f'{key}  -->  {value}' for key, value in adverb_dic.items()])
    await callback_query.message.answer(f'Плаголы:\n\n{text}\n\nЗакрепи знания:', reply_markup=markup)

@dp.callback_query_handler(lambda query: query.data == 'other_dic')
async def all_dictionary_other(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(types.InlineKeyboardButton('RUS-ENG', callback_data='other_rus'), types.InlineKeyboardButton('ENG-RUS', callback_data='other_eng'))
    text = '\n'.join([f'{key}  -->  {value}' for key, value in other_dic.items()])
    await callback_query.message.answer(f'Прочие слова:\n\n{text}\n\nЗакрепи знания:', reply_markup=markup)

def register_handlers_all_dic(dp : Dispatcher):
	
	dp.register_callback_query_handler(all_dictionary, lambda query: query.data == 'all_dic')
	