import os
from dotenv import load_dotenv

import asyncio
from aiomysql import connect

async def create_table_users(conn):
    async with conn.cursor() as cur:
        await cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            verified_email BOOLEAN DEFAULT FALSE,
            user_type ENUM('user', 'admin') DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

async def create_table_sessions(conn):
    async with conn.cursor() as cur:
        await cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expired_at TIMESTAMP NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

async def migrations(conn):
    await create_table_users(conn)
    await create_table_sessions(conn)

async def main():
    load_dotenv()
    async with connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        charset="utf8",
        autocommit=True
    ) as conn:
        await migrations(conn)

if __name__ == "__main__":
    asyncio.run(main())
    print("Migrations completed")