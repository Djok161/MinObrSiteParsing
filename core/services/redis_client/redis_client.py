import redis

ALL_REDIS = []


def get_redis(db: int) -> redis.Redis:
    r = redis.Redis(host='redis', port=6379,
                    decode_responses=True,
                    db=db)
    ALL_REDIS.append(r)
    return r


async def close_all_redis():
    [r.colse() for r in ALL_REDIS]
    return True
