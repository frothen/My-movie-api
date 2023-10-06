from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import  JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


#los tags nos permite agrupar las rutas de la aplicacion
@movie_router.get("/", tags=['home'])
def message():
    return JSONResponse("<h1>Hello worldddd 546!</h1>")

@movie_router.get("/movies" , tags=['movies'],response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
async def get_movies():
    db =Session()
    #result = db.query(MovieModel).all()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))  # Lo retorna en JSON

@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie,status_code=200)
def get_movie(id : int = Path(ge=1, le=2000)):
    db = Session()
    #result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={'Message' : 'No Encontrado'})
    return JSONResponse(status_code=200,content = jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'],response_model=List[Movie],status_code=200)
def get_movies_by_category(category : str =Query(min_length=5, max_length=15)):
    db =  Session()
    #result = db.query(MovieModel).filter(MovieModel.category == category).all()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(status_code=404,content={'Message' : 'Categoria no Encontrada'})
    return JSONResponse(status_code=200,content = jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict,status_code=201)
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
    '''
    #movies.append(movie.dict())
    new_movie = MovieModel(**movie.dict())
    #Añadir el nuevo registro a la base de datos
    db.add(new_movie)
    #Actualizar y guardar los cambios.
    db.commit()
    '''
    MovieService(db).create_movie(movie)

    return JSONResponse(status_code=201,content={"message" : "Se ha registrado la pelicula"})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict,status_code=200)
def update_movie(id: int, movie: Movie):
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={'Message' : 'ID No Encontrado'})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200,content={"message" : "Se ha modificado la pelicula"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict,status_code=200)
def delete_movie(id:int):
    db = Session()
    result : MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404,content={'Message' : 'ID No Encontrado'})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200,content={"message" : "Se ha eliminado la pelicula"}) 