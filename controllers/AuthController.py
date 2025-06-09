from fastapi.responses import JSONResponse
from aiomysql import Pool
from datetime import datetime, timezone

class AuthController:
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
                await cur.execute("""
                    INSERT INTO users (username, email, password) VALUES (%s, %s, %s)
                """, (userData["username"], userData["email"], userData["password"]))
                await conn.commit()
                return JSONResponse(content={"status": True, "message": "User registered successfully"}, status_code=200)