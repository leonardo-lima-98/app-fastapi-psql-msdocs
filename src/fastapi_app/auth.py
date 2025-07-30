import requests
from datetime import datetime, timedelta
from jose import JWTError, jwt, constants, utils, backends, jwe, jwk, jws
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from settings import settings
from msal import ConfidentialClientApplication

# variaveis de ambiente
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
AUTHORITY = settings.AUTHORITY.replace('TENANT_ID', settings.TENANT_ID)
JWKS_URL = settings.JWKS_URL.replace('TENANT_ID', settings.TENANT_ID)
SCOPE = settings.SCOPE
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET

jwks = requests.get(JWKS_URL).json()["keys"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

msal_app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
)

# Simulação de base de usuários
fake_users_db = {
    "leonardo": {"username": "leonardo", "password": "123456", "role": "admin"},
    "user": {"username": "user", "password": "user123", "role": "viewer"}
}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or user["password"] != password:
        return None
    return user

def decode_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # você pode retornar o usuário aqui também
    except JWTError:
        raise credentials_exception

def get_access_token():
    result = msal_app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Erro ao obter token", result.get("error_description"))

def verify_jwt_token(token: str):
    try:
        unverified_header = jwt.get_unverified_header(token)
        key = next(k for k in jwks if k["kid"] == unverified_header["kid"])
        public_key = jwt.construct_rsa_key(key)
        payload = jwt.decode(token, public_key, algorithms=['RS256'], audience=CLIENT_ID)
        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

def get_current_user(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente")
    token = auth[len("Bearer "):]
    return verify_jwt_token(token)

def get_token():
    result = msal_app.acquire_token_silent(settings.SCOPE, account=None)
    if not result:
        result = msal_app.acquire_token_for_client(scopes=settings.SCOPE)
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Erro ao obter token: {result.get('error_description', 'Desconhecido')}")