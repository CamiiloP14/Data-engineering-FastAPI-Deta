from fastapi import FastAPI
import pandas as pd



# Creacion de una aplicación FastAPI.

app = FastAPI(title='Consultas sobre películas en las plataformas: Amazon, Disney, Hulu y Netflix')

#definiendo metodos:

@app.get ("/")
async def read_root():
    return {"Hello":
            "World!"}

#Consultas

'''
1. Cantidad de veces que aparece una keyword en el título de
 peliculas/series, por plataforma.
'''
@app.get("/get_word_count")
async def get_word_count(plataforma: str, keyword: str):
    movie_df=pd.read_csv('movies.csv')
    #pasamos las entradas a minúsculas
    plataforma =plataforma.lower()
    keyword=keyword.lower()
    #creamos la columna 'platform' 
    movie_df['platform']=movie_df['id'].str[0]
    #filtramos por plataforma
    platform_df = movie_df[movie_df['platform'] == plataforma[0]]
    #extramos los titulos en dicha plataforma 
    titles = platform_df['title']
    #luego iteramos a través de los títulos de las filas filtradas
    count = 0
    for title in titles:
        count += title.count(keyword)
    return f"La keyword '{keyword}' aparece {count} veces en los títulos de películas y series de la plataforma {plataforma}."


'''
2. Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año.
'''

@app.get("/get_score_count")
async def get_score_count(plataforma: str, Score: int, anio: int):
    movie_df=pd.read_csv('movies.csv')
    #pasamos las entradas a minúsculas
    plataforma =plataforma.lower()
    #creamos la columna 'platform' para poder agrupar más adelante
    movie_df['platform']=movie_df['id'].str[0]
    # Creamos una máscara booleana para filtrar las películas con puntaje mayor a Score
    mask = movie_df['score']>Score
    #Aplicamos la máscara para filtrar las películas con puntaje mayor a XX
    high_rated_movies= movie_df[mask]
    # Creamos una máscara booleana para filtrar las películas lanzadas en el año deseado
    mask_2= high_rated_movies['release_year'] == anio
     # Aplicamos la máscara para filtrar las películas lanzadas en el año deseado
    movies_anio = high_rated_movies[mask_2]
    # Agrupamos las películas por plataforma y contamos el número de películas en cada plataforma
    peliculas_por_plataforma = movies_anio.groupby('platform').size().reset_index(name='count')
    # Devolvemos el DataFrame con el resultado
    peliculas_por_plataforma['platform'] == plataforma[0]
    resul=peliculas_por_plataforma[peliculas_por_plataforma['platform'] == plataforma[0]]
    resul= resul['count']
    return f"Para el año {anio} la Cantidad de películas por la plataforma {plataforma}, con un puntaje mayor a {Score} es de {int(resul)}."
  

'''
3. La segunda película con mayor score para una plataforma determinada, 
según el orden alfabético de los títulos.
'''

@app.get("/get_second_score")
async def get_second_score(plataforma: str):
    movie_df=pd.read_csv('movies.csv')
    #pasamos las entradas a minúsculas
    plataforma =plataforma.lower()
    # creamos la columna 'platform' para agrupar
    movie_df['platform']=movie_df['id'].str[0]
    platform_df = movie_df[movie_df['platform'] == plataforma[0]]
    #ordenamos la  columna 'title'
    platform_df = platform_df.sort_values(by=['title', 'score'], ascending=[True, False])
    # Filtramos los títulos que comienzan con #,
    # un número, una comilla doble, una comilla simple, un paréntesis o un guión bajo
    platform_df = platform_df[~platform_df['title'].str.match('^[#"\'\d\(\_]')]
    second_score = platform_df.drop_duplicates(subset='title', keep='first').iloc[1]['score']
    title_second_score =platform_df.drop_duplicates(subset='title', keep='first').iloc[1]['title']
    return f"La segunda película con mayor score para la plataforma {plataforma} según el orden alfabético de los títulos es: '{title_second_score}' con un score de {second_score}."

'''
4. Película que más duró según año, plataforma y tipo de duración.
'''

@app.get("/get_longest")
async def get_longest(plataforma: str, min_or_season: str, anio: int):
    movie_df=pd.read_csv('movies.csv')
    movie_df['platform']=movie_df['id'].str[0]
    # Filtramos por plataforma
    platform_df = movie_df[movie_df['platform'] == plataforma[0]]
    # Filtramos por año
    platform_df = platform_df[platform_df['release_year'] == anio]
    # Filtramos por tipo de duración
    if min_or_season == "min":
        platform_df = platform_df[platform_df["duration_type"]=="min"]
    elif min_or_season == "season":
        platform_df = platform_df[platform_df["duration_type"]=="season"]
    # Ordenamos por duración en orden descendente
    platform_df = platform_df.sort_values(by=['duration_int'], ascending=False)
    # retornamos la primera película
    return f"la película que más duró en el año {anio}, por la plataforma {plataforma} y por el tipo de duración {min_or_season} es: '{platform_df.iloc[0]['title']}' con una duración de {int(platform_df.iloc[0]['duration_int'])} min."

'''
5. Cantidad de series y películas por rating.
'''

@app.get("/get_rating_count")
async def get_rating_count(rating: str):
  movie_df=pd.read_csv('movies.csv')
  return f"La cantidad de peliculas y series por el rating '{rating}' es: {movie_df.groupby('rating').size().loc[rating]}."

