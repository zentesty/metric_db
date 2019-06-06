from core.metric_db_access import MetricDBAccess
from metrics.product import Product
from metrics.metric import Metric
from datetime import datetime, timedelta
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


    # TODO: Complete the auto creation
    def createTestRunFromResultSet(resultSet):
        ret_val = []
        if not resultSet: ret_val
        for result in resultSet:
            res = TestRun()




    def __init__(self, build_number, type = TypeEnum.DEV, scenario = None, group='dev', dt_stamp=datetime.now()):
        self.build_number = build_number
        self.scenario = scenario
        self._status = StatusEnum.READY
        self.type = TypeEnum.DEV
        self.test_group = group
        self.metrics = []
        self.products = []
        self.ts_run =  dt_stamp
        self.__internal_id = -1


    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def add_metric(self, name, description, value, qualifier, dimensions, target, index=1):
        newMetric = Metric(name=name, description=description, value=value,
                           qualifier=qualifier, dimensions=dimensions, target=target, index=index)
        self.metrics.append(newMetric)

    def add_product(self, name, version, description = None):
        newProd = Product(name, version, description)
        self.products.append(newProd)




    def commit(self):
        try:
            connection = psycopg2.connect(user=MetricDBAccess.DB_USER,
                                          password=MetricDBAccess.DB_PWD,
                                          host=MetricDBAccess.DB_SERVER,
                                          port=MetricDBAccess.DB_PORT,
                                          database=MetricDBAccess.DB_NAME)

            cursor = connection.cursor()

            scTestRun = f"INSERT INTO testrun (build_number, scenario, status, run_time, run_type) " \
                f"VALUES('{str(self.build_number)}', '{str(self.scenario)}', {self.status.value}," \
                f" '{str(self.ts_run)}','{str(self.test_group)}') RETURNING id_test;"


            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")


            # execute the query
            cursor.execute(scTestRun)

            # Since the query ends with Return id the resultset expected in one row and one cell being the id
            recordId = cursor.fetchone()

            # if we did not receive any return the insert failed, should have normaly raised an exception
            if recordId is None: raise Exception("RQTA_DB: Unable to create the test entity in the schema")

            self.__internal_id = recordId[0]


            # loop on all product to add them to the schema
            for product in self.products:
                prodId = product.commit(cursor)
                # insert in the join table
                scTestProd = f"INSERT INTO testrun_product (id_test, id_product) VALUES({self.__internal_id}, {prodId});"
                cursor.execute(scTestProd)

            for metric in self.metrics:
                metricId = metric.commit(cursor)
                scTestProd = f"INSERT INTO testrun_metric (id_test, id_metric) VALUES({self.__internal_id}, {metricId});"
                cursor.execute(scTestProd)


            # Completed
            # at this time we will commit all the previously created transactions
            # commit the transaction to the DBMS
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")



