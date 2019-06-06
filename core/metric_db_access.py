
import psycopg2
import copy


class MetricDBAccess:

    DB_SERVER = "127.0.0.1"
    DB_PORT = 5432
    DB_USER = "robotiq"
    DB_PWD = "qitobor"
    DB_NAME = "rqta_db_01"

    # DB_SERVER = "resultats-autotest.robotiq.rocks"
    # DB_PORT = 5433
    # DB_USER = "robotiq"
    # DB_PWD = "qitobor"
    # DB_NAME = "rqta_db_01"




    def execute_query(query):
        ret_val = []
        try:
            connection = psycopg2.connect(user=MetricDBAccess.DB_USER,
                                          password=MetricDBAccess.DB_PWD,
                                          host=MetricDBAccess.DB_SERVER,
                                          port=MetricDBAccess.DB_PORT,
                                          database=MetricDBAccess.DB_NAME)
            cursor = connection.cursor()


            print(connection.get_dsn_parameters(), "\n")

            # execute the query
            cursor.execute(query)
            retsultSet = cursor.fetchall()

            connection.commit()

            colnames = [desc[0] for desc in cursor.description]



            for resline in retsultSet:
                resObj = {}
                for i in range(len(colnames)):
                    a = {colnames[i]:resline[i]}
                    resObj.update(a)
                ret_val.append(resObj)

            return ret_val

        except (Exception, psycopg2.Error) as error:
            print(f"Error while connecting to PostgreSQL "
                  f"(server{MetricDBAccess.DB_SERVER}:{MetricDBAccess.DB_PORT}, "
                  f"DB={MetricDBAccess.DB_NAME}, USER={MetricDBAccess.DB_USER} ", error)

        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


if __name__ == '__main__':
    rset = MetricDBAccess.execute_query("SELECT * FROM  metric")
    for line in rset:
        print(line)
