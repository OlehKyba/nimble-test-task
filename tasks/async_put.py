from domain.entity.file import File
from domain.repository.file import FileRepository
from domain.use_cases import put

from .inject import inject


@inject
def async_put(cache_key: str, expire: int, cache_repository: FileRepository, main_repository: FileRepository):
    file: File = cache_repository.get(cache_key)
    put(file, main_repository)
    put(file, cache_repository, expire=expire)
