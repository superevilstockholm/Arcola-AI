from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse

from aiomysql import Pool

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