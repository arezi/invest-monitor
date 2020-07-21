

csv_source = '/home/fabio/Dropbox/invest/easynvest/resumos/' # all .csv files from directory
#csv_source = '/home/fabio/Dropbox/invest/easynvest/resumos/ResumoNegociacao_2019-12-31.csv'
#csv_source = '/home/fabio/Downloads/ResumoNegociacao_2019-12-31.csv'



# ---------------------------------


import os
import sqlite3
import csv
from datetime import datetime




if 'INVEST_MONITOR_DB' not in os.environ:
    print('INVEST_MONITOR_DB does not setted!')
    quit()


db_file = os.path.abspath(os.environ['INVEST_MONITOR_DB'])


if not os.path.exists(db_file):
    print('ERROR: '+db_file+' does not exist!')
    quit()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()




def load_csv_content(file, operations):
    print('Reading from '+file)
    with open(file, encoding='iso-8859-1') as csvfile:
        csvfile.readline() # pass sep=
        csvfile.readline() # pass original field names
        fieldnames = ['data', 'conta', 'ativo', 'preco', 'qtde_compra', 'qtde_venda', 'total_compra', 'total_venda']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=';')
        for row in reader:
            row['data'] = datetime.strftime(datetime.strptime(row['data'], '%d/%m/%Y'), '%Y-%m-%d')
            row['preco'] = row['preco'].replace('.','').replace(',','.')
            ix = row['data']+row['ativo']+row['preco'] # cria um indice pra unificar operacoes fragmentadas (comum em FIIs)
            if ix not in operations:
                operations[ix] = row
            else:
                operations[ix]['qtde_compra'] = int(operations[ix]['qtde_compra']) + int(row['qtde_compra'])
                operations[ix]['qtde_venda'] = int(operations[ix]['qtde_venda']) + int(row['qtde_venda'])
    return operations



if not os.path.exists(csv_source):
    print('File or directory '+csv_source+' does not exist!')



operations = {}

if os.path.isdir(csv_source):
    for file in os.listdir(csv_source):
        load_csv_content( os.path.join(csv_source,file) , operations)
else:
    load_csv_content(csv_source, operations)


# convert map to list
operations = [operations[ix] for ix in operations.keys()]

# sort by date
operations = sorted(operations, key=lambda op: op['data'])

datainserts = []

for op in operations:
    values = (op['ativo'], op['preco'], op['qtde_compra'], op['qtde_venda'], op['data'] )
    cursor.execute("SELECT * FROM operation WHERE ticker = ? AND price = ? AND buy = ? AND sell = ? AND date = ?", values)
    if cursor.fetchone() == None:
        datainserts.append(values)
        print('ADD > '+str(values))
    else:
        print('exist > '+str(values))
 

cursor.executemany("INSERT INTO operation (ticker, price, buy, sell, date) VALUES (?, ?, ?, ?, ?)", datainserts)

conn.commit()

conn.close()
