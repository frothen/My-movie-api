from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction, RequestResponseEndpoint

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={'error' : str(e)})
        
'''
#Reemplazar 
Response | JSONResponse

#usar
Union[Response, JSONResponse]

#Deben importar 
from typing import Union


    Creen su cuenta en Railway
    Vinculen github
    New Project -> Deploy form github repo
    Colocan el nombre del repositorio
    Una vez les avisa que se hizo el deploy van a Settings
    Generan la URL del dominio

Listo -> Habemus API en línea
'''