from botocore.exceptions import ClientError

from .file_repository import FileRepository, FileNotFound
from ...entity.file import File


class S3FileRepository(FileRepository):

    def __init__(self, bucket_name: str, s3_resource):
        self.bucket_name = bucket_name
        self.s3_resource = s3_resource

    def set(self, file: File, key: str = None, expire: int = None) -> File:
        obj = self.s3_resource.Object(self.bucket_name, key or file.key)
        obj.put(Body=file.data, Metadata={'extension': file.extension, 'key': file.key})
        return file

    def get(self, key: str) -> File:
        try:
            obj = self.s3_resource.Object(self.bucket_name, key)
            extension, file_key = obj.metadata['extension'], obj.metadata['key']
            data = obj.get()['Body'].read()
            return File(extension=extension, key=file_key, data=data)
        except self.s3_resource.meta.client.exceptions.NoSuchKey:
            raise FileNotFound
        except ClientError:
            raise FileNotFound
