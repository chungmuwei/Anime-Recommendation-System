from AnilistPython import Anilist
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
import numpy as np
import csv


def setup():
    genres = ['sports','supernatural','comedy','ecchi','sci-fi','psychological','mahou shoujo','horror',
            'drama','thriller','action','mystery','hentai','music','fantasy','adventure','mecha','slice of life',
            'romance'
    ]

    genres_id = {}
    # Converting genre into binary
    for i in range(0, 19):
        genres_id.update({genres[i]: i})

    genres_list = dict()
    with open("anime-db.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key, value in row.items():
                if value == '':
                    continue
                int_value = int(value)
                if int_value in genres_list:
                    genres_list[int_value].append(key)
                else:
                    genres_list.update({int_value: [key]})

    ultimate_binary_list = []
    anime_id_at = []
    for anime_id, genre_list in genres_list.items():
        binary_list = [0] * 19
        for genre in genre_list:
            binary_list[genres_id[genre]] = 1
        anime_id_at.append(anime_id)
        ultimate_binary_list.append(np.array(binary_list))
    
    return genres_id, anime_id_at, ultimate_binary_list

# ultimate_binary_list
def get_recommendation(user_input: str, genres_id: dict, anime_id_at: list, ultimate_binary_list: list) -> list[str]:
    anilist = Anilist()
    try:
        usr_anime = anilist.get_anime(user_input)["genres"]
    # return an empty list if cannot find usr_anime
    except IndexError:
        return []
    for i in range(len(usr_anime)):
        usr_anime[i] = usr_anime[i].lower()

    usr_list = [0] * 19
    for genre in usr_anime:
        usr_list[genres_id[genre]] = 1

    sim_jaccard = []

    x = np.array(usr_list)
    # x = user or item vector
    # articles = vectors correcponding to every article
    
    for a in ultimate_binary_list:
        sim_jaccard.append(jaccard_score(x,a)) # only if all the vectors have binary values

    result = []
    for i in range(len(sim_jaccard)):
        result.append((sim_jaccard[i], anime_id_at[i]))
    result.sort(reverse=True)


    recommend_list = []

    for i in range(8):
        anime = anilist.get_anime_with_id(result[i][1])
        anime_name = anime["name_english"]
        if (anime_name == None):
            anime_name = anime["name_romaji"]

        recommend_list.append({"name": anime_name, "image": anime['cover_image'], "rating": anime['average_score']})

    return recommend_list

if __name__ == "__main__":
    # setup: run once
    genres_id, anime_id_at, ultimate_binary_list = setup()
    get_recommendation("Naruto", genres_id, anime_id_at, ultimate_binary_list)
    get_recommendation("one piece", genres_id, anime_id_at, ultimate_binary_list)




