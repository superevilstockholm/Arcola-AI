from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

import os
from dotenv import load_dotenv

from aiomysql import create_pool, Pool

from typing import Optional

from utils.logger import log

from router import Router

class ArcolaAI:
    def __init__(self):
        # Initialization
        load_dotenv()
        self.app = FastAPI(
            title="ArcolaAI",
            version="1.0.0"
        )
        self.db_pool: Optional[Pool] = None
        # Mount
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        # Middlewares
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        self.app.add_middleware(GZipMiddleware, minimum_size=500)
        # Events
        self.app.add_event_handler("startup", self.startup_event)
        self.app.add_event_handler("shutdown", self.shutdown_event)
    
    async def startup_event(self):
        if self.db_pool and not self.db_pool.closed:
            self.db_pool.close()
            await self.db_pool.wait_closed()
        self.db_pool = await create_pool(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
            charset="utf8",
            autocommit=True
        )
        await log("Database connected", "info")
        Router(app=self.app, db_pool=self.db_pool)
        await log("Router initialized", "info")

    async def shutdown_event(self):
        if self.db_pool and not self.db_pool.closed:
            self.db_pool.close()
            await self.db_pool.wait_closed()

app = ArcolaAI().app