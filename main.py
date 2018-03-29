# Установленные модули
import re
import telebot
import logging.config

# Модули, созданные в ходе разработки.
import api_connection
from constants import ConstantsToken, ConstantsAnswers, Genres, LoggerConfig
from database import Base
from keyboard import *
from errors import FilmNotFound
from formatters import *

bot = telebot.TeleBot(ConstantsToken.TEST_API_TOKEN)
db = Base()

logging.config.dictConfig(LoggerConfig.dictLogConfig)
logger = logging.getLogger("console_logger")


@bot.message_handler(commands=["start"])
def show_start_message(message):
    bot.send_message(message.chat.id, ConstantsAnswers.GREETING_MSG, reply_markup=create_main_markup())


@bot.message_handler(content_types=["text"], func=lambda message: message.text == Commands.SEARCH_FILM_COMMAND)
def search_movie_command(message):
    logger.debug("NEW SEARCH REQUEST BY USER " + str(message.chat.id))
    db.create_new_search_request(message.chat.id, message.message_id + 1)
    bot.send_message(message.chat.id, ConstantsAnswers.SEARCH_MSG,
                     reply_markup=create_genres_keyboard())


@bot.message_handler(content_types=["text"], regexp=Commands.ID_FILM_RE)
def get_film_by_id(message):
    film_id = int(re.match(Commands.ID_FILM_RE, message.text).group("film_id"))

    logger.debug("NEW REQUEST TO FIND FILM BY ID " + str(film_id))

    api = api_connection.APIMethods()
    current_film = api.get_film_by_id(film_id)
    answer = format_text_one(current_film)

    is_favorite = True

    users_favorite_films = db.get_favorite_films(message.chat.id)

    if users_favorite_films is None:
        pass
    elif film_id in users_favorite_films:
        is_favorite = False

    if is_favorite:
        bot.send_message(message.chat.id, answer, parse_mode="Markdown",
                        reply_markup=create_favorite_markup(film_id),
                        disable_web_page_preview=False)
    else:
        bot.send_message(message.chat.id, answer, parse_mode="Markdown",
                         reply_markup=create_del_favorite_markup(film_id),
                         disable_web_page_preview=False)

    db.new_request_count(message.chat.id)


@bot.message_handler(content_types=["text"], func=lambda message: message.text == Commands.TOP_FILMS_COMMAND)
def show_top_films(message):
    # ""
    #     Метод, выводящий топовые фильмы.
    # 
    # :param message:
    # :return: 0
    # ""
    api = api_connection.APIMethods()

    top_rated = api.get_top_rated()
    top_rated_results = top_rated["results"]

    f_top_rated_res = format_text(top_rated_results[0])
    f_top_rated_id = top_rated_results[0]["id"]

    set_favorite = True

    db.new_film_list(message.chat.id, message.message_id, top_rated_results)

    user_favorite_films = db.get_favorite_films(message.chat.id)

    if user_favorite_films is None:
        pass
    elif f_top_rated_id in user_favorite_films:
        set_favorite = False

    if set_favorite:
        bot.send_message(message.chat.id, f_top_rated_res,
                         parse_mode="Markdown", reply_markup=combine_add_favorite_and_slide(f_top_rated_id))
    else:
        bot.send_message(message.chat.id, f_top_rated_res,
                         parse_mode="Markdown", reply_markup=combine_del_favorite_and_slide(f_top_rated_id))

@bot.message_handler(content_types=["text"], func=lambda message: message.text == Commands.UPCOMING_FILMS_COMMAND)
def show_upcoming_films(message):
    api = api_connection.APIMethods()
    upcoming = api.get_movie_upcoming()
    f_upcoming_film = upcoming["results"]
    f_upcoming_film_text = format_text(f_upcoming_film[0])
    db.new_film_list(message.chat.id, message.message_id, f_upcoming_film)
    logger.debug("NEW REQUEST ON UPCOMING FILMS BY USER ID " + str(message.chat.id))
    bot.send_message(message.chat.id, f_upcoming_film_text,
                     parse_mode="Markdown",
                     reply_markup=create_list_movies_inline_keyboard(),
                     disable_web_page_preview=False)


@bot.message_handler(content_types=["text"], func=lambda message: message.text == Commands.GET_BACK_COMMAND)
def get_back_menu(message):
    bot.send_message(message.chat.id, "Выберите", reply_markup=create_main_markup())


