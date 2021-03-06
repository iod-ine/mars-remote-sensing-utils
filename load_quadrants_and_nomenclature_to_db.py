#!python

import pathlib
import psycopg2
import numpy as np
import pandas as pd
from tools import sql

data_root = pathlib.Path('/Users/ivan/Projects/Data/Mars/')

connection = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mars_remote_sensing',
    'user': 'markwatney',
    'password': 'no one knows :) secret :)',
}

quadrants = data_root / 'Vectors' / 'Quadrants' / 'quadrants.csv'
nomenclature = data_root / 'Vectors' / 'Nomenclature' / 'nomenclature_exported.csv'

qd = pd.read_csv(quadrants)
nm = pd.read_csv(nomenclature)

nm['center_lon_180'] = np.where(nm['center_lon'] >= 180, nm['center_lon'] - 360, nm['center_lon'])
nm['min_lon_180'] = np.where(nm['min_lon'] >= 180, nm['min_lon'] - 360, nm['min_lon'])
nm['max_lon_180'] = np.where(nm['max_lon'] >= 180, nm['max_lon'] - 360, nm['max_lon'])

query0 = sql.generate_sql_insert_statement_for_quadrants(qd)
query1 = sql.generate_sql_insert_statement_for_nomenclature(nm)

with psycopg2.connect(**connection) as conn:
    cur = conn.cursor()
    cur.execute(query0)
    cur.execute(query1)
    conn.commit()
