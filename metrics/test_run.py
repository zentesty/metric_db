
import uuid
from enum import Enum

class TestRun:
    guid =str(uuid.uuid4())

    def __init__(self, build_number, scenario):
        self.scenario = None
        self.build_number = None
        self._status = -1


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value




    class Status(Enum):
        NOTRAN = -1
        FAIL = 0
        ERROR = 1 # was not able to run
        ER = 0
