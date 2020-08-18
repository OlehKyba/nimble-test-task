from typing import Dict
from uuid import uuid4


class File:

    def __init__(self, extension: str, data: bytes, key: str = None):
        self.key: str = key or str(uuid4().hex)
        self.extension: str = extension
        self.data: bytes = data

    def to_dict(self) -> Dict:
        return {'key': self.key, 'extension': self.extension, 'data': self.data}
