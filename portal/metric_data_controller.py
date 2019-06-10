
from core.metric_db_access import MetricDBAccess
from datetime import datetime, timedelta
from flask import request


import time

class MetricDataController:

    DEFAULT_INSTANCE = "DEFAULT_INSTANCE"

    def __init__(self):
        self.initialized = int(round(time.time() * 1000))


    def createWhereClause(self, whereElements):
        bAdded = False
        whereClause = ""
        for element in whereElements:
            val = request.args.get(element[0])
            if val:
                if bAdded == 0: whereClause = " WHERE "
                else: whereClause += " AND "
                bAdded = True
                whereClause += element[1].replace('<<VALUE>>', val)
        return whereClause


    ###########################################################################
    ##
    ##      TEST_RUNS
    ##
    def srv_get_testruns(self):
        ret_value = {'status': 'success', 'return': ''}

        where_elements = [["start_date","run_time >= '<<VALUE>> 00:00:00'"],
                          ["end_date","run_time <= '<<VALUE>> 23:59:59'"],
                          ["build_number","build_number = '<<VALUE>>'"],
                          ["status","status = '<<VALUE>>'"],
                          ["trigger","run_type = '<<VALUE>>'"],
                          ["scenario","scenario <= '<<VALUE>>'"]]

        whereclause = self.createWhereClause(where_elements)

        # replace time based search for the proper column name
        whereclause = whereclause.replace("start_date", "run_time")
        whereclause = whereclause.replace("to_date", "run_time")


        products = request.args.get('prodcuts')
        ## Extract products from the variable == prod1|prod2|prod3|prod4


        query = "SELECT * FROM testrun" + whereclause
        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value

    ###########################################################################
    ##
    ##      PRODUCTS
    ##
    def srv_get_products(self):
        ret_value = {'status': 'success', 'return': ''}


        where_elements = [["name","name = '<<VALUE>>'"],
                          ["version","version = '<<VALUE>>'"]]
        whereclause = self.createWhereClause(where_elements)

        query = "SELECT * FROM product" + whereclause
        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value


    ###########################################################################
    ##
    ##      METRICS
    ##
    def srv_get_metrics(self):
        ret_value = {'status': 'success', 'return': ''}

        where_elements = [["name","name = '<<VALUE>>'"],
                          ["target","target = '<<VALUE>>'"],
                          ["scalar_index","scalar_index = <<VALUE>>"]]
        whereclause = self.createWhereClause(where_elements)


        query = "SELECT * FROM metric" + whereclause
        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value



    def testdateformat(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")


    def srv_get_metric_by_Build_number(self):

        query = """
        SELECT m.id_metric, m.scalar_index, m.name, m.target, m.value, t.run_type from metric m
            Join testrun_metric tm on m.id_metric = tm.id_metric
            Join testrun t on tm.id_test = t.id_test
            WHERE t.build_number='<<BUILD_NUMBER>>' and t.scenario='<<SCENARIO>>'
                  and m.target='<<TARGET>>' and m.name='<<METRIC>>'
            ORDER BY m.scalar_index;
        """
        ret_value = {'status': 'success', 'return': ''}

        target = request.args.get("target")
        build_number = request.args.get("build_number")
        scenario = request.args.get("scenario")
        metric = request.args.get("metric")

        query = query.replace('<<BUILD_NUMBER>>', build_number)
        query = query.replace('<<SCENARIO>>', scenario)
        query = query.replace('<<TARGET>>', target)
        query = query.replace('<<METRIC>>', metric)

        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value


    def srv_get_metric_by_Build_number_graph(self):

        query = """
        SELECT m.id_metric, m.scalar_index, m.name, m.target, m.value, t.run_type from metric m
            Join testrun_metric tm on m.id_metric = tm.id_metric
            Join testrun t on tm.id_test = t.id_test
            WHERE t.build_number='<<BUILD_NUMBER>>' and t.scenario='<<SCENARIO>>'
                  and m.target='<<TARGET>>' and m.name='<<METRIC>>'
            ORDER BY m.scalar_index;
        """
        ret_value = {'status': 'success', 'return': ''}

        target = request.args.get("target")
        build_number = request.args.get("build_number")
        scenario = request.args.get("scenario")
        metric = request.args.get("metric")

        query = query.replace('<<BUILD_NUMBER>>', build_number)
        query = query.replace('<<SCENARIO>>', scenario)
        query = query.replace('<<TARGET>>', target)
        query = query.replace('<<METRIC>>', metric)

        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value




