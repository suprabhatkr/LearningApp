import logging
import json
import time
from typing import Any, Optional
import redis.asyncio as aioredis
from app.config import settings

logger = logging.getLogger("Cache")

class LocalMemoryCache:
    """Fallback in-memory cache to use when Redis is offline."""
    def __init__(self):
        self._data = {}
        self._expires = {}
        logger.info("Initializing In-Memory Cache (Redis Offline Fallback)")

    async def get(self, key: str) -> Optional[str]:
        if key in self._expires and self._expires[key] < time.time():
            self.delete(key)
            return None
        return self._data.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        self._data[key] = value
        if ex:
            self._expires[key] = time.time() + ex
        else:
            self._expires.pop(key, None)
        return True

    def delete(self, key: str) -> bool:
        self._data.pop(key, None)
        self._expires.pop(key, None)
        return True

    async def incr(self, key: str) -> int:
        val = await self.get(key)
        try:
            new_val = int(val) + 1 if val else 1
        except ValueError:
            new_val = 1
        await self.set(key, str(new_val))
        return new_val

    async def ping(self) -> bool:
        return True


class CacheManager:
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
        self.local_cache = LocalMemoryCache()
        self.is_redis_active = False

    async def connect(self):
        try:
            self.redis = aioredis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                socket_timeout=1.0  # Fail fast if Redis is not running
            )
            await self.redis.ping()
            self.is_redis_active = True
            logger.info("Connected to Redis successfully.")
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Falling back to in-memory cache.")
            self.redis = None
            self.is_redis_active = False

    async def get(self, key: str) -> Optional[str]:
        if self.is_redis_active and self.redis:
            try:
                return await self.redis.get(key)
            except Exception as e:
                logger.error(f"Redis get error: {e}. Reading from local fallback.")
        return await self.local_cache.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        if self.is_redis_active and self.redis:
            try:
                await self.redis.set(key, value, ex=ex)
                return True
            except Exception as e:
                logger.error(f"Redis set error: {e}. Writing to local fallback.")
        return await self.local_cache.set(key, value, ex)

    async def delete(self, key: str) -> bool:
        if self.is_redis_active and self.redis:
            try:
                await self.redis.delete(key)
                return True
            except Exception as e:
                logger.error(f"Redis delete error: {e}. Deleting from local fallback.")
        return self.local_cache.delete(key)

    async def incr(self, key: str) -> int:
        if self.is_redis_active and self.redis:
            try:
                return await self.redis.incr(key)
            except Exception as e:
                logger.error(f"Redis incr error: {e}. Incrementing in local fallback.")
        return await self.local_cache.incr(key)

    async def check_rate_limit(self, key: str, limit: int, window: int) -> tuple[bool, int, int]:
        """
        Implements a sliding window rate limiter.
        Returns (is_allowed, current_requests, time_remaining).
        Highly educational senior SDE implementation.
        """
        now = time.time()
        if self.is_redis_active and self.redis:
            try:
                # Redis-based Rate Limiter using Transaction & Sorted Set
                # Key maps to a sorted set of timestamps
                clear_before = now - window
                pipeline = self.redis.pipeline()
                pipeline.zremrangebyscore(key, 0, clear_before)
                pipeline.zadd(key, {str(now): now})
                pipeline.zcard(key)
                pipeline.expire(key, window)
                res = await pipeline.execute()
                
                request_count = res[2]
                is_allowed = request_count <= limit
                
                # Approximate time remaining until next token/expiry
                time_remaining = int(window - (now % window))
                return is_allowed, request_count, time_remaining
            except Exception as e:
                logger.error(f"Redis rate limiter error: {e}. Falling back to in-memory rate limiter.")

        # In-memory sliding window rate limiter fallback
        limiter_key = f"rate_limit:{key}"
        data_str = await self.get(limiter_key)
        timestamps = json.loads(data_str) if data_str else []
        
        # Filter timestamps outside window
        timestamps = [t for t in timestamps if t > now - window]
        timestamps.append(now)
        
        request_count = len(timestamps)
        is_allowed = request_count <= limit
        
        await self.set(limiter_key, json.dumps(timestamps), ex=window)
        time_remaining = int(window - (now % window))
        
        return is_allowed, request_count, time_remaining

cache_manager = CacheManager()
