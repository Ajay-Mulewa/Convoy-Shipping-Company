import csv
import json
import pandas as pd
import sqlite3
import re
from lxml import etree


def excel_to_csv(excel_file):
    dataframe = pd.read_excel(excel_file, sheet_name='Vehicles', dtype=str)
    lines = dataframe.shape[0]

    csv_file = excel_file.replace('.xlsx', '.csv')
    dataframe.to_csv(csv_file, index=False)

    print(f'{lines} line{"s were" if lines > 1 else " was"} imported to {csv_file}')

    correct_csv_file(csv_file)


def correct_cells(reader, writer):
    counter = 0
    row_counter = 0
    for row in reader:
        if row_counter == 0:
            row_counter += 1
            writer.writerow([header for header in row])
            continue
        list_ = list()
        for cell in row:
            if not cell.isnumeric():
                counter += 1
                list_.append(re.sub('\\D', '', cell))
            else:
                list_.append(cell)
        writer.writerow(list_)
    return counter


def correct_csv_file(csv_file):
    dest_file = "[CHECKED].".join(csv_file.split('.'))

    with open(csv_file, newline='') as csv_file, \
            open(dest_file, 'w', encoding='utf-8') as dest_csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        writer = csv.writer(dest_csv_file, delimiter=',', lineterminator='\n')
        counter = correct_cells(reader, writer)

    print(f'{counter} cell{"s were" if counter > 1 else " was"} corrected in {dest_file}')

    export_to_database(dest_file)


def extract_header(reader):
    command = 'CREATE TABLE IF NOT EXISTS convoy ('
    header = next(reader)
    for column in header:
        if column == 'vehicle_id':
            command += '{} INTEGER NOT NULL PRIMARY KEY, '.format(column)
        else:
            command += '{} INTEGER NOT NULL, '.format(column)
    command += 'score NOT NULL)'
    return command


def calculate_score(vehicle_data):
    route_length = 450
    fuel_used = int(vehicle_data[2]) * route_length / 100
    efficiency_score = 2 if fuel_used <= 230 else 1
    capacitance_score = 2 if int(vehicle_data[3]) >= 20 else 0
    if fuel_used < int(vehicle_data[1]):
        refueling_score = 2
    elif fuel_used < int(vehicle_data[1]) * 2:
        refueling_score = 1
    else:
        refueling_score = 0
    return refueling_score + efficiency_score + capacitance_score


def insert_values(iterable_values):
    query = 'INSERT INTO convoy VALUES ('
    for value in iterable_values:
        query += '{}, '.format(value)
    query += '{})'.format(calculate_score(iterable_values))
    return query


def export_to_database(checked_file):
    database = checked_file.replace('[CHECKED].csv', '.s3db')
    conn = sqlite3.connect(database)
    cursor_name = conn.cursor()
    with open(checked_file, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        create_table_command = extract_header(reader)
        cursor_name.execute('DROP TABLE IF EXISTS convoy')
        cursor_name.execute(create_table_command)
        count_records = 0
        for row in reader:
            cursor_name.execute(insert_values(row))
            count_records += 1
            conn.commit()
        conn.close()

    print(f'{count_records} record{"s were" if count_records > 1 else " was"} added to {database}')

    import_database_to_json(database)
    import_database_to_xml(database)


def import_database_to_json(file_name):
    new_file_name = file_name.replace('.s3db', '.json')
    con = sqlite3.connect(file_name)

    query = pd.read_sql('SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load from convoy '
                        'WHERE score > 3', con)
    b = query.to_dict(orient='records')
    m = {'convoy': b}
    con.close()

    with open(new_file_name, 'w', encoding='utf-8') as json_file:
        json.dump(m, json_file)

    print(f"{query.shape[0]} vehicle{'s were' if query.shape[0] > 1 else ' was'} saved into {new_file_name}")


def import_database_to_xml(database):
    dest_file = database.replace('.s3db', '.xml')
    conn = sqlite3.connect(database)

    query = pd.read_sql('SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load from convoy '
                        'WHERE score <= 3', conn)

    if query.shape[0] == 0:
        root = etree.Element('convoy')
        tree = etree.ElementTree(root)
        tree.write(dest_file, method='html')
        print(f'0 vehicles were saved to {dest_file}')
    else:
        query.to_xml(f'{dest_file}', index=False, xml_declaration=False, root_name='convoy', row_name='vehicle')
        print(f'{query.shape[0]} vehicle{"s were" if query.shape[0] > 1 else " was"} saved into {dest_file}')


def handler(file_name):
    if file_name.endswith('.xlsx'):
        excel_to_csv(file_name)
    elif file_name.endswith('[CHECKED].csv'):
        export_to_database(file_name)
    elif file_name.endswith('.csv'):
        correct_csv_file(file_name)
    elif file_name.endswith('.s3db'):
        import_database_to_json(file_name)
        import_database_to_xml(file_name)
    else:
        print('File format is not supported')


print('Input file name')
file_ = input()

handler(file_)