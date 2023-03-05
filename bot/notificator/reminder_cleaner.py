from create_bot import db, bot
import datetime
from datetime import datetime

#reminder of films 
async def reminder():
    users = db.get_users()
    for user in users:
        movies = db.get_movies(user[1])
        for movie in movies:
            rd = movie[3]
            datetoday = datetime.today()
            from_str_to_date = datetime.strptime(rd, '%Y-%m-%d')
            dif =  from_str_to_date - datetoday
            if dif.days <= 1:
                if dif.days >= 0:
                    await bot.send_message(movie[1], movie[2] + " coming soon!")
            else:
                pass


#cleanup method of released films
async def cleaner():
    movies = db.get_all_movies()
    for movie in movies:
        rd = movie[3]
        today = datetime.today()
        str_to_date = datetime.strptime(rd, '%Y-%m-%d')
        dif =  str_to_date - today
        if dif.days < 0:
            id = movie[0]
            user_id = movie[1]
            db.remove_movie(id, user_id)
        else:
            pass