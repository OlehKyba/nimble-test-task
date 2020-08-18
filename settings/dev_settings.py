import os

settings = {
    "REDIS_HOST": os.environ.get("REDIS_HOST"),
    "REDIS_PORT": os.environ.get("REDIS_PORT"),
    "REDIS_DB": os.environ.get("REDIS_DB"),
    "TASK_QUEUE_NAME": os.environ.get("TASK_QUEUE_NAME"),
    "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY"),
    "AWS_BUCKET_NAME": os.environ.get("AWS_BUCKET_NAME"),
    "CACHE_EXPIRE_TIME": os.environ.get("CACHE_EXPIRE_TIME")
}

