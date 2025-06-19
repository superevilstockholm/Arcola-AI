from fastapi.responses import JSONResponse
from aiomysql import Pool

from models.ProfileModel import ChangeUsernameModel, ChangeEmailModel

class ProfileController:
    @staticmethod
    async def ChangeUsername(userData: ChangeUsernameModel, token: str, db_pool: Pool):
        async with db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT user_id FROM sessions WHERE token = %s LIMIT 1", (token,))
                    user_row = await cur.fetchone()
                    if not user_row:
                        return JSONResponse(content={"status": False, "message": "Unauthorized", "detail": {"reason": "Invalid session"}}, status_code=401)
                    user_id = user_row[0]
                    await cur.execute("SELECT id FROM users WHERE username = %s AND id != %s", (userData.username, user_id))
                    if await cur.fetchone():
                        return JSONResponse(content={"status": False, "message": "Username already taken", "detail": {"reason": "Duplicate username"}}, status_code=409)
                    await cur.execute("UPDATE users SET username = %s WHERE id = %s", (userData.username, user_id))
                    await conn.commit()
                    return JSONResponse(content={"status": True, "message": "Username changed successfully", "detail": {}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error changing username", "detail": {"reason": str(e)}}, status_code=500)
            
    @staticmethod
    async def ChangeEmail(userData: ChangeEmailModel, token: str, db_pool: Pool):
        async with db_pool.acquire() as conn:
            try:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT user_id FROM sessions WHERE token = %s LIMIT 1", (token,))
                    user_row = await cur.fetchone()
                    if not user_row:
                        return JSONResponse(content={"status": False, "message": "Unauthorized", "detail": {"reason": "Invalid session"}}, status_code=401)
                    user_id = user_row[0]
                    await cur.execute("SELECT id FROM users WHERE email = %s AND id != %s", (userData.email, user_id))
                    if await cur.fetchone():
                        return JSONResponse(content={"status": False, "message": "Email already taken", "detail": {"reason": "Duplicate email"}}, status_code=409)
                    await cur.execute("UPDATE users SET email = %s WHERE id = %s", (userData.email, user_id))
                    await conn.commit()
                    return JSONResponse(content={"status": True, "message": "Email changed successfully", "detail": {}}, status_code=200)
            except Exception as e:
                return JSONResponse(content={"status": False, "message": "Error changing email", "detail": {"reason": str(e)}}, status_code=500)