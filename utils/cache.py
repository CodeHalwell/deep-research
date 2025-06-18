from functools import wraps
import hashlib
import json
import aiofiles
import os

async def cached_async_function(cache_dir: str = "cache"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = hashlib.md5(
                f"{func.__name__}:{json.dumps([args, kwargs], sort_keys=True)}"
                .encode()
            ).hexdigest()
            
            cache_file = os.path.join(cache_dir, f"{cache_key}.json")
            
            # Try to load from cache
            if os.path.exists(cache_file):
                async with aiofiles.open(cache_file, 'r') as f:
                    return json.loads(await f.read())
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            
            os.makedirs(cache_dir, exist_ok=True)
            async with aiofiles.open(cache_file, 'w') as f:
                await f.write(json.dumps(result))
            
            return result
        return wrapper
    return decorator