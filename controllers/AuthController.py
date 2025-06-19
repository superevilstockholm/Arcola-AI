from fastapi.responses import JSONResponse
from aiomysql import Pool
from datetime import datetime, timezone, timedelta

import bcrypt
import secrets
import uuid

from models.AuthModel import LoginModel, RegisterModel

class AuthController:
    @staticmethod
    async def Login(user_data: LoginModel, db_pool: Pool) -> JSONResponse:
        """Login handler"""
        async with db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("""
                        SELECT password, user_type FROM users WHERE username = %s LIMIT 1
                    """, (user_data.username))
                    result = await cur.fetchone()
                    if not result:
                        return JSONResponse(content={"status": False, "message": "Invalid credentials", "detail": {"reason": "User not found"}}, status_code=401)
                    stored_password = result[0]
                    if not bcrypt.checkpw(password=user_data.password.encode("utf-8"), hashed_password=stored_password.encode("utf-8")):
                        return JSONResponse(content={"status": False, "message": "Invalid credentials", "detail": {"reason": "Invalid password"}}, status_code=401)
                    token = secrets.token_hex(16) + datetime.now().strftime("%Y%m%d%H%M%S") + secrets.token_hex(16) + uuid.uuid4().hex
                    expired_at = datetime.now(timezone.utc) + timedelta(days=30)
                    await cur.execute("""
                        DELETE FROM sessions WHERE user_id = (SELECT id FROM users WHERE username = %s LIMIT 1);
                        INSERT INTO sessions (user_id, token, expired_at) VALUES ((SELECT id FROM users WHERE username = %s LIMIT 1), %s, %s);
                    """, (user_data.username, user_data.username, token, expired_at))
                    await conn.commit()
                    user_type = result[1]
                    response = JSONResponse(content={"status": True, "message": "User logged in successfully", "detail": {"username": user_data.username, "role": user_type}}, status_code=200)
                    response.set_cookie(key="session_token", value=token, httponly=True, samesite="Lax", secure=True, max_age=60 * 60 * 24 * 30) # 30 days
                    return response
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error logging in user", "detail": {"reason": str(e)}}, status_code=500)
            
    @staticmethod
    async def Register(userData: RegisterModel, db_pool: Pool) -> JSONResponse:
        async with db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("""
                        SELECT username, email FROM users WHERE username = %s OR email = %s LIMIT 1
                    """, (userData.username, userData.email))
                    result = await cur.fetchone()
                    if result:
                        existing_username, existing_email = result
                        if existing_username == userData.username:
                            return JSONResponse(content={"status": False, "message": "Username already exists", "detail": {"reason": "Username already exists"}}, status_code=409)
                        if existing_email == userData.email:
                            return JSONResponse(content={"status": False, "message": "Email already exists", "detail": {"reason": "Email already exists"}}, status_code=409)
                    encrypted_password = bcrypt.hashpw(userData.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                    await cur.execute("""
                        INSERT INTO users (username, email, password) VALUES (%s, %s, %s)
                    """, (userData.username, userData.email, encrypted_password))
                    await conn.commit()
                    return JSONResponse(content={"status": True, "message": "User registered successfully", "detail": {"username": userData.username, "email": userData.email}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error logging out user", "detail": {"reason": str(e)}}, status_code=500)
            
    @staticmethod
    async def Logout(token: str, db_pool: Pool) -> JSONResponse:
        async with db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("""
                        DELETE FROM sessions WHERE token = %s
                    """, (token,))
                    await conn.commit()
                    return JSONResponse(content={"status": True, "message": "User logged out successfully", "detail": {}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error logging out user", "detail": {"reason": str(e)}}, status_code=500)