#!/usr/bin/env python3

import sys
import os
import sqlite3
import csv
from datetime import datetime


import sys
if len(sys.argv) > 1:
    param1 = sys.argv[1]
else:
    print('Error: expected parameter: %s <csv dir|file> '%sys.argv[0])
    quit(1)


csv_source = param1
#csv_source = '/mnt/invest/easynvest/resumos/' # all .csv files from directory
#csv_source = '/mnt/invest/easynvest/resumos/ResumoNegociacao_2019-12-31.csv'


# TODO load from ignore_import.(json or txt)
ignore_ixs=[]

''' # example:
ignore_ixs=[
    '2020-06-24,CSAN3,68.72', # desmembramento da CSAN3 em 4
    '2020-06-24,CSAN3,17.18',
    '2020-03-08,CMIG3F,5.0', # bonificacao (12 papeis)
    '2020-11-03,ROMI3F,13.91', # bonificacao (33 papeis)
]
'''


# ---------------------------------




if 'INVEST_MONITOR_DB' not in os.environ:
    print('INVEST_MONITOR_DB does not setted!')
    quit()


db_file = os.path.abspath(os.environ['INVEST_MONITOR_DB'])


if not os.path.exists(db_file):
    print('ERROR: '+db_file+' does not exist!')
    quit()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()




def load_csv_content(file, operations_map):
    print('Reading from '+file)
    with open(file, encoding='iso-8859-1') as csvfile:
        csvfile.readline() # pass sep=
        csvfile.readline() # pass original field names

        fieldnames = ['data', 'conta', 'ativo', 'preco', 'qtde_compra', 'qtde_venda', 'total_compra', 'total_venda']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')

        for row in reader:
            row['data'] = datetime.strftime(datetime.strptime(row['data'], '%d/%m/%Y'), '%Y-%m-%d')
            row['preco'] = float(row['preco'].replace('.','').replace(',','.'))
            row['qtde_compra'] = int(row['qtde_compra'])
            row['qtde_venda'] = int(row['qtde_venda'])

            ix = row['data']+','+row['ativo']+','+str(row['preco']) # cria um indice pra unificar operacoes fragmentadas (comum em FIIs)
            if ix not in operations_map:
                operations_map[ix] = row
            else:
                operations_map[ix]['qtde_compra'] = operations_map[ix]['qtde_compra'] + row['qtde_compra']
                operations_map[ix]['qtde_venda'] = operations_map[ix]['qtde_venda'] + row['qtde_venda']



if not os.path.exists(csv_source):
    print('File or directory '+csv_source+' does not exist!')



operations_map = {}

if os.path.isdir(csv_source):
    for file in sorted(os.listdir(csv_source)):
        load_csv_content( os.path.join(csv_source,file) , operations_map)
else:
    load_csv_content(csv_source, operations_map)


## convert map to list
#operations_list = [operations_map[ix] for ix in operations_map.keys()]
## sort by date
#operations_list = sorted(operations_list, key=lambda op: op['data'])

datainserts = []

operations_keys = sorted(operations_map.keys())

for ix in operations_keys:
    if ix in ignore_ixs:
        continue
    op = operations_map[ix]
    values = (op['ativo'], op['preco'], op['qtde_venda'], op['qtde_compra'], op['data'] )
    cursor.execute("SELECT * FROM operation WHERE ticker = ? AND price = ? AND sell = ? AND buy = ? AND date = ?", values)
    if cursor.fetchone() == None:
        datainserts.append(values)
        print('ADD > '+str(values))
    else:
        #print('exist > '+ix)
        pass

cursor.executemany("INSERT INTO operation (ticker, price, sell, buy, date) VALUES (?, ?, ?, ?, ?)", datainserts)
conn.commit()


cursor.execute("SELECT ticker, price, sell, buy, date FROM operation ORDER BY date")
for row in cursor.fetchall():
    ops = {
        'ticker': row[0], 
        'price': row[1], 
        'sell': row[2], 
        'buy': row[3], 
        'date': row[4]
    }
    ix = ops['date']+','+ops['ticker']+','+str(ops['price'])

    if ix in ignore_ixs:
        continue

    if ix in operations_keys:
        opi = operations_map[ix]
        if ops['sell'] != opi['qtde_venda'] or ops['buy'] != opi['qtde_compra']:
            print('not match > '+str(ops)+'  < '+str(opi['qtde_venda'])+' - '+str(opi['qtde_compra']))
        else:
            #print('match > '+ix)
            pass
    else:
        print('not found > '+str(ops))

conn.close()
