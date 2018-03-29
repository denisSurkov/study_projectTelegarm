from constants import Smiles, Genres
import api_connection

def format_text(text_obj):
    # print(text_obj)
    text_to_return = Smiles.TOP + " *" + text_obj["title"] + "* _(" + text_obj["original_title"] + ")_   \n"
    text_to_return += Smiles.YEAR + " " + text_obj["release_date"]

    # Разбор случая, если есть предупереждение о возрастном цензе фильма.
    if text_obj["adult"]:
        text_to_return += " " + Smiles.NOONE_UNDER_EIGHTEEN + "\n"
    else:
        text_to_return += "\n"

    # Вывод средней оценки.
    text_to_return += Smiles.STAR + " " + str(text_obj["vote_average"]) + "\n"

    # Вывод всех жанров фильма
    genres = text_obj["genre_ids"]
    text_to_return += Smiles.HISTORY + " "
    for genre in genres:
        text_to_return += Genres.num_dict_of_genres[genre] + " / "

    text_to_return += "\n\n"

    # Описание фильма
    text_to_return += text_obj["overview"]
    url_path = api_connection.APIMethods().get_image_url(text_obj["poster_path"])

    text_to_return += "[.](" + url_path + ")"

    # Необходимо заменять символ, т.к при его отправке возникает ошибка.
    # Поэтому заменяем на '
    return text_to_return.replace("`", "'")


def format_text_one(text):
    text_to_return = Smiles.TOP + " *" + text["title"] + "* _(" + text["original_title"] + ")_   \n"
    text_to_return += Smiles.YEAR + " " + text["release_date"]

    # Разбор случая, если есть предупереждение о возрастном цензе фильма.
    if text["adult"]:
        text_to_return += " " + Smiles.NOONE_UNDER_EIGHTEEN + "\n"
    else:
        text_to_return += "\n"

    # Вывод средней оценки.
    text_to_return += Smiles.STAR + " " + str(text["vote_average"]) + "\n"

    # Вывод всех жанров фильма
    genres = text["genres"]
    text_to_return += Smiles.HISTORY + " "
    for genre in genres:
        text_to_return += genre["name"].title() + " / "


    url_path = api_connection.APIMethods().get_image_url(text["poster_path"])

    text_to_return += "\n\n"

    # Описание фильма
    text_to_return += text["overview"]

    # Необходимо заменять символ, т.к при его отправке возникает ошибка.
    # Поэтому заменяем на '
    return text_to_return.replace("`", "'")


def complite_results(results):
    text_to_return = "_Результаты поиска:_ \n\n"
    res = results["results"]

    for film in res:
        text_to_return += "*->* *" + film["title"] + "* _(" + film["original_title"] + ")_ /f" + str(film["id"]) + "\n\n"

    text_to_return += "\n"
    return text_to_return


def format_favorite_films(favorite_films):
    return "0"
    # # TODO: Переписать метод. Чтоб не обращался к api_connection
    # text_to_return = Smiles.STAR + " _Ваши избранные фильмы_: \n\n"
    #
    # for film in favorite_films:
    #     text_to_return += "*->* *"+ film[0] + "* /f" + str(film[1]) + "\n\n"
    #
    # return text_to_return


def format_genres(genres):
    text_to_return = " _Поиск по заданным параметрам_: \n\n"
    text_to_return += " *Жанры:* "

    for genre in genres:
        text_to_return += " *" + Genres.num_dict_of_genres[genre] + "* / "

    text_to_return += "\n\n _Для того чтобы добавить новые жанры в поиск, нажмите на одну из кнопок "
    text_to_return += 'на клавиатуре ниже. Чтобы выполнить поиск, нажмите на "Выполнить поиск" \n'
    text_to_return += "Параметры будут дополняться._"
    return text_to_return