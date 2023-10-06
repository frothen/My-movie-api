from fastapi import FastAPI
from config.database import engine,Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
#Para cambiar el nombre de la aplicacion
app.title = "Mi aplicacion con FASTAPI"

#Para cambiar la version de la aplicacion
app.version = "0.0.1"
app.add_middleware(ErrorHandler)

app.include_router(movie_router)
app.include_router(user_router)

#En main.py añadimos las configuraciones para que se cree la base de datos.
Base.metadata.create_all(bind=engine)

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

