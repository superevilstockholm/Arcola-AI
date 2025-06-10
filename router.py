from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse, StreamingResponse, FileResponse

from aiomysql import Pool

# Models
from models.AuthModels import RegisterModel, LoginModel

# Controllers
from controllers.AuthController import AuthController

class Router:
    def __init__(self, app: FastAPI, db_pool: Pool):
        self.app = app
        self.db_pool = db_pool
        self.routes()

    def routes(self):
        @self.app.get("/api/ping", response_class=JSONResponse, include_in_schema=True)
        async def ping(request: Request) -> JSONResponse:
            """Pinging the server"""
            return JSONResponse(content={"status": True, "message": "pong"}, status_code=200)
        
        @self.app.get("/api/isLoggedIn", response_class=JSONResponse, include_in_schema=True)
        async def isLoggedIn(request: Request) -> JSONResponse:
            """Checking if the user is logged in"""
            return await AuthController().isLoggedIn(request.cookies.get("session_token"), self.db_pool)
        
        @self.app.post("/api/register", response_class=JSONResponse, include_in_schema=True)
        async def register(request: Request, userData: RegisterModel) -> JSONResponse:
            """Registering a new user"""
            return await AuthController().Register(userData.model_dump(), self.db_pool)
        
        @self.app.post("/api/login", response_class=JSONResponse, include_in_schema=True)
        async def login(request: Request, userData: LoginModel) -> JSONResponse:
            """Logging in a user"""
            return await AuthController().Login(userData.model_dump(), self.db_pool)
        
        @self.app.delete("/api/logout", response_class=JSONResponse, include_in_schema=True)
        async def logout(request: Request) -> JSONResponse:
            """Logging out a user"""
            return await AuthController().Logout(token=request.cookies.get("session_token"), db_pool=self.db_pool)
        
        @self.app.post("/api/generate/chat", response_class=StreamingResponse, include_in_schema=True)
        async def chat(request: Request, message: any) -> StreamingResponse:
            pass

        @self.app.post("/api/generate/image", response_class=FileResponse, include_in_schema=True)
        async def image(request: Request, model: any) -> FileResponse:
            pass