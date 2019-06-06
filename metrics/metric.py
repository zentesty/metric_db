



class Metric:
    def __init__(self, name, value, target, qualifier = "", dimensions = {}, description = "", index=0):
        if name is None: raise Exception("Cannot create a Metric without a name")
        if value is None: raise Exception("Cannot create a Metric without a value")

        self.name = name
        self.value = value
        self.target = target
        self.qualifier = qualifier
        self.dimensions = dimensions
        self.description = description
        self.scalar_index = index
        self.__internal_id = -1


    def commit(self, cursor):

        scMetrics = f"INSERT INTO metric (name, description, value, target, qualifier, scalar_index) " \
            f"VALUES('{str(self.name)}', '{str(self.description)}', {self.value}, '{self.target}', " \
            f"'{str(self.qualifier)}', {self.scalar_index}) " \
            f"RETURNING id_metric;"

        cursor.execute(scMetrics)

        # Since the query ends with Return id the resultset expected in one row and one cell being the id
        recordId = cursor.fetchone()
        # if we did not receive any return the insert failed, should have normaly raised an exception
        if recordId is None: raise Exception(f"RQTA_DB: Unable to create the {self.__class__.name} entity in the schema")
        self.__internal_id = recordId[0]


        for dim in self.dimensions:
            scDimensions = f"SELECT id_dimension FROM dimension WHERE name='{str(dim)}' AND value='{str(self.dimensions[dim])}';"
            cursor.execute(scDimensions)
            recordId = cursor.fetchone()
            if recordId is not None:
                dimID = recordId[0]
            else:
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



