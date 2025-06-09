from fastapi.responses import JSONResponse
from aiomysql import Pool
from datetime import datetime, timezone, timedelta

import bcrypt
import secrets
import uuid

class AuthController:
    @staticmethod
    async def encryptPassword(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    async def isLoggedIn(token: str, db_pool: Pool) -> JSONResponse:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT user_id, expired_at FROM sessions WHERE token = %s LIMIT 1
                """, (token,))
                result = await cur.fetchone()
                if result:
                    user_id, expired_at = result
                    now_utc = datetime.now(timezone.utc)
                    if expired_at is not None and now_utc > expired_at:
                        return JSONResponse(content={"status": False, "message": "Session expired"}, status_code=401)
                    return JSONResponse(content={"status": True, "user_id": user_id}, status_code=200)
                return JSONResponse(content={"status": False, "message": "Session not found"}, status_code=401)

    @staticmethod
    async def Register(userData: dict, db_pool: Pool) -> JSONResponse:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT username, email FROM users WHERE username = %s OR email = %s LIMIT 1
                """, (userData["username"], userData["email"]))
                result = await cur.fetchone()
                if result:
                    username, email = result
                    if username == userData["username"]:
                        return JSONResponse(content={"status": False, "message": "Username already exists"}, status_code=409)
                    if email == userData["email"]:
                        return JSONResponse(content={"status": False, "message": "Email already exists"}, status_code=409)
                encrypted_password = await AuthController.encryptPassword(userData["password"])
                await cur.execute("""
                    INSERT INTO users (username, email, password) VALUES (%s, %s, %s)
                """, (userData["username"], userData["email"], encrypted_password))
                await conn.commit()
                return JSONResponse(content={"status": True, "message": "User registered successfully"}, status_code=200)
            
    @staticmethod
    async def Login(userData: dict, db_pool: Pool) -> JSONResponse:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT id, password FROM users WHERE username = %s LIMIT 1
                """, (userData["username"],))
                result = await cur.fetchone()

                if result:
                    user_id, hashed_password = result
                    if bcrypt.checkpw(password=userData["password"].encode("utf-8"), hashed_password=hashed_password.encode("utf-8")):
                        token = secrets.token_hex(16) + datetime.now().strftime("%Y%m%d%H%M%S") + secrets.token_hex(16) + uuid.uuid4().hex
                        expired_at = datetime.now(timezone.utc) + timedelta(days=30)
                        await cur.execute("""
                            DELETE FROM sessions WHERE user_id = %s;
                            INSERT INTO sessions (user_id, token, expired_at) VALUES (%s, %s, %s);
                        """, (user_id, user_id, token, expired_at))
                        response = JSONResponse(content={"status": True, "message": "User login successfully"}, status_code=200)
                        response.set_cookie(key="session_token", value=token, httponly=True, samesite="Lax", secure=True, max_age=60 * 60 * 24 * 30) # 30 days
                        return response

        response = JSONResponse(content={"status": False, "message": "Invalid credentials"}, status_code=401)
        response.set_cookie(key="session_token", value="", httponly=True, samesite="Lax", secure=True, max_age=0)
        return response
