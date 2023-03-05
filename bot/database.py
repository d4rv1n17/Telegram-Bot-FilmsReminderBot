import sqlite3


class SQLighter:


    def __init__(self, database):
        """connect to the database and save the connection cursor"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()


    def get_all_users(self):
        """getting all bot's userss"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions`", ()).fetchall()


    def get_users(self, status = True):
        """getting all active bot's subscribers"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()


    def user_exists(self, user_id):
        """checking if user exists in database"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))


    def add_user(self, user_id, name, status = True):
        """adding new subscriber"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`, 'name') VALUES(?,?,?)", (user_id, status, name))


    def update_status(self, user_id, status):
        """updating user's subscribe status"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))


    def get_movies(self, user_id):
        """getting movies from user's database"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'favorites' WHERE user_id = ?", (user_id,)).fetchall()


    def add_movie(self, user_id, film_name, release_date):
        """adding movie to user's database"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'favorites' ('user_id', 'film_name', 'release_date') VALUES(?,?,?)", (user_id,film_name,release_date))


    def remove_movie(self, id, user_id):
        """deleting movie from user's database"""
        with self.connection:
            return self.cursor.execute("DELETE FROM 'favorites' WHERE id = ? and user_id = ?", (id, user_id))


    def get_all_movies(self):
        """getting movies from user's database"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'favorites'", ()).fetchall()


    def close(self):
        """closing connection with database"""
        self.connection.close()
