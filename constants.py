import os

# Константы - пороли
class ConstantsToken:
    T_BOT_API_TOKEN = ""
    TMBD_API_TOKEN = str(os.environ.get("TMDB_TOKEN"))
    TEST_API_TOKEN = str(os.environ.get('ACCSESS_TOKEN'))


class Smiles:
    HEART = '❤'
    THINKING = '🤔'
    HAPPY = '☺'
    VERY_HAPPY = '😄'
    LIKE = '👍'
    ARROW_LEFT = '⬅'
    ARROW_RIGHT = "➡"
    LUPA = '🔎'
    KINO = '📽️'
    LAMP = '💡'
    LETTER = '📰'
    FIRE='🔥'
    GAME = '🎮'
    TOP = '🎬'
    MAP = '🗺️'
    YEAR = '📅'
    SETTINGS = '🛠'
    WAR = '🔫'
    WEST = '🌵'
    DETECTIVE = '🕵️'
    DRAMA = '🎭'
    HISTORY = '📜'
    COMEDY = '🤡'
    TRILLER = '🧟'
    FANTASTIC = '🔮'
    ACTOR = '🤓'
    DESCRIPTION = '🎞️'
    NOONE_UNDER_EIGHTEEN = "🔞"
    STAR = "🌟"
    THUMBS_UP = "👍"
    THUMBS_DOWN = "👎"
    SOON = "🔜"
    BROKEN_HEART = "💔"


class Commands:
    COMPLITE_SEARCH = Smiles.LUPA + " Выполнить поиск"
    SETTING_COMMAND = Smiles.SETTINGS + " Настройки"
    GET_BACK_COMMAND = Smiles.ARROW_LEFT + " Назад"
    USER_FAVORITE_COMMAND = Smiles.HEART + " Мои избранные"
    UPCOMING_FILMS_COMMAND = Smiles.YEAR + " Сейчас идут"

    COUNTRIES_COMMAND = Smiles.MAP + " Страны"

    SEARCH_FILM_COMMAND = Smiles.LUPA + " Найти фильм"
    SEARCH_FILM_BY_ACTOR = Smiles.ACTOR + 'Найди фильм по актеру'

    NEWS_COMMAND = Smiles.LETTER + " Новости кино"
    GAME_COMMAND = Smiles.GAME + " Игры"
    TOP_FILMS_COMMAND = Smiles.TOP + ' Топ 10'

    YEAR_COMMAND = Smiles.YEAR + " Год"

    GENRE_COMMAND = "Жанр"
    GENRE_HISTORY_COMMAND = Smiles.HISTORY + ' История'
    GENRE_BLOCKBASTER_COMMAND = Smiles.WAR + " Боевик"
    GENRE_FANTASTIC_COMMAND = Smiles.FANTASTIC + ' Фантастика'
    GENRE_DRAMA_COMMAND = Smiles.DRAMA + " Драма"
    GENRE_DETECTIVE_COMMAND = Smiles.DETECTIVE + " Детектив"
    GENRE_MELODRAMA_COMMAND = Smiles.HEART + " Мелодрама"
    GENRE_COMEDY_COMMAND = Smiles.COMEDY + " Комедия"
    GENRE_TRILLER_COMMAND = Smiles.TRILLER + " Триллер"
    GENRE_WEST_COMMAND = Smiles.WEST + " Вестрен"

    GAME_TRUE_OR_FALSE_COMMAND = Smiles.DRAMA + " Правда или ложь"
    GAME_GUESS_FILM = Smiles.DESCRIPTION + " Угадай фильм"

    CLEAR_SETTINGS_COMMAND = Smiles.SETTINGS + ' Убрать настройки'

    POPULAR_FILMS_COMMAND = Smiles.FIRE + " Популярные"

    # CallbackQuery
    NEXT_PAGE_COMMAND = "next_page"
    PREV_PAGE_COMMAND = "prev_page"

    NEW_LIKE_COMMAND = "new_like"
    NEW_DISLIKE_COMMAND = "new_dislike"

    OPEN_GENRES_COMMAND = "open_genres"
    OPEN_YEARS_COMMAND = "open_years"
    OPEN_COUNTRIES_COMMAND = "open_countries"
    COMPLITE_SEARCH_COOMMAND_INLINE = "do_search"


    ADD_FAVORITE_COMMAND = r"add_favorite-(?P<film_id>[0-9]*)"
    ID_FILM_RE = r'/f(?P<film_id>[0-9]*)'
    ID_GENRE_RE = r'add_genre-(?P<genre_id>[0-9]*)'
    DEL_FAVORITE_COMMAND = r"del_favorite-(?P<film_id>[0-9]*)"


class ConstantsAnswers:
    GREETING_MSG = "✌  Привет!\n🎥  Чтобы найти фильм, просто введи его название.\n"
    GREETING_MSG += "👥  Для того, чтобы использовать меня в группе, воспользуйся: @SearchMovieBot /название Фильма/"

    FILM_NOT_FOUNDED_EDITABLE =  Smiles.THINKING + ' По запросу _"{0}"_ ничего не найдено. '
    NO_FAVORITE_FILMS = Smiles.THINKING + " * Вы не добавили избранных фильмов *"

    SEARCH_MSG = " Поиск по заданным параментрам: "
    def format_film_text(self, **text_params):
        # Форматирует текст по фильму в стандартный вид
        pass


class Genres:
    dict_of_genres = {'Детектив': 9648, 'История': 36,
                      'Триллер': 53, 'Вестерн': 37,
                      'Приключения': 12, 'Документальный': 99,
                      'Мультфильм': 16, 'Боевик': 28,
                      'Семейный': 10751, 'Драма': 18,
                      'Военный': 10752, 'Комедия': 35,
                      'Мелодрама': 10749,
                      'Музыка': 10402, 'Криминал': 80, 'Ужасы': 27, 'Фэнтези': 14, 'Фантастика': 878}

    num_dict_of_genres = {
        10752: 'Военный', 9648: 'Детектив', 10402: 'Музыка', 35: 'Комедия', 36: 'История', 878: 'Фантастика',
         80: 'Криминал', 12: 'Приключения', 10770: 'Телевизионный фильм', 14: 'Фэнтези', 16: 'Мультфильм', 18: 'Драма',
         99: 'Документальный', 53: 'Триллер', 10751: 'Семейный', 27: 'Ужасы', 28: 'Боевик', 10749: 'Мелодрама',
         37: 'Вестерн'
    }


class LoggerConfig:
    dictLogConfig = {
        "version": 1,
        "handlers": {
            "fileHandler": {
                "class": "logging.FileHandler",
                "formatter": "myFormatter",
                "filename": "db.log"
            },
            "consoleHandler": {
                "class": "logging.StreamHandler",
                "formatter": "consoleFormatter"
            },
            "fileHandlerOther":{
                "class": "logging.FileHandler",
                "formatter": "myFormatter",
                "filename": "chat_logs.log"
            }
        },
        "loggers": {
            "file_logger": {
                "handlers": ["fileHandler", "consoleHandler"],
                "level": "INFO",
            },

            "console_logger": {
                "handlers": ["consoleHandler", "fileHandler"],
                "level": "DEBUG"
            },
            
            "db_logger": {
                "handlers": ["fileHandler", "consoleHandler"],
                "level": "DEBUG"
            }
        },
        "formatters": {
            "myFormatter": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "consoleFormatter":{
                "format": "%(lineno)d | %(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    }


