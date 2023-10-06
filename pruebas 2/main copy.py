from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Optional, List
from starlette.requests import Request
from utils.jwt_manager import create_token, validate_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config.database import Session,engine,Base
from models.movie import Movie as MovieModel

app = FastAPI()
#Para cambiar el nombre de la aplicacion
app.title = "Mi aplicacion con FASTAPI"

#Para cambiar la version de la aplicacion
app.version = "0.0.1"

#En main.py añadimos las configuraciones para que se cree la base de datos.
Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request): #-> Coroutine[Any, Any, HTTPAuthorizationCredentials | None]:
       auth = await super().__call__(request)
       data = validate_token(auth.credentials)# type: ignore
       if data['email'] != "admin@gmail.com":
           raise HTTPException(status_code=403, detail="Credenciales invalidas")
           

class User(BaseModel):
    email : str
    password : str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5,max_length=15)
    overview: str= Field(min_length=15,max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1,le=10)
    category: str = Field(min_length=5, max_length=15)

    """
    gt: greater than
    ge: greater than or equal
    lt: less than
    le: less than or equal
    """

    class Config:
        json_schema_extra = {
            'example': {
                "id": 1,
                "title": "Mi pelicula",
                "overview": "Descripción de la pelicula",
                "year": 2022,
                "rating": 9.8,
                "category": "Acción"
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 2,
        'title': 'Avatar 2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 3,
        'title': 'En busca de la felicidad',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 9.8,
        'category': 'Drama'
    }
]
#los tags nos permite agrupar las rutas de la aplicacion
@app.get("/", tags=['home'])

def message():
    return HTMLResponse("<h1>Hello worldddd 546!</h1>")
'''
def message():
    return "Hello world !"

def read_root():
    return {"Hello": "World"}
'''
@app.get("/movies" , tags=['movies'],response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
async def get_movies():
    return JSONResponse(status_code=200,content=movies)  # Lo retorna en JSON

@app.post('/login', tags=['auth'])
def login(user: User):
    if (user.email == "admin@gmail.com" and user.password == "123456"):
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content={"message": "Credenciales inválidas, intente de nuevo"})

@app.get('/movies/{id}', tags=['movies'], response_model=Movie,status_code=200)
def get_movie(id : int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            return JSONResponse(status_code=200,content=item)
    return JSONResponse(status_code=404,content=[])

'''
@app.get(
    "/movies/{movie_id}",tags=["Movies"])
def read_movie(movie_id: int):
    try:
        return [ movie for movie in movies if movie['id'] == movie_id][0]
    except IndexError:
        return {"error": "Movie not found"}
'''
@app.get('/movies/', tags=['movies'],response_model=List[Movie],status_code=200)
def get_movies_by_category(category : str =Query(min_length=5, max_length=15)):
    data=[item for item in movies if item['category'] == category] 

    return JSONResponse(status_code=200,content=data)
""" 
@app.post('/movies', tags=['movies'])
def create_movie(
    id: int = Body(),
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()):
movies.append(
        {
            "id": id,
            "title": title,
            "overview":overview,
            "year" :year,
            "rating":rating,
            "category":category
        }
    ) 
    return movies

@app.put('/movies/{id}', tags=['movies'])
def update_movie(
    id: int,
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()):
    for item in movies:
        if item["id"] == id:
            item['title'] = title,
            item['overview'] = overview,
            item['year'] = year,
            item['rating'] = rating,
            item['category'] = category
            return movies
    return []

Encontré esto en la documentación de FastAPI: . Para devolver respuestas HTTP se utiliza HTTPException:

from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"item": items[item_id]}

Al envíar desde la documentación un string diferente a 'foo' arrojará el mensaje de 'detail':

Pero si enviamos 'foo': . Espero te sirva. Puede que exista otro método muchísimo más fácil.
"""
@app.post('/movies', tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie :Movie):
    #Iniciamos una sesión
    db = Session()
    #Añadimos los datos al modelo MovieModel()
    '''
    Podemos hacerlo de dos formas:
    Añadiendo dato por dato:
    new_movie = MovieModel(title=movie.title, overview=movie.overview, ...)

    Descomprimiendo el diccionario de peliculas.
    new_movie = MovieModel(**movie.dict())
    '''
    #movies.append(movie.dict())
    new_movie = MovieModel(**movie.dict())
    #Añadir el nuevo registro a la base de datos
    db.add(new_movie)
    #Actualizar y guardar los cambios.
    db.commit()
    
    return JSONResponse(status_code=201,content={"message" : "Se ha registrado la pelicula"})


@app.put('/movies/{id}', tags=['movies'], response_model=dict,status_code=200)
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200,content={"message" : "Se ha modificado la pelicula"})
    return []

@app.delete('/movies/{id}', tags=['movies'], response_model=dict,status_code=200)
def delete_movie(id:int):
     for item in movies:
        if item["id"] == id:

            movies.remove(item)
            return JSONResponse(status_code=200,content={"message" : "Se ha eliminado la pelicula"}) 