from fastapi import FastAPI
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

from redis import asyncio as aioredis

from users.router import user_router
from auth.router import auth_router
from relatives.router import relatives_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(relatives_router)

@app.get('/')
def hello():
    return {"Hello": "word"}


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
