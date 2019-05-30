



class Metric:
    def __init__(self, name, value, qualifier = "", dimensions = {}, description = ""):
        if name is None: raise Exception("Cannot create a Metric without a name")
        if value is None: raise Exception("Cannot create a Metric without a value")

        self.name = name
        self.value = value
        self.qualifier = qualifier
        self.dimensions = dimensions
        self.description = description
        self.__internal_id = -1




    def commit(self, cursor):

        scMetrics = f"INSERT INTO metric (name, description, value, qualifier) " \
            f"VALUES('{str(self.name)}', '{str(self.description)}', {self.value}, '{str(self.qualifier)}') " \
            f"RETURNING id_metric;"

        cursor.execute(scMetrics)

        # Since the query ends with Return id the resultset expected in one row and one cell being the id
        recordId = cursor.fetchone()
        # if we did not receive any return the insert failed, should have normaly raised an exception
        if recordId is None: raise Exception(f"RQTA_DB: Unable to create the {self.__class__.name} entity in the schema")
        self.__internal_id = recordId[0]


        for dim in self.dimensions:
            scDimensions = f"INSERT INTO dimension (name, value) " \
                f"VALUES('{str(dim)}', '{str(self.dimensions[dim])}') RETURNING id_dimension;"
            cursor.execute(scDimensions)
            # Since the query ends with Return id the resultset expected in one row and one cell being the id
            recordId = cursor.fetchone()
            # if we did not receive any return the insert failed, should have normaly raised an exception
            if recordId is None: raise Exception(f"RQTA_DB: Unable to create the Dimension entity in the schema")
            dimID = recordId[0]

            ## Add the entry in the join table
            scTestProd = f"INSERT INTO metric_dimension (id_metric, id_dimension) VALUES({self.__internal_id}, {dimID});"
            cursor.execute(scTestProd)

        return self.__internal_id





if __name__ == '__main__':
        mydict = {'kay1':'val1', 'kay2':'val2', 'kay3':'val3'}
        for entry in mydict:
            moi = mydict[entry]
            print(entry + " ... " + moi)
