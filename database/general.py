"""General functions that all the scripts use to interact with the database"""
import inspect
from datetime import datetime
import MySQLdb
import os


def dump_sql_error(cursor, utc_date, module, function, query, error):
    try:
        table_name = 'err_identity_log'
        to_insert = {
            'utc_dtm': str(utc_date),
            'module': "/".join(str(module).split('/')[-3:]),
            'function': str(function),
            'query': query,
            'error': error
        }

        fields = ', '.join(to_insert.keys())
        values = ', '.join('%(' + k + ")s" for k in to_insert.keys())
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, fields, values)
        cursor.execute(sql, to_insert)
        return 'Error dumped'
    except MySQLdb.Error as e:
        return 'Cannot store error dump. Reason: %s' % e


def execute(cursor, query):
    """Executes and sql statement and hide MySQLdb.Error exceptions."""
    # execute and sql statement
    try:
        cursor.execute(query)
    except MySQLdb.Error as err:
        print('SQL ERROR: %s' % err)
        if 'Duplicate entry' not in err.args[1]:
            print(
                dump_sql_error(
                    cursor, datetime.utcnow(),
                    inspect.stack()[2][1],
                    inspect.stack()[1][3],
                    query, str(err)
                    )
                )
    else:
        print("OK")


def get_customer_database_config():
    return {
        'user': os.environ['DB_USERNAME'],
        'passwd': os.environ['DB_PASSWORD'],
        'host': os.environ['DB_HOSTNAME'],
        'db': os.environ['DB_UAT_NAME'],
        'charset': 'utf8',
    }


def get_database_connection(**config):
    """Initiates connection to database server\n
        return - database connection and cursor object
    """
    # initiate database connection
    con = MySQLdb.connect(**config)
    # get database cursor object
    cursr = con.cursor()

    return con, cursr


def concat_query(values, table_name):
    fields = ', '.join(values.keys())
    values = ', '.join("'%(" + k + ")s'" for k in values.keys())
    return "INSERT INTO %s (%s) VALUES (%s)" % (table_name, fields, values)


def datetime_handler(date):
    """parse dates for json dumping"""
    if isinstance(date, datetime):
        return str(date)
    else:
        return date


def db_data_to_json(db_data, headers):
    result = []
    for row in db_data:
        result.append(dict(zip(headers, list([datetime_handler(field) for field in row]))))
    return result
