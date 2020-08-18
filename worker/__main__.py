import os
from uuid import uuid4
from rq import Connection, Worker
from rq.job import Job

from settings.wiring import Wiring


env = os.environ.get("APP_ENV", "dev")
wiring = Wiring(env)


class JobWithWiring(Job):

    @property
    def kwargs(self):
        result = dict(super().kwargs)
        result["wiring"] = Wiring(env)
        return result

    @kwargs.setter
    def kwargs(self, value):
        super().kwargs = value


with Connection(wiring.redis):
    worker = Worker(
        queues=[
            wiring.settings["TASK_QUEUE_NAME"],
        ],
        name=uuid4().hex,
        job_class=JobWithWiring,
    )
    worker.work()
