from fastapi import FastAPI, Path, Query
from models import Movie
from data import movies
from config import create_configuration_fastapi
# Permite retornar HTML
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
# Genera una instancia de FastAPI
app = FastAPI()
create_configuration_fastapi(app)


# Lo primero es un decorador
# tags agrupa las rutas


def search_a_movie(id):
    return list(filter(lambda movie: movie["id"] == id, movies))


def delete_a_movie_1(index):
    movies.pop(index)


def get_index(movie):
    return movies.index(movie[0])


@app.get('/', tags=["home"])
def hello_world():
    # Permite retornar cualquier cosa
    # return "Hello world"
    # return {"Hello": "World"}
    return HTMLResponse("<h2>Hello World!</h2>")


@app.get("/movies", tags=["Movies"], response_model=List[Movie])
async def get_movies():
    print([type(element) for element in movies])
    # return movies # Lo retorna sin formato prácticamente
    return JSONResponse(content=movies)  # Lo retorna en JSON


@app.get("/movies/{id}", tags=["Movies"], response_model=Movie)
async def get_movie(id: int = Path(ge=1, le=2000)):
    # for movie in movies:
    #     if movie["id"] == id:
    #         return movie
    movie = search_a_movie(id)
    if movie:
        return JSONResponse(content=movie[0])
    else:
        return "Sorry, we coudn't find that movie"


@app.get("/movies/", tags=["Movies"], response_model=List[Movie])
# Cuando no se deja un parámetro en la ruta pero si en la función, fastAPI detecta que es por query
async def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    # return [movie for movie in movies if movie["category"] == category and movie["year"] == str(year) and movie["rating"] == rating]
    data = [movie for movie in movies if movie["category"] == category]
    return JSONResponse(content=data)


@app.post("/movies", tags=["Movies"], response_model=dict)
async def create_movie(movie: Movie):
    # async def create_movie(id: int, title: str, overview: str, year: int, rating: float, category: str): # Así lo detectaría como si fueran parámetros
    try:
        # movies.append({
        #     'id': id,
        #     'title': title,
        #     'overview': overview,
        #     'year': year,
        #     'rating': rating,
        #     'category': category
        # })
        movies.append(dict(movie))
        return JSONResponse(content={"message": "Created successfully","details": movies[len(movies)-1]})
    except Exception as err:
        print(f"Unexpected error, details: {err}")


@app.put("/movies/{id}", tags=["Movies"], response_model=dict)
def update_a_movie(id: int, movie: Movie):
    movie_to_change = search_a_movie(int(id))
    if (movie_to_change):
        index = movies.index(movie_to_change[0])
        movies[index] = {
            'id': id,
            'title': movie.title,
            'overview': movie.overview,
            'year': movie.year,
            'rating': movie.rating,
            'category': movie.category
        }
        return JSONResponse(content={
            "message": "Updated successfully",
            "details": movies[index]
        })
    else:
        return "Sorry, we coudn't find that movie"


@app.delete("/movies/{id}", tags=["Movies"])
def delete_a_movie(id: int):
    movie_to_delete = search_a_movie(id)
    if (movie_to_delete):
        index = get_index(movie_to_delete)
        # movies.pop(index)
        delete_a_movie(index)
        return JSONResponse(content={
            "message": "Deleted successfully"
        })
    else:
        return "Sorry, we coudn't find that movie"