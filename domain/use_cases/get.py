from ..entity.file import File
from ..repository.file import FileRepository, FileNotFound


def get(key: str, cache_repository: FileRepository, main_repository: FileRepository, expire: int = None) -> File:
    try:
        return cache_repository.get(key)
    except FileNotFound:
        file = main_repository.get(key)
        cache_repository.set(file, expire=expire)
        return file
