from aiogram import Bot, Dispatcher
#from config import *
from database import SQLighter

BOT_TOKEN = 'your bot token'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
db = SQLighter('bd.db')
