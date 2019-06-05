
from core.metric_db_access import MetricDBAccess
from datetime import datetime, timedelta
from flask import request


import time

class MetricDataController:

    DEFAULT_INSTANCE = "DEFAULT_INSTANCE"

    def __init__(self):
        self.initialized = int(round(time.time() * 1000))


    def srv_get_testruns(self):
        ret_value = {'status': 'success', 'testruns': ''}


        lastdays = request.args.get('lastdays')
        startday = request.args.get('startday')
        endday = request.args.get('endday')
        build_number = request.args.get('build_number')
        status = request.args.get('status')
        test_group = request.args.get('test_group')
        scenario = request.args.get('scenario')

        products = request.args.get('prodcuts')
        ## Extract products from the variable == prod1|prod2|prod3|prod4

        rset = MetricDBAccess.execute_query("SELECT * FROM testrun")
        ret_value['testruns'] = rset
        return ret_value


    def srv_get_products(self):
        ret_value = {'status': 'success', 'products': ''}

        name = request.args.get('name')
        version = request.args.get('version')

        rset = MetricDBAccess.execute_query("SELECT * FROM product")
        ret_value['products'] = rset
        return ret_value



    def testdateformat(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")