# imports
from aiogram import executor, types
from datetime import datetime
import logging
import asyncio
import aioschedule as schedule
from imdb import Cinemagoer
from text import *
from markups import *
from create_bot import dp, bot, db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests




# logs level
logging.basicConfig(level=logging.INFO)


# imports of files from folders
from handlers import admin
from notificator import reminder_cleaner as rc

admin.register_handlers_admin(dp)

# function to clean to clear obsolete items in the user's favorites
async def on_reminder():
    await rc.cleaner()
    await rc.reminder()


# subscribe command 
@dp.message_handler(commands=["Subscribe✅"])
async def subscribe(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
        # if is no user in db, we just add him
        db.add_user(message.from_user.id, message.from_user.first_name)
    else:
        # if user exists, we just update subscribe status
        db.update_status(message.from_user.id, True)
    
    await message.answer(text_subscribe, reply_markup=main_menu)


# unsubscribe command
@dp.message_handler(commands=["Unsubscribe❌"])
async def unsubscribe(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
        # if the user is not in db, we add him to db with inactive subscription
        db.add_user(message.from_user.id, message.from_user.first_name, False)
        await message.answer("You have not subscribed yet")
    else:
        # if user is already in db, we just update his subscription status
        db.update_status(message.from_user.id, False)
        await message.answer(text_unsubscribe, reply_markup=main_menu)


# command to add film to favorites
@dp.message_handler(commands=["addfilm"])
async def add_film_method(message: types.Message):
    await message.answer("Wait for few seconds please...")
    try:
        film_name_from_user = message.text[9:]
        api_key = "k_403m7mo7"
        get_json_filmId = requests.get("https://imdb-api.com/API/Search/" + str(api_key) + "/"  + str(film_name_from_user))
        json_filmID = get_json_filmId.json()
        filmId = json_filmID['results'][0]['id']
        get_json_filmInfo = requests.get("https://imdb-api.com/en/API/Title/" + str(api_key) + "/" + str(filmId))
        json_filmInfo = get_json_filmInfo.json()
        film_name_from_api = json_filmInfo['title']
        release_date_from_api = json_filmInfo['releaseDate']
        user_id = message.from_user.id
        db.add_movie(user_id, film_name_from_api, release_date_from_api)
        await message.answer(film_name_from_api + "\n" + "was added to your favorites!")
    except:
        await message.answer("Sorry, i couldn't find the film, please try again!")


# commands start
@dp.message_handler(commands=["start"])
async def acquaintance_with_bot(message: types.Message):
    text = text_start
    await message.answer(text, reply_markup=subscribe_menu)


# command to add item in favorites
@dp.message_handler(commands=["add"])
async def add(message: types.Message):
    try:
        input_message = message.text[5:].split(':')
        film_name = input_message[0]
        if len(film_name) > 0:
            release_date = input_message[1].strip()
            id_user = message.from_user.id
            db.add_movie(id_user,film_name,release_date)
            await message.answer(film_name + " was added to your favorites!")
        else:
            await message.answer("Film name is empty!")
    except:
        await message.answer("Error, try again, make sure is data in correct format!")


# command to view your items in favorites
@dp.message_handler(commands=["Favorites📁"])
async def get_mov(message: types.Message):
    id_user = message.from_user.id
    mov = db.get_movies(id_user)
    if len(mov) == 0:
        await message.answer("No films found!")
    else:
        for row in mov:
            text = f"Name: {row[2]}\nRelease date: {row[3]}"
            await bot.send_message(id_user, text)
            await bot.send_message(id_user, text='❗️Remove item from favorites❗️', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'❌Remove❌', callback_data=f'del {row[0]}')))


# callback for remove item from favorites
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    data = callback_query.data.replace('del ', '')
    user_id = callback_query.from_user.id
    db.remove_movie(data, user_id)
    text = "Item has been removed from favorites!"   
    await callback_query.answer(text, show_alert=True)  


# bot send to user 25 best ever films
@dp.message_handler(commands=["Top25📊"])
async def top_films(message: types.Message):
    try:
        await message.answer("TOP 25 OF FILMS:")
        moviesDB = Cinemagoer()
        top = moviesDB.get_top250_movies()
        for movie in top[:25]:
            title =  movie['title']
            rating = str(movie['rating'])
            year = str(movie['year'])
            title_clean = title.replace("()", "")
            title_clean2 = title_clean.replace("''", "")
            rating_clean = rating.replace("()", "")
            rating_clean2 = rating_clean.replace("''", "")
            year_clean = year.replace("()", "")
            year_clean2 = year_clean.replace("''", "")
            await message.answer(text=f"Title: {title_clean2}\nRating: {rating_clean2}\nYear: {year_clean2}")
    except:
        await message.answe("Sorry, this command is not working yet!")


#handler
@dp.message_handler()
async def handler(message: types.Message):
    if message.text == "Commands📜":
        await message.answer(text_commands)
    
    elif message.text == "➡️Other":
        await message.answer("Other menu",reply_markup=other_menu)

    elif message.text == "⬅️Main menu":
        await message.answer("Main menu",reply_markup=main_menu)

    elif message.text == "🆘Help":
        await message.answer(text_help)

    else:
        await message.answer("Unknown command!")


# scheduler that runs function on_reminder (string 28)
async def scheduler():
    schedule.every(21600).seconds.do(on_reminder)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())


#start
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


