from constants import Commands, Smiles, Genres
from telebot import types


def create_main_markup():
    """
        Метод, создающий главную клавиатуру взаимодействия пользователя
        и чат-бота.

    :return: main_markup
    """
    main_markup = types.ReplyKeyboardMarkup()
    main_markup.row(Commands.SEARCH_FILM_COMMAND, Commands.TOP_FILMS_COMMAND)
    main_markup.row(Commands.USER_FAVORITE_COMMAND, Commands.UPCOMING_FILMS_COMMAND, Commands.POPULAR_FILMS_COMMAND)

    return main_markup


def create_search_markup():
    """
        Метод, возвращающий клавиатуру поиска фильмов по определенным
        параметрам.

    :return: search_makrup
    """

    search_markup = types.ReplyKeyboardMarkup()
    search_markup.row(Commands.GENRE_COMMAND)
    search_markup.row(Commands.COUNTRIES_COMMAND, Commands.YEAR_COMMAND)
    search_markup.row(Commands.CLEAR_SETTINGS_COMMAND)
    search_markup.row(Commands.GET_BACK_COMMAND)

    return search_markup

def create_genre_markup():
    """
        Метод, создающий клавиатуру взаимодейтсвия пользователя и
        набором жанров.

    :return: genry_markup
    """
    genry_markup = types.ReplyKeyboardMarkup()
    genry_markup.row(Commands.GENRE_BLOCKBASTER_COMMAND, Commands.GENRE_WEST_COMMAND, Commands.GENRE_DETECTIVE_COMMAND)
    genry_markup.row(Commands.GENRE_DRAMA_COMMAND, Commands.GENRE_HISTORY_COMMAND, Commands.GENRE_COMEDY_COMMAND)
    genry_markup.row(Commands.GENRE_MELODRAMA_COMMAND, Commands.GENRE_TRILLER_COMMAND, Commands.GENRE_FANTASTIC_COMMAND)
    genry_markup.row(Commands.GET_BACK_COMMAND)

    return genry_markup

def create_news_markup():
    """
        Метод, создающий клавиатуру для новостей кино

    :return: telebot.types.ReplyKeyboardMarkup
    """
    news_markup = types.ReplyKeyboardMarkup()
    news_markup.row(Commands.GET_BACK_COMMAND)

    return news_markup

def create_list_movies_inline_keyboard():
    list_movies_inline_keyboard = types.InlineKeyboardMarkup(row_width=2)

    callback_button_next = types.InlineKeyboardButton(text=Smiles.ARROW_RIGHT, callback_data=Commands.NEXT_PAGE_COMMAND)
    callback_button_back = types.InlineKeyboardButton(text=Smiles.ARROW_LEFT, callback_data=Commands.PREV_PAGE_COMMAND)
    list_movies_inline_keyboard.add(callback_button_back, callback_button_next)

    return list_movies_inline_keyboard


def create_games_markup():
    games_markup = types.ReplyKeyboardMarkup()
    games_markup.row(Commands.SEARCH_FILM_BY_ACTOR)
    games_markup.row(Commands.GAME_TRUE_OR_FALSE_COMMAND, Commands.GAME_GUESS_FILM)
    games_markup.row(Commands.GET_BACK_COMMAND)

    return games_markup


def create_marks_markup():
    mark_keyboard = types.InlineKeyboardMarkup()
    like_button = types.InlineKeyboardButton(text=Smiles.THUMBS_UP, callback_data=Commands.NEW_LIKE_COMMAND)
    dislike_button = types.InlineKeyboardButton(text=Smiles.THUMBS_DOWN, callback_data=Commands.NEW_DISLIKE_COMMAND)
    mark_keyboard.add(like_button, dislike_button)

    return mark_keyboard


def combine_marks_and_slides_markup():
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    like_button = types.InlineKeyboardButton(text=Smiles.THUMBS_UP, callback_data=Commands.NEW_LIKE_COMMAND)
    dislike_button = types.InlineKeyboardButton(text=Smiles.THUMBS_DOWN, callback_data=Commands.NEW_DISLIKE_COMMAND)
    keyboard.add(like_button, dislike_button)

    callback_button_next = types.InlineKeyboardButton(text=Smiles.ARROW_RIGHT, callback_data=Commands.NEXT_PAGE_COMMAND)
    callback_button_back = types.InlineKeyboardButton(text=Smiles.ARROW_LEFT, callback_data=Commands.PREV_PAGE_COMMAND)
    keyboard.add(callback_button_back, callback_button_next)

    return keyboard

