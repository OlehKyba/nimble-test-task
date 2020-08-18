from typing import Callable
from ..entity.file import File
from ..repository.file import FileRepository


def put(file: File,
        repository: FileRepository,
        expire: int = None,
        on_success: Callable = None,
        on_success_args: list = []) -> File:

    file = repository.set(file, expire=expire)
    if on_success:
        on_success(*on_success_args)

    return file
