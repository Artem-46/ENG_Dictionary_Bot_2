from aiogram import types, Dispatcher
from create_bot import dp
import json

# Загружаем данные со словами и их переводами из файла read.json
with open('data.json', 'r', encoding='utf-8') as file:
    data_dic = json.load(file)

with open('adverb.json', 'r', encoding='utf-8') as file:
    adverb_dic = json.load(file)

with open('other.json', 'r', encoding='utf-8') as file:
    other_dic = json.load(file)

user_message_ids = []

# Обработчик команды /all_dic

# @dp.callback_query_handler(lambda query: query.data == 'all_dic')


async def all_dictionary(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(row_width=3)
    bt1 = types.InlineKeyboardButton('Глаголы', callback_data='data_dic')
    bt2 = types.InlineKeyboardButton('Предлоги', callback_data='adverb_dic')
    bt3 = types.InlineKeyboardButton('Прочие слова', callback_data='other_dic')
    markup.row(bt1, bt2, bt3)
    await callback_query.message.edit_text('Выбери словарь:', reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data == 'data_dic' or query.data == 'adverb_dic' or query.data == 'other_dic')
async def all_dictionary_data(callback_query: types.CallbackQuery):
    user_answer_dic = callback_query.data
    if user_answer_dic == 'data_dic':
        dictionary, dic_name = data_dic, 'Глаголы'
    if user_answer_dic == 'adverb_dic':
        dictionary, dic_name = adverb_dic, 'Предлоги'
    if user_answer_dic == 'other_dic':
        dictionary, dic_name = other_dic, 'Прочие слова'
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(types.InlineKeyboardButton('RUS-ENG', callback_data='data_rus'),
               types.InlineKeyboardButton('ENG-RUS', callback_data='data_eng'))
    text = '\n'.join([f'{key}  -->  {value}' for key,
                     value in dictionary.items()])
    await callback_query.message.answer(f'{dic_name}:\n\n{text}\n\nЗакрепить знания:', reply_markup=markup)


def register_handlers_all_dic(dp: Dispatcher):

    dp.register_callback_query_handler(
        all_dictionary, lambda query: query.data == 'all_dic')
