
from core.metric_db_access import MetricDBAccess
from datetime import datetime, timedelta
from flask import request


import time

class ProductsDataController:

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
    ##      PRODUCTS
    ##
    def srv_get_products(self):
        ret_value = {'status': 'success', 'return': ''}


        where_elements = [["name" ,"name = '<<VALUE>>'"],
                          ["version" ,"version = '<<VALUE>>'"]]
        whereclause = self.createWhereClause(where_elements)

        query = "SELECT * FROM product" + whereclause
        rset = MetricDBAccess.execute_query(query)
        ret_value['return'] = rset
        return ret_value
