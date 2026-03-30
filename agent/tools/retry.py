import time
from functools import wraps


def with_retry(max_retries: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"⚠️ 第 {attempt + 1} 次失败：{e}")
                    if attempt < max_retries - 1:
                        print(f"🔄 {delay} 秒后重试...")
                        time.sleep(delay)
            print(f"❌ 重试 {max_retries} 次后仍失败")
            raise last_exception

        return wrapper

    return decorator