@bot.message_handler(content_types=["text"],func=lambda message: message.text == Commands.POPULAR_FILMS_COMMAND)
def get_most_popular(message):
    api = api_connection.APIMethods()
    most_popular_films = api.get_most_popular()
    db.new_film_list(message.chat.id, message.message_id, most_popular_films["results"])
    logger.debug("NEW REQUEST FOR POPULAR FILMS BY USER " + str(message.chat.id))
    f_most_popular_film = most_popular_films["results"][0]
    answer = format_text(f_most_popular_film)

    set_favorite = True
    user_favorite_films = db.get_favorite_films(message.chat.id)

    if user_favorite_films is None:
        pass
    elif f_most_popular_film["id"] in user_favorite_films:
        set_favorite = False

    if set_favorite:
        bot.send_message(message.chat.id, answer,
                         reply_markup=combine_add_favorite_and_slide(f_most_popular_film["id"]),
                        parse_mode="Markdown", disable_web_page_preview=False)
    else:
        bot.send_message(message.chat.id, answer,
                         reply_markup=combine_del_favorite_and_slide(f_most_popular_film["id"]),
                         parse_mode="Markdown", disable_web_page_preview=False)

@bot.message_handler(content_types=["text"], func=lambda message: message.text == Commands.USER_FAVORITE_COMMAND)
def show_favorite_film(message):

    user_favorite_films = db.get_favorite_films_w_title(message.from_user.id)

    if user_favorite_films:
        answer = format_favorite_films(user_favorite_films)
    else:
        answer = ConstantsAnswers.NO_FAVORITE_FILMS
    bot.send_message(message.chat.id, answer, parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def search_film_by_title(message):
    """

    :param message:
    :return:
    """

    # Определяем переменную для поиска фильма. Т.е выделяем текст из информации по сообщению
    film_to_find = message.text

    api = api_connection.APIMethods()
    logger.debug("NEW REQUEST TO SEARCH FILM")

    try:
        result = api.get_movie_by_title(film_to_find)
    except FilmNotFound:
        answer = ConstantsAnswers.FILM_NOT_FOUNDED_EDITABLE.format(message.text)
        image_poster = ""
        results = ConstantsAnswers.FILM_NOT_FOUNDED_EDITABLE.format(message.text)
        is_board_active = False
    else:
        list_of_results = result["results"]
        db.new_film_list(message.chat.id, message.message_id, list_of_results)
        current_result = result["results"][0]
        image_path = current_result["poster_path"]
        image_poster = api.get_image_url(image_path)

        answer = format_text(current_result)



        results = complite_results(result)

    bot.send_message(message.chat.id, results,
                         parse_mode="Markdown",
                     disable_web_page_preview=False)


@bot.callback_query_handler(func=lambda call: call.data == Commands.PREV_PAGE_COMMAND or
                            call.data == Commands.NEXT_PAGE_COMMAND)
def slide_message(call):
    correct_message_id = call.message.message_id - 1
    list_user_movies = db.get_user_movie_list(call.from_user.id, call.message.message_id)
    logger.debug("NEW SLIDE")
    arrays_of_films = list_user_movies[2]

    set_favorite = True

    try:
        current_page = list_user_movies[-1]
    except TypeError:
        return 0

    if call.data == Commands.PREV_PAGE_COMMAND:
        current_page = list_user_movies[-1] - 1

        if current_page < 0:  # len(list_user_movies[2]):
            current_page = len(list_user_movies[2]) - 1
            current_text_on_page = list_user_movies[2][current_page]
        else:
            current_text_on_page = format_text(list_user_movies[2][current_page])

        current_film_data = list_user_movies[2][current_page]

    else:
        current_page = list_user_movies[-1] + 1
        if current_page >= len(arrays_of_films):
            current_page = 0
            current_text_on_page = format_text(list_user_movies[2][current_page])
        else:
            current_text_on_page = format_text(list_user_movies[2][current_page])

        current_film_data = list_user_movies[2][current_page]

    logger.debug("USER " +  str(call.from_user.id) + " SLIDED " + str(correct_message_id) + " TO " + str(current_page))
    db.update_position_film_list(call.from_user.id, correct_message_id, current_page)

    logger.debug("NOW SENT " +  str(current_text_on_page[:10])  + " ...")

    user_favorite_films = db.get_favorite_films(call.from_user.id)

    if user_favorite_films is None:
        pass
    elif current_film_data["id"] in user_favorite_films:
        set_favorite = False

    if set_favorite:
        bot.edit_message_text(current_text_on_page, list_user_movies[0], list_user_movies[1] + 1,
                              reply_markup=combine_add_favorite_and_slide(current_film_data["id"]),
                              parse_mode="Markdown",
                              disable_web_page_preview=False)
    else:
        bot.edit_message_text(current_text_on_page, list_user_movies[0], list_user_movies[1] + 1,
                              reply_markup=combine_del_favorite_and_slide(current_film_data["id"]),
                              parse_mode="Markdown",
                              disable_web_page_preview=False)



@bot.callback_query_handler(func=lambda call: re.match(Commands.ADD_FAVORITE_COMMAND, call.data) != None)
def add_favorite_film(call):
    film_id = int(re.match( Commands.ADD_FAVORITE_COMMAND, call.data).group("film_id"))
    user_id = call.from_user.id
    film_title = call.message.text.split(Smiles.YEAR)[0][1:].strip()

    users_favorite_films = db.get_favorite_films(user_id)

    if users_favorite_films:
        if  film_id in users_favorite_films:
            return 0

    logger.debug("NEW FAVORITE FILM " + str(film_id) + " FROM USER " + str(user_id))

    db.add_new_favorite_film(user_id, film_id, film_title)

    is_slider = db.get_user_movie_list(user_id, call.message.message_id) is not None

    if is_slider:
        bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,
                                      reply_markup=combine_del_favorite_and_slide(film_id))
    else:
        bot.edit_message_reply_markup(call.message.chat.id,call.message.message_id,
                                      reply_markup=create_del_favorite_markup(film_id))


