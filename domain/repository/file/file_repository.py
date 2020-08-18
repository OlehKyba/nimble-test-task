import abc

from domain.entity.file import File


class FileRepository(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def set(self, file: File, key: str = None, expire: int = None) -> File:
        pass

    @abc.abstractmethod
    def get(self, key: str) -> File:
        pass


class FileNotFound(Exception):
    pass
