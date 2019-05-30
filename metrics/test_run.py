from datetime import datetime
import uuid
import psycopg2
import time

from enum import Enum


class StatusEnum(Enum):
    ERROR = -1 # test was unable to perform assertions due to error in setup
    FAIL  = 0  # test ran but assertion(s) failed
    READY = 1  # test setup to be ran but not started yet

class TypeEnum(Enum):
    DEV         = 1
    DAILY       = 2
    REFERENCE   = 3


class TestRun:
    guid =str(uuid.uuid4())

    def __init__(self, build_number, type = TypeEnum.DEV, scenario = None):
        self.build_number = build_number
        self.scenario = scenario
        self._status = StatusEnum.READY
        self.type = TypeEnum.DEV
        self.metrics = []
        self.products = []

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def add_metric(self, name, description, value, qualifier, dimensions):
        newMetric = self.Metric(name, description, value, qualifier, dimensions)
        self.metrics.append(newMetric)

    def add_product(self, name, version, description = None):
        newProd = self.Product(name, version, description)
        self.metrics.append(newProd)

    def commit(self):
        try:
            connection = psycopg2.connect(user="mpr", password="robotiq",
                                          host="127.0.0.1", port="5432", database="rqta_db")
            cursor = connection.cursor()

            scTestRun = f"INSERT INTO test_run (build_number, scenario, status, ts_run) " \
                f"VALUES('{str(self.build_number)}', '{str(self.scenario)}', {self.status.value}, '{str(datetime.now())}');"

            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")
            # Print PostgreSQL version
            cursor.execute(scTestRun)
            connection.commit()



            # record = cursor.fetchone()
            # print("You are connected to - ", record, "\n")

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")



