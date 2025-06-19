from fastapi import Request
from fastapi.responses import JSONResponse
from aiomysql import Pool

class DataAdminController:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def Index(self, request: Request) -> JSONResponse:
        return JSONResponse(content={"status": True, "message": "pong", "detail": {"test": "Berhasil"}}, status_code=200)
    
    async def Store(self, request: Request) -> JSONResponse:
        return JSONResponse(content={"status": True, "message": "pong", "detail": {"test": "Berhasil"}}, status_code=200)
    
    async def Show(self, request: Request, item: str) -> JSONResponse:
        return JSONResponse(content={"status": True, "message": "pong", "detail": {"test": "Berhasil"}}, status_code=200)

    async def Update(self, request: Request, item: str) -> JSONResponse:
        return JSONResponse(content={"status": True, "message": "pong", "detail": {"test": "Berhasil"}}, status_code=200)
    
    async def Delete(self, request: Request, item: str) -> JSONResponse:
        return JSONResponse(content={"status": True, "message": "pong", "detail": {"test": "Berhasil"}}, status_code=200)