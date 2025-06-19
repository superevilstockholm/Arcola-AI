from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse

from aiomysql import Pool

from functools import wraps
from typing import Literal

# Models
from models.ResponseModel import BaseResponse
from models.AuthModel import RegisterModel, LoginModel, ResetPasswordByPasswordModel
from models.ProfileModel import ChangeUsernameModel

# Controllers
from controllers.AuthController import AuthController
from controllers.ProfileController import ProfileController

from datetime import datetime

class CustomMiddlewares:
    def auth_middleware(self, role: list[Literal["user", "admin"]] | Literal["user", "admin"] = "user"):
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                token_cookie = request.cookies.get("session_token")
                if not token_cookie:
                    return self._unauthorized("Cookie not found")
                async with self.db_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("SELECT user_id, expired_at FROM sessions WHERE token = %s LIMIT 1", (token_cookie,))
                        session = await cur.fetchone()
                        if not session:
                            return self._unauthorized("Session not found")
                        user_id, expired_at = session
                        if expired_at and datetime.now() > expired_at:
                            await cur.execute("DELETE FROM sessions WHERE token = %s", (token_cookie,))
                            return self._unauthorized("Session expired")
                        await cur.execute("SELECT user_type FROM users WHERE id = %s LIMIT 1", (user_id,))
                        user = await cur.fetchone()
                        if not user:
                            return self._unauthorized("User not found")
                        user_role = user[0]
                        allowed_roles = role if isinstance(role, list) else [role]
                        if user_role not in allowed_roles:
                            return self._forbidden("Forbidden access")
                return await func(request, *args, **kwargs)
            return wrapper
        return decorator
    
    def data_verify_middleware(self, key_data: list[str]):
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                try:
                    json_data = await request.json()
                except Exception:
                    return JSONResponse(content={"status": False, "message": "Invalid JSON body"}, status_code=400)
                if len(key_data) < len(json_data):
                    more_keys: list[str] = [key for key in json_data if key not in key_data]
                    return JSONResponse(
                        content={
                            "status": False,
                            "message": "Too many keys",
                            "detail": f"{', '.join(more_keys)}"
                        },
                        status_code=400
                    )
                return await func(request, *args, **kwargs)
            return wrapper
        return decorator
    
    def _unauthorized(self, reason: str):
        response = JSONResponse(
            content={"status": False, "message": "Unauthorized", "detail": {"reason": reason}},
            status_code=401
        )
        response.delete_cookie(key="session_token")
        return response

    def _forbidden(self, reason: str):
        response = JSONResponse(
            content={"status": False, "message": "Forbidden", "detail": {"reason": reason}},
            status_code=403
        )
        response.delete_cookie(key="session_token")
        return response

class Router(CustomMiddlewares):
    def __init__(self, app: FastAPI, db_pool: Pool):
        super().__init__()
        self.app = app
        self.db_pool = db_pool
        self.routes()

    def routes(self):
        @self.app.route("/api/ping", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"], include_in_schema=False)
        @self.auth_middleware(role=["user", "admin"])
        async def ping(request: Request) -> JSONResponse:
            """Pinging the server"""
            if request.headers.get('content-length') and int(request.headers.get('content-length')) > 100:
                return JSONResponse(content={"status": False, "message": "Payload too large", "detail": {}}, status_code=413)
            try: json_data = await request.json()
            except Exception: json_data = None
            return JSONResponse(content={"status": True, "message": "pong", "detail": { "headers": dict(request.headers), "json_data": json_data, "query": str(request.query_params), "method": request.method}}, status_code=200)
        
        @self.app.post("/api/login", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True)
        @self.data_verify_middleware(["username", "password"])
        async def login(request: Request, userData: LoginModel) -> JSONResponse:
            """Logging in a user"""
            return await AuthController().Login(userData, self.db_pool)
        
        @self.app.post("/api/register", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True)
        @self.data_verify_middleware(["username", "password", "email"])
        async def register(request: Request, userData: RegisterModel) -> JSONResponse:
            """Registering a new user"""
            return await AuthController().Register(userData, self.db_pool)
        
        @self.app.delete("/api/logout", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True)
        @self.auth_middleware(role=["user", "admin"])
        async def logout(request: Request) -> JSONResponse:
            """Logging out a user"""
            return await AuthController().Logout(token=request.cookies.get("session_token"), db_pool=self.db_pool)
        
        @self.app.put("/api/users/change_password", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True)
        @self.auth_middleware(role=["user", "admin"])
        @self.data_verify_middleware(["old_password", "new_password"])
        async def reset_password_using_password(request: Request, userData: ResetPasswordByPasswordModel) -> JSONResponse:
            """Reset password using old password"""
            return await AuthController().ResetPasswordUsingPassword(userData=userData, token=request.cookies.get("session_token"), db_pool=self.db_pool)
        
        @self.app.put("/api/users/change_username", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True)
        @self.auth_middleware(role=["user", "admin"])
        @self.data_verify_middleware(["username"])
        async def change_username(request: Request, userData: ChangeUsernameModel) -> JSONResponse:
            """Change username"""
            return await ProfileController().ChangeUsername(userData=userData, token=request.cookies.get("session_token"), db_pool=self.db_pool)