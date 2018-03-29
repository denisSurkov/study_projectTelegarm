import os
import json
import logging


class Base:
    def __init__(self):
        from urllib import parse
        import psycopg2

        self.logger = logging.getLogger("db_logger")


        # Конфигурация для heroku

        parse.uses_netloc.append("postgres")
        url = parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )


        # self.logger.debug("TRY TO CONNECT")
        # self.connection = psycopg2.connect(
        #     database="postgres",
        #     user="postgres",
        #     password="12345",
        #     host="localhost",
        #     port="5432"
        # )

        self.cursor = self.connection.cursor()
        self._create_tables()
        self.logger.debug("DB CONNECTED. START TO WORK")

    def _create_tables(self):
        # Таблица для листов фильмов
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS film_lists (
                                                            chat_id BIGINT,
                                                            message_id BIGINT,
                                                            list_movies JSON,
                                                            current_position INT)""")
        self.connection.commit()

        # Таблица любимых фильмов
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS user_favorite_films (
                                                                user_id BIGINT, 
                                                                film_id BIGINT,
                                                                film_title TEXT
                                                                )""")
        self.connection.commit()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS user_request_search (
                                                            user_id BIGINT,
                                                            message_id BIGINT,
                                                            genres_list JSON)""")
        self.connection.commit()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS counter(user_id BIGINT)""")
        self.logger.debug("TABLES CREATED")

    def test_it(self):
        # dumped_json = json.dumps([{"title": "Зеленый фонарь", "runtime": "90"}, {"title": "Зеленая миля"}])
        #
        # self.cursor.execute("INSERT INTO film_lists VALUES ({0},{1}, '{2}', {3})".format(
        #     519661997, 966, dumped_json, 0
        # ))
        self.connection.commit()
        self.cursor.execute("SELECT * FROM film_lists")
        answ = self.cursor.fetchall()

        return answ

    def _drop_table(self):
        self.cursor.execute("DROP TABLE film_lists")
        self.connection.commit()
        self.cursor.execute("DROP TABLE user_favorite_films")
        self.connection.commit()
        self.cursor.execute("DROP TABLE user_request_search")
        self.connection.commit()
        self.logger.warning("DB DROPPED!")

    def new_film_list(self, chat_id, message_id, list_of_movie, correct_position=0):
        correct_list = json.dumps(list_of_movie)

        self.cursor.execute("INSERT INTO film_lists VALUES ({0}, {1}, '{2}', {3})".format(chat_id,
                                                                                          message_id,
                                                                                          str(correct_list).replace("'", " "),
                                                                                          correct_position))
        self.logger.debug("NEW USER_MOVIE_LIST " + str(chat_id) + " " + str(message_id))
        self.connection.commit()

    def update_position_film_list(self, chat_id, message_id, position):
        self.cursor.execute("""UPDATE film_lists SET current_position = {0} 
                                WHERE chat_id = {1} and message_id = {2}""".format(position, chat_id, message_id))
        self.connection.commit()

    def get_user_movie_list(self, chat_id, message_id):
        self.cursor.execute("SELECT * FROM film_lists WHERE message_id = {0} and chat_id = {1}".format(message_id - 1,
                                                                                                       chat_id))

        result = self.cursor.fetchone()
        return result

    def add_new_favorite_film(self, user_id, film_id, film_title):
        self.cursor.execute("INSERT INTO user_favorite_films VALUES({0}, {1}, '{2}')".format(user_id,
                                                                                           film_id,
                                                                                           film_title))
        self.logger.debug("NEW FAVORITE FILM ID " + str(film_id) + " ON USER " + str(user_id))
        self.connection.commit()

    def del_favorite_film(self, user_id, film_id):
        self.cursor.execute("DELETE FROM user_favorite_films WHERE user_id={0} and film_id={1}".format(user_id,
                                                                                                       film_id))
        self.connection.commit()

    def get_favorite_films(self, user_id):
        self.cursor.execute("SELECT film_id FROM user_favorite_films WHERE user_id={0}".format(user_id))


        # self.connection.commit()

        ans = self.cursor.fetchall()
        if len(ans) == 0:
            return None
        ans = [j[0] for j in ans]
        return ans

    def get_favorite_films_w_title(self, user_id):
        self.cursor.execute("SELECT film_title, film_id FROM user_favorite_films WHERE user_id={0}".format(user_id))
        ans = self.cursor.fetchall()
        if len(ans) == 0:
            return None
        ans = [j for j in ans]
        return ans

    def create_new_search_request(self, user_id, message_id):
        clear_list_request = json.dumps([])
        self.cursor.execute("INSERT INTO user_request_search VALUES ({0}, {1}, '{2}')".format(user_id,
                                                                                            message_id,
                                                                                            clear_list_request))
        self.logger.debug("NEW USER REUQEST SEARCH CREATED: INFO - " + str(user_id) + " " + str(message_id))
        self.connection.commit()

    def get_all_genres_for_user(self, user_id, message_id):
        self.cursor.execute("SELECT genres_list FROM user_request_search WHERE user_id = {0} and message_id = {1}".format(
                                                                                user_id, message_id))
        result = self.cursor.fetchone()
        return result

    def add_new_genre_for_user(self, user_id, message_id, genre_id):
        # TODO: Сделать проверку на этой стороне, а не на стороне main
        genres_list = self.get_all_genres_for_user(user_id, message_id)[0]
        genres_list.append(genre_id)
        self.logger.debug("NEW DATA " + str(genres_list))
        self.cursor.execute("UPDATE user_request_search SET genres_list='{0}' WHERE user_id={1} and message_id={2}".format(
            genres_list, user_id, message_id))
        self.logger.debug("CORRECT genre_list = " + str(genres_list) + " TO USER " + str(user_id) + " AND MES ID " + str(message_id))
        self.connection.commit()

    def destroy_request(self, user_id, message_id):
        self.cursor.execute("DELETE FROM user_request_search WHERE user_id={0} and message_id={1}".format(
            user_id, message_id
        ))
        self.logger.debug("USER REQUEST SEARCH WITH USER ID " + str(user_id) + " AND MSG ID " + str(message_id) + "DESTROYED")
        self.connection.commit()

    def new_request_count(self, user_id):
        self.cursor.execute("INSERT INTO counters VALUES ({0})".format(user_id))
        self.connection.commit()
        self.logger.debug("METRICS - COUNTER: NEW USER REQUEST " + str(user_id))

if __name__ == "__main__":
    # Тест часть
    db = Base()
    db._drop_table()
    db._create_tables()