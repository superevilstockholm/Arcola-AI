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
                    await cur.execute("SELECT id, username, email, verified_email, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at FROM users")
                    rows = await cur.fetchall()
                    return JSONResponse(content={"status": True, "message": "Success fetching data users", "detail": {"head": ["id", "username", "email", "verified_email", "created_at"], "body": list(rows)}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error", "detail": {"reason": str(e)}}, status_code=500)
    
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
                return JSONResponse(content={"status": False, "message": "Error", "detail": {"reason": str(e)}}, status_code=500)
    
    async def Show(self, request: Request, item: str) -> JSONResponse:
        async with self.db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT id, username, email, password, user_type, verified_email, DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i:%%s') AS created_at FROM users WHERE id = %s", (item,))
                    row = await cur.fetchone()
                    if not row:
                        return JSONResponse(content={"status": False, "message": "Data users not found", "detail": {"reason": "Data users not found"}}, status_code=404)
                    return JSONResponse(content={"status": True, "message": "Success fetching data users", "detail": {"head": ["id", "username", "email", "password", "user_type", "verified_email", "created_at"], "body": list(row)}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error", "detail": {"reason": str(e)}}, status_code=500)

    async def Update(self, request: Request, item: str, data: EditDataUsersModel) -> JSONResponse:
        async with self.db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("""
                        SELECT username, email FROM users WHERE (username = %s OR email = %s) AND id != %s LIMIT 1
                    """, (data.username, data.email, item))
                    result = await cur.fetchone()
                    if result:
                        existing_username, existing_email = result
                        if existing_username == data.username:
                            return JSONResponse(content={"status": False, "message": "Username already exists", "detail": {"reason": "Username already exists"}}, status_code=409)
                        if existing_email == data.email:
                            return JSONResponse(content={"status": False, "message": "Email already exists", "detail": {"reason": "Email already exists"}}, status_code=409)
                    if data.password:
                        new_password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                        await cur.execute("""
                            UPDATE users SET username = %s, email = %s, password = %s, user_type = %s, verified_email = %s WHERE id = %s
                        """, (data.username, data.email, new_password, data.user_type, data.verified_email, item))
                    else:
                        await cur.execute("""
                            UPDATE users SET username = %s, email = %s, user_type = %s, verified_email = %s WHERE id = %s
                        """, (data.username, data.email, data.user_type, data.verified_email, item))
                    await conn.commit()
                    return JSONResponse(content={"status": True, "message": "Success updating data users", "detail": {"test": "Berhasil"}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error", "detail": {"reason": str(e)}}, status_code=500)
    
    async def Delete(self, request: Request, item: str) -> JSONResponse:
        async with self.db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("DELETE FROM users WHERE id = %s", (item,))
                    await conn.commit()
                    if cur.rowcount == 0:
                        return JSONResponse(content={"status": False, "message": "Data users not found", "detail": {"reason": "Data users not found"}}, status_code=404)
                    else:
                        return JSONResponse(content={"status": True, "message": "Success deleting data users", "detail": {"test": "Berhasil"}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error", "detail": {"reason": str(e)}}, status_code=500)