def combine_slides_and_favorite():
    kb = types.InlineKeyboardMarkup()

    make_favorite = types.InlineKeyboardButton(text=Smiles.HEART + " Добавить в избранное", callback_data="add_favorite")
    kb.add(make_favorite)

    callback_button_next = types.InlineKeyboardButton(text=Smiles.ARROW_RIGHT, callback_data=Commands.NEXT_PAGE_COMMAND)
    callback_button_back = types.InlineKeyboardButton(text=Smiles.ARROW_LEFT, callback_data=Commands.PREV_PAGE_COMMAND)
    kb.add(callback_button_back, callback_button_next)

    return kb


def create_search_inline_keyboard():
    kb = types.InlineKeyboardMarkup()

    countries = types.InlineKeyboardButton(text=Commands.COUNTRIES_COMMAND, callback_data=Commands.OPEN_COUNTRIES_COMMAND)
    years = types.InlineKeyboardButton(text=Commands.YEAR_COMMAND, callback_data=Commands.OPEN_YEARS_COMMAND)
    genres = types.InlineKeyboardButton(text=Commands.GENRE_COMMAND, callback_data=Commands.OPEN_GENRES_COMMAND)

    kb.add(countries, years, genres)

    complite_search = types.InlineKeyboardButton(text=Commands.COMPLITE_SEARCH, callback_data=Commands.COMPLITE_SEARCH_COOMMAND_INLINE)
    kb.add(complite_search)

    return kb

def create_genres_keyboard():
    kb = types.InlineKeyboardMarkup()

    first_b = types.InlineKeyboardButton(text="Детектив", callback_data="add_genre-" + str(Genres.dict_of_genres["Детектив"]))
    second_b = types.InlineKeyboardButton(text="Приключения", callback_data="add_genre-" + str(Genres.dict_of_genres["Приключения"]))
    third_b = types.InlineKeyboardButton(text="Триллер", callback_data="add_genre-" + str(Genres.dict_of_genres["Триллер"]))

    kb.add(first_b, second_b, third_b)

    b1 = types.InlineKeyboardButton(text="Семейный", callback_data="add_genre-" + str(Genres.dict_of_genres["Семейный"]))
    b2 = types.InlineKeyboardButton(text="Боевик", callback_data="add_genre-" + str(Genres.dict_of_genres["Боевик"]))
    b3 = types.InlineKeyboardButton(text="Комедия", callback_data="add_genre-" + str(Genres.dict_of_genres["Комедия"]))

    kb.add(b1, b2, b3)

    complite_search = types.InlineKeyboardButton(text="Выполнить поиск", callback_data="do_search")

    kb.add(complite_search)

    return kb


def create_favorite_markup(film_id):
    kb = types.InlineKeyboardMarkup()

    favorite = types.InlineKeyboardButton(text=Smiles.HEART + " Добавить в избранные",
                                          callback_data="add_favorite-" + str(film_id))
    kb.add(favorite)

    return kb


def create_del_favorite_markup(film_id):
    kb = types.InlineKeyboardMarkup()

    del_favorite = types.InlineKeyboardButton(text=Smiles.BROKEN_HEART + " Убрать из избранных",
                                              callback_data="del_favorite-" + str(film_id))
    kb.add(del_favorite)

    return kb


def combine_add_favorite_and_slide(film_id):
    kb = types.InlineKeyboardMarkup()

    favorite = types.InlineKeyboardButton(text=Smiles.HEART + " Добавить в избранные",
                                          callback_data="add_favorite-" + str(film_id))
    kb.add(favorite)

    callback_button_next = types.InlineKeyboardButton(text=Smiles.ARROW_RIGHT, callback_data=Commands.NEXT_PAGE_COMMAND)
    callback_button_back = types.InlineKeyboardButton(text=Smiles.ARROW_LEFT, callback_data=Commands.PREV_PAGE_COMMAND)
    kb.add(callback_button_back, callback_button_next)

    return kb

def combine_del_favorite_and_slide(film_id):
    kb = types.InlineKeyboardMarkup()

    del_favorite = types.InlineKeyboardButton(text=Smiles.BROKEN_HEART + " Убрать из избранных",
                                              callback_data="del_favorite-" + str(film_id))
    kb.add(del_favorite)

    callback_button_next = types.InlineKeyboardButton(text=Smiles.ARROW_RIGHT, callback_data=Commands.NEXT_PAGE_COMMAND)
    callback_button_back = types.InlineKeyboardButton(text=Smiles.ARROW_LEFT, callback_data=Commands.PREV_PAGE_COMMAND)
    kb.add(callback_button_back, callback_button_next)

    return kb