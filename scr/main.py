from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache



from redis import asyncio as aioredis

from users.router import user_router
from auth.router import auth_router
from relatives.router import relatives_router
from pages.router import pages_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(relatives_router)
app.include_router(pages_router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
