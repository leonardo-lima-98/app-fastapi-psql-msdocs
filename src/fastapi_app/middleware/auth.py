from fastapi import Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


# Token simples para teste - em produção seria gerado dinamicamente
VALID_TOKEN = "meu-token-secreto-123"

# Rotas que não precisam de autenticação
PUBLIC_ROUTES = ["/", "/auth/", "/docs/", "/bingo/", "/restaurant/"]

# === OPÇÃO 1: Middleware personalizado ===
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Permitir acesso irrestrito à documentação ou login (exemplo)

        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        # Captura o token do header Authorization
        token = request.headers.get("Authorization")
        
        if token != f"Bearer {VALID_TOKEN}":
            JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Unauthorized"})
            # login_url = request.url_for("http://localhost:8000/auth")
            return RedirectResponse(url='http://127.0.0.1:8000/auth', status_code=status.HTTP_302_FOUND)

        # Se autorizado, continua o fluxo
        response = await call_next(request)
        return response
    # async def dispatch(self, request: Request, call_next):
    #     # Pula verificação para rotas públicas
    #     if request.url.path in PUBLIC_ROUTES:
    #         response = await call_next(request)
    #         return response
        
    #     # Verifica se existe o header Authorization
    #     auth_header = request.headers.get("Authorization")
        
    #     if not auth_header:
    #         # Para requests de API (Accept: application/json), retorna JSON
    #         accept_header = request.headers.get("Accept", "")
    #         if "application/json" in accept_header:
    #             return JSONResponse(
    #                 status_code=status.HTTP_401_UNAUTHORIZED,
    #                 content={"detail": "Token de acesso obrigatório"}
    #             )
    #         # Para requests de navegador, redireciona para login
    #         login_url = request.url_for("/auth/")
    #         return RedirectResponse(url=login_url, status_code=status.HTTP_302_FOUND)
        
    #     # Verifica formato "Bearer token"
    #     try:
    #         scheme, token = auth_header.split()
    #         if scheme.lower() != "bearer":
    #             raise ValueError
    #     except ValueError:
    #         accept_header = request.headers.get("Accept", "")
    #         if "application/json" in accept_header:
    #             return JSONResponse(
    #                 status_code=status.HTTP_401_UNAUTHORIZED,
    #                 content={"detail": "Formato de token inválido. Use: Bearer <token>"}
    #             )
    #         login_url = request.url_for("/auth/")
    #         return RedirectResponse(url=login_url, status_code=status.HTTP_302_FOUND)
        
    #     # Valida o token
    #     if token != VALID_TOKEN:
    #         accept_header = request.headers.get("Accept", "")
    #         if "application/json" in accept_header:
    #             return JSONResponse(
    #                 status_code=status.HTTP_401_UNAUTHORIZED,
    #                 content={"detail": "Token inválido"}
    #             )
    #         login_url = request.url_for("/auth/")
    #         return RedirectResponse(url=login_url, status_code=status.HTTP_302_FOUND)
        
    #     # Token válido, continua para a rota
    #     response = await call_next(request)
    #     return response