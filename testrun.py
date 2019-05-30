import psycopg2
import sys, os
# import numpy as np
import pandas as pd
# import example_psql as creds
# import pandas.io.sql as psql

## ****** LOAD PSQL DATABASE ***** ##


def load_data(schema, table, conn):

    sql_command = f"SELECT * FROM {str(schema)}.{str(table)}"
    print (sql_command)

    # Load the data
    data = pd.read_sql(sql_command, conn)

    print(data.shape)
    return (data)



# Set up a connection to the postgres server.
if __name__ == '__main__':
    conn_string = "host="+ "127.0.0.1" +" port="+ "5432" +" dbname="+ "postgres" +" user=" + "mpr" \
    +" password="+ "robotiq"
    conn=psycopg2.connect(conn_string)
    print("Connected!")

    # Create a cursor object
    cursor = conn.cursor()
    load_data("rqta_db", "tmp_account", conn)



