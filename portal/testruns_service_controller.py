
from core.metric_db_access import MetricDBAccess
from datetime import datetime, timedelta
from flask import request


import time

class TestRunsDataController:

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


    def validate_date_format(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

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
    ##      TEST_RUNS - GET ALL DATES
    ##
    def srv_get_testruns_all_dates(self):
        ret_value = {'status': 'success', 'return': ''}

        sort_order = " DESC"

        if request.args.get("sort") == "ASC": sort_order == "ASC"



        query = """
            SELECT DISTINCT build_number, to_char(run_time, 'YYYY-MM-DD') AS run_time FROM testrun
            ORDER BY to_char(run_time, 'YYYY-MM-DD')
        """
        query += f" {sort_order};"
        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value







    ###########################################################################
    ##
    ##      TEST_RUNS - SCENARIO by
    ##
    def srv_get_scenario_by_build_number(self):
        ret_value = {'status': 'success', 'return': ''}

        build_number = request.args.get("build_number")

        if not build_number:
            ret_value['status'] = 'failure'
            return ret_value

        query = """
            SELECT DISTINCT scenario FROM testrun
            WHERE build_number='<<BUILD_NUMBER>>';
        """
        query = query.replace('<<BUILD_NUMBER>>', build_number)
        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value





