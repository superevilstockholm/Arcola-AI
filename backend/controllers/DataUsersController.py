from fastapi import Request
from fastapi.responses import JSONResponse
from aiomysql import Pool

import bcrypt

from models.DataUsersModel import CreateDataUsersModel, EditDataUsersModel

class DataUsersController():
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def Index(self, request: Request) -> JSONResponse:
        async with self.db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT id, username, email, verified_email, DATE_FORMAT(created_at, '%Y-%m-%dT%H:%i:%s') AS created_at FROM users")
                    rows = await cur.fetchall()
                    return JSONResponse(content={"status": True, "message": "Success fetching data users", "detail": {"head": ["id", "username", "email", "verified_email", "created_at"], "body": list(rows)}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error logging out user", "detail": {"reason": str(e)}}, status_code=500)
    
    async def Store(self, request: Request, data: CreateDataUsersModel) -> JSONResponse:
        async with self.db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("""
                        SELECT username, email FROM users WHERE username = %s OR email = %s LIMIT 1
                    """, (data.username, data.email))
                    result = await cur.fetchone()
                    if result:
                        existing_username, existing_email = result
                        if existing_username == data.username:
                            return JSONResponse(content={"status": False, "message": "Username already exists", "detail": {"reason": "Username already exists"}}, status_code=409)
                        if existing_email == data.email:
                            return JSONResponse(content={"status": False, "message": "Email already exists", "detail": {"reason": "Email already exists"}}, status_code=409)
                    await cur.execute("INSERT INTO users (username, email, password, user_type) VALUES (%s, %s, %s, %s)", (data.username, data.email, bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"), "user"))
                    await conn.commit()
                    return JSONResponse(content={"status": True, "message": "Success storing data users", "detail": {"test": "Berhasil"}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error logging out user", "detail": {"reason": str(e)}}, status_code=500)
    
    async def Show(self, request: Request, item: str) -> JSONResponse:
        return JSONResponse(content={"status": True, "message": "pong", "detail": {"test": "Berhasil"}}, status_code=200)

    async def Update(self, request: Request, item: str, data: EditDataUsersModel) -> JSONResponse:
        return JSONResponse(content={"status": True, "message": "pong", "detail": {"test": "Berhasil"}}, status_code=200)
    
    async def Delete(self, request: Request, item: str) -> JSONResponse:
        return JSONResponse(content={"status": True, "message": "pong", "detail": {"test": "Berhasil"}}, status_code=200)