



class Product:
    def __init__(self, name, version, description = ""):
        if name is None: raise Exception("Cannot create a product without a name")
        if version is None: raise Exception("Cannot create a product without a name")
        self.name = name
        self.version = version
        self.description = description
        self.__internal_id = -1


    """ Test for the demo of tomorrow """
    def commit(self, cursor):
        scProd = f"SELECT id_product FROM product p WHERE p.name='{str(self.name)}' AND p.version='{str(self.version)}';"
        cursor.execute(scProd)
        recordId = cursor.fetchone()
        if recordId is not None:
            self.__internal_id = recordId[0]
        else:
            scProd = f"INSERT INTO product (name, version, description) VALUES('{str(self.name)}', '{str(self.version)}', " \
                f"'{str(self.description)}') RETURNING id_product;"

            cursor.execute(scProd)
            # Since the query ends with Return id the resultset expected in one row and one cell being the id
            recordId = cursor.fetchone()
            # if we did not receive any return the insert failed, should have normaly raised an exception
            if recordId is None: raise Exception("RQTA_DB: Unable to create the test entity in the schema")
            self.__internal_id = recordId[0]
        return self.__internal_id