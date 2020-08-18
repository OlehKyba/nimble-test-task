import os
from flask import Flask, request

from settings.wiring import Wiring

from domain.entity.file import File
from domain.mappers.file import map_file_to_json, map_json_to_file, RequiredFieldMissingError
from domain.repository.file import FileNotFound
from domain.use_cases import get, put

from tasks.async_put import async_put


class App(Flask):

    def __init__(self, wiring, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print(f"Starting application in {wiring.env} mode")
        self.wiring = wiring

        self.route("/get/<key>")(self.get)
        self.route("/put/", methods=['POST'])(self.put)

    def get(self, key: str):
        try:
            file: File = get(key,
                             self.wiring.cache_repository,
                             self.wiring.main_repository,
                             expire=self.wiring.cache_expire_time)
            return map_file_to_json(file)
        except FileNotFound:
            return {"msg": f"File with key {key} not found!"}, 404

    def put(self):
        try:
            file = map_json_to_file(request.json)
        except RequiredFieldMissingError as error:
            return {"msg": str(error)}, 409
        else:
            put(
                file=file,
                repository=self.wiring.cache_repository,
                on_success=self.wiring.task_queue.enqueue,
                on_success_args=[async_put, file.key, self.wiring.cache_expire_time],
            )
            return {"msg": "OK!"}


env = os.environ.get("APP_ENV", "dev")
wiring = Wiring(env)
app = App(wiring, "app-file-storage-proxy")
