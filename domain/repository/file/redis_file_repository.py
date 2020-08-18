from redis import Redis

from .file_repository import FileRepository, FileNotFound
from ...entity.file import File


class RedisFileRepository(FileRepository):

    def __init__(self, redis_db: Redis):
        self.redis_db = redis_db

    def set(self, file: File, key: str = None, expire: int = None) -> File:
        file_dict = file.to_dict()
        key = file_dict.pop('key')
        self.redis_db.hmset(key, file_dict)
        if expire:
            self.redis_db.expire(key, expire)
        else:
            self.redis_db.persist(key)
        return file

    def get(self, key: str) -> File:
        file_bytes_dict: dict = self.redis_db.hgetall(key)

        if not file_bytes_dict:
            raise FileNotFound

        file_dict = {}
        for k, v in file_bytes_dict.items():
            k = k.decode()
            file_dict[k] = v.decode() if k != 'data' else v

        file_dict['key'] = key
        return File(**file_dict)
