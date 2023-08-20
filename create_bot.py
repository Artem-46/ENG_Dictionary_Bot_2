from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import openai

storage = MemoryStorage()

# Инициализируем бота и диспетчер
# @dictionary_46Bot
bot = Bot('6368563334:AAFOKxjgPVBe7JVIsfXTQa705txgSLSz97s')
dp = Dispatcher(bot, storage=storage)

# API GPT 2
openai.api_key = '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' 