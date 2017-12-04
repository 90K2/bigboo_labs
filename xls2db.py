import argparse
import _mysql_exceptions
import xlrd

from database.general import get_customer_database_config, get_database_connection


def create_table(cursor, table_name, headers, one_data_row):
    """
    Create db table based on headers and one row with data for data type detection
    :param headers: column names list
    :param one_data_row: one row with data list
    :return: None
    """
    fields = []
    for i, f in enumerate(one_data_row):
        if "time" in headers[i].lower():
            fields.append("`%s` TIMESTAMP" % headers[i])
        else:
            if isinstance(f, int):
                fields.append("`%s` INT(10)" % headers[i])
            elif isinstance(f, str):
                if len(f) > 255:
                    fields.append("`%s` TEXT" % headers[i])
                else:
                    fields.append("`%s` VARCHAR(255)" % headers[i])
            elif isinstance(f, float):
                fields.append("`%s` FLOAT" % headers[i])

    query_draft = """
        CREATE TABLE %(table_name)s (
            %(fields)s
        )
    """ % {
        'table_name': table_name,
        'fields': ",".join(fields)
    }
    cursor.execute(query_draft)
    print("%s has been created" % table_name)


def main(input_file, db_connection):
    rb = xlrd.open_workbook(input_file, formatting_info=True)
    sheet_names = rb.sheet_names()
    for sheet in sheet_names:
        print('Processing -- %s' % sheet)
        focus_on = rb.sheet_by_name(sheet)
        headers = focus_on.row_values(0)
        table_name = '_'.join(sheet.lower().split())
        data_rows = list(range(focus_on.nrows))
        data_rows.pop(0)
        for i in data_rows:
            row_data = focus_on.row_values(i)
            print(row_data)
            with db_connection as cursor:
                inserted = False
                while not inserted:
                    try:
                        cursor.execute(
                            """
                            INSERT INTO %(table_name)s VALUES (%(values)s)
                            """ % {'table_name': table_name, 'values': ','.join(["\"" + str(v) + "\"" for v in row_data])}
                        )
                        connection.commit()
                        inserted = True
                    except _mysql_exceptions.ProgrammingError as e:
                        if "doesn't exist" in str(e):
                            print("%s does not exist, trying to create" % table_name)
                            create_table(cursor, table_name, headers, row_data)
                            connection.commit()

if __name__ == '__main__':
    usage = """"%prog --input-file </path/to/excel.xls>"""
    parser = argparse.ArgumentParser(description='Excel to MySQL convertor')
    parser.add_argument('--input-file', dest='input', action='store', type=str)
    args = parser.parse_args()
    if not args.input:
        parser.error(usage)

    db_config = get_customer_database_config()
    connection, _ = get_database_connection(**db_config)

    main(args.input, connection)
