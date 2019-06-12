
from core.metric_db_access import MetricDBAccess
from datetime import datetime, timedelta
from flask import request


import time

class MetricsDataController:

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



    ###########################################################################
    ##
    ##      METRICS
    ##
    def srv_get_metrics_by_build_number(self):
        ret_value = {'status': 'success', 'return': ''}

        build_number = request.args.get("build_number")

        if not build_number:
            ret_value['status'] = 'failure'
            return ret_value

        query = """
            SELECT DISTINCT name AS metric_name FROM metric
            JOIN testrun_metric on metric.id_metric = testrun_metric.id_metric
            JOIN testrun t on testrun_metric.id_test = t.id_test
            WHERE t.build_number = '<<BUILD_NUMBER>>';        
        """
        query = query.replace('<<BUILD_NUMBER>>', build_number)

        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value


    ###########################################################################
    ##      Get Metrics By Build Number
    ##      METRICS
    ##
    def srv_get_metrics_by_build_number(self):
        ret_value = {'status': 'success', 'return': ''}

        build_number = request.args.get("build_number")

        if not build_number:
            ret_value['status'] = 'failure'
            return ret_value

        query = """
            SELECT DISTINCT name AS metric_name FROM metric
            JOIN testrun_metric on metric.id_metric = testrun_metric.id_metric
            JOIN testrun t on testrun_metric.id_test = t.id_test
            WHERE t.build_number = '<<BUILD_NUMBER>>';        
        """
        query = query.replace('<<BUILD_NUMBER>>', build_number)

        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value



    ###########################################################################
    ##
    ##      METRICS
    ##
    def srv_get_targets_by_build_number(self):
        ret_value = {'status': 'success', 'return': ''}

        build_number = request.args.get("build_number")

        if not build_number:
            ret_value['status'] = 'failure'
            return ret_value

        query = """
            SELECT DISTINCT target FROM metric
            JOIN testrun_metric on metric.id_metric = testrun_metric.id_metric
            JOIN testrun t on testrun_metric.id_test = t.id_test
            WHERE t.build_number = '<<BUILD_NUMBER>>'        
            ORDER BY target;             
        """
        query = query.replace('<<BUILD_NUMBER>>', build_number)

        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value





    def testdateformat(date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")


    def srv_get_metric_by_Build_number_old(self):

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





    ###########################################################################
    ##
    ##      METRICS
    ##
    def srv_get_graph_data(self):
        ret_value = {'status': 'success', 'return': ''}

        build_number = request.args.get("build_number")
        metric = request.args.get("metric")
        scenario = request.args.get("scenario")

        final_return = {}

        if not build_number:
            ret_value['status'] = 'failure'
            ret_value['return'] = 'Failure: Missing build number'
            print("Build number missing")
            return ret_value

        if not scenario:
            ret_value['status'] = 'failure'
            ret_value['return'] = 'Failure: Missing scenario'
            print("Scenario missing")
            return ret_value

        rset_metrics = self._get_metrics_per_build_number_scenario(build_number, scenario)

        if len(rset_metrics) == 0: return ""

        for metric_entry in rset_metrics:
            query = """
                SELECT m.target, m.scalar_index, m.value FROM metric m
                JOIN testrun_metric tm ON m.id_metric = tm.id_metric
                JOIN testrun t ON tm.id_test = t.id_test
                WHERE t.build_number='<<BUILD_NUMBER>>' and t.scenario='<<SCENARIO>>' and m.name='<<METRIC_NAME>>'
                ORDER BY m.target, m.scalar_index;          
            """
            query = query.replace('<<BUILD_NUMBER>>', build_number)
            query = query.replace('<<SCENARIO>>', scenario)
            query = query.replace('<<METRIC_NAME>>', metric_entry.get('name'))

            rset = MetricDBAccess.execute_query(query)

            if len(rset) == 0: return "";


            # Process all metrics for the combinaison of build_number / scenario
            return_header = ["Index"]
            list_return = []

            temp_list = []
            first_insert = True
            idx = 1

            # Add the header as first
            list_return.append(return_header)
            for result_entry in rset:

                if not result_entry.get('target') == return_header[len(return_header) - 1]:
                    return_header.append(result_entry.get('target'))
                    idx = 1

                if len(return_header) <= 2:
                    list_return.append([])
                    list_return[idx].append(result_entry.get('scalar_index'))

                list_return[idx].append(result_entry.get('value'))
                idx += 1

            final_return.update({metric_entry.get('name'):list_return})

        ret_value['return'] = final_return
        return ret_value









    def _get_metrics_per_build_number_scenario(self, build_number, scenario):
        query = """
            SELECT DISTINCT name FROM metric
            JOIN testrun_metric tm ON metric.id_metric = tm.id_metric
            JOIN testrun t ON tm.id_test = t.id_test
            WHERE t.build_number='<<BUILD_NUMBER>>' and t.scenario='<<SCENARIO>>';
        """

        query = query.replace('<<BUILD_NUMBER>>', build_number)
        query = query.replace('<<SCENARIO>>', scenario)
        rset = MetricDBAccess.execute_query(query)
        return rset





if __name__ == '__main__':
    mc = MetricsDataController()
    rset = mc._get_metrics_per_build_number_scenario('10030', 'gripper')
    print("returned " + str(rset.count()))