
from aiogram import types, Dispatcher
from admin_id import admin
from create_bot import dp, bot, db

# command to view all users
async def get_all_users(message: types.Message):
    if message.from_user.id == admin:
        users = db.get_all_users()
        for user in  users:
            text = f"Name: {user[3]}\nUser_id: {user[1]}\nStatus: {user[2]}"
            await bot.send_message(admin, text)
    else:
        await message.answer("You aren't the admin!")


# command to send any message from admin
async def newsletter(message: types.Message):
    if message.from_user.id == admin:
        text = message.text[6:]
        users = db.get_users()
        for row in users:
            try:
                await bot.send_message(row[1], text)
            except:
                db.update_status(row[1], 0)
            await bot.send_message(message.from_user.id, "successfully")


def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(get_all_users, commands=["users"])
    dp.register_message_handler(newsletter, commands=["send"])
