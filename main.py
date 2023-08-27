from handlers import trening_words, other, all_dic, read
from create_bot import dp


async def on_startup(_):
    print('Бот вышел в онлайн')

trening_words.register_handlers_trening_words(dp)
all_dic.register_handlers_all_dic(dp)
read.register_handlers_read(dp)
other.register_handler_other(dp)
# wgpt.register_handlers_gpt(dp)

# Запускаем бота

if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup)
