from fastapi.responses import JSONResponse

from aiomysql import Pool

class AuthController:
    async def isLoggedIn(token: str, db_pool: Pool) -> JSONResponse:
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                pass