@bot.callback_query_handler(func=lambda call: re.match(Commands.DEL_FAVORITE_COMMAND, call.data) != None)
def del_favorite_film(call):
    film_id = int(re.match(Commands.DEL_FAVORITE_COMMAND, call.data).group("film_id"))
    user_id = call.from_user.id

    logger.debug("DEL FAVORITE FILM " + str(film_id) + " FROM USER " + str(user_id))
    db.del_favorite_film(user_id, film_id)

    is_slider = db.get_user_movie_list(user_id, call.message.message_id) is not None

    if is_slider:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=combine_add_favorite_and_slide(film_id))
    else:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=create_favorite_markup(film_id))


@bot.callback_query_handler(func=lambda call: re.match(Commands.ID_GENRE_RE, call.data) is not None)
def add_new_genre_to_search(call):
    current_genre_id = int(re.match(Commands.ID_GENRE_RE, call.data).group("genre_id"))
    logger.debug("TRY TO ADD NEW GENRE " + str(current_genre_id) + " TO USER " + str(call.from_user.id))

    all_genres_in_request = db.get_all_genres_for_user(call.from_user.id, call.message.message_id)[0]

    if current_genre_id in all_genres_in_request:
        logger.debug("GENRE " + str(current_genre_id) + " ALREADY ADDED TO USER " + str(call.from_user.id))
        # TODO: Сделать откат выбранных жанров.
        return 0

    all_genres_in_request.append(current_genre_id)
    db.add_new_genre_for_user(call.from_user.id, call.message.message_id, current_genre_id)
    text_to_answer = format_genres(all_genres_in_request)

    # TODO: Добавить обновление клавиатуры с галочкой
    bot.edit_message_text(text_to_answer, call.message.chat.id, call.message.message_id,
                          parse_mode="Markdown",
                          reply_markup=create_genres_keyboard())
    logger.debug(" GENRE ADDED TO REQUEST USER " + str(call.message.message_id) + str(call.from_user.id))


@bot.callback_query_handler(func=lambda call: re.match(Commands.COMPLITE_SEARCH_COOMMAND_INLINE, call.data) is not None)
def complite_search_genres(call):
    # Метод, осуществляющий поиск по заданным параментрам в сообщении.
    all_user_genres = db.get_all_genres_for_user(call.from_user.id, call.message.message_id)[0]

    logger.debug("TRY TO MAKE SEARCH ON USER " + str(call.from_user.id) + " AND MSG_ID " + str(call.message.message_id))
    if len(all_user_genres) > 0:
        all_user_genres = [str(j) for j in db.get_all_genres_for_user(call.from_user.id, call.message.message_id)[0]]
    else:
        # TODO: Вывести сообщение о том, что юзер ничего не выбрал через
        # TODO: оповещения в диалоге. bot.notification
        return 0

    result = api_connection.APIMethods().get_movie_by_params(with_genres=",".join(all_user_genres))
    answer_text = complite_results(result) # Формирование текста

    logger.debug("SEARCH ON USER " + str(call.from_user.id) + " AND MSG_ID " + str(call.message.message_id) + " COMPLITED")
    bot.edit_message_text(answer_text,
                          call.message.chat.id, call.message.message_id,
                          parse_mode="Markdown")

    db.destroy_request(call.from_user.id, call.message.message_id) # Удаление запроса из БД.


if __name__ == "__main__":
    bot.polling(none_stop=True)