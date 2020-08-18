import boto3, os
from redis import Redis
from rq import Queue

from .dev_settings import settings

from domain.repository.file import FileRepository, RedisFileRepository, S3FileRepository


class Wiring:

    def __init__(self, env=None):
        if env is None:
            env = os.environ.get("APP_ENV", "dev")

        self.env = env
        self.settings = {
            "dev": settings,
        }[env]

        self.cache_expire_time = self.settings["CACHE_EXPIRE_TIME"]

        self.redis: Redis = Redis(
            host=self.settings["REDIS_HOST"],
            port=self.settings["REDIS_PORT"],
            db=self.settings["REDIS_DB"],
        )

        self.s3_session = boto3.Session(
            aws_access_key_id=self.settings["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=self.settings["AWS_SECRET_ACCESS_KEY"],
        )

        self.s3_resource = self.s3_session.resource('s3')

        self.main_repository: FileRepository = S3FileRepository(self.settings["AWS_BUCKET_NAME"], self.s3_resource)
        self.cache_repository: FileRepository = RedisFileRepository(self.redis)

        self.task_queue: Queue = Queue(
            name=self.settings["TASK_QUEUE_NAME"],
            connection=self.redis,
        )
