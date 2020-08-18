import json
from base64 import b64encode, decodebytes

from ..entity.file import File


class Base64Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return b64encode(o).decode()
        return json.JSONEncoder.default(self, o)


def map_file_to_json(file: File):
    return json.dumps(file.to_dict(), cls=Base64Encoder)


def map_json_to_file(file_dict: dict) -> File:
    string: str = file_dict.get('data')

    if not string:
        raise RequiredFieldMissingError('data')

    if not file_dict.get('key'):
        raise RequiredFieldMissingError('key')

    file_dict['data'] = decodebytes(string.encode())
    return File(**file_dict)


class RequiredFieldMissingError(Exception):

    def __init__(self, field_name):
        super().__init__(f"Required field '{field_name}' is missing!")
