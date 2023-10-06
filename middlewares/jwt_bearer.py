from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from utils.jwt_manager import create_token, validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request): #-> Coroutine[Any, Any, HTTPAuthorizationCredentials | None]:
       auth = await super().__call__(request)
       data = validate_token(auth.credentials)# type: ignore
       if data['email'] != "admin@gmail.com":
           raise HTTPException(status_code=403, detail="Credenciales invalidas")