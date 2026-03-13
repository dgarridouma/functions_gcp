import csv
import json
import requests
import datetime
from google.cloud import bigquery
import functions_framework

# filename: must be main.py
# functions_framework --target hello_http --debug
#
# http://127.0.0.1:8080 
#
# curl -X POST http://localhost:8080 -H "Content-Type: application/json" -d "{}"
@functions_framework.http
def hello_http(request):
    client = bigquery.Client()
    dataset_id = 'midataset'  # replace with your dataset ID
    table_id = 'parkings'  # replace with your table ID
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)
    
    url='https://datosabiertos.malaga.eu/recursos/aparcamientos/ocupappublicosmun/catalogo.csv'
    catalogo=dict()
    headers = {'User-Agent': 'myagent'}
    response=requests.get(url,headers=headers)
    response.encoding='utf-8'
    reader = csv.reader(response.text.splitlines(),delimiter=',')
    header_row = next(reader)
    try:
        for row in reader:
            #print(row[0])
            #print(row[1])
            catalogo[row[0]]=row[1]

        rows_to_insert = []
        url = 'https://datosabiertos.malaga.eu/recursos/aparcamientos/ocupappublicosmun/ocupappublicosmun.csv'
        headers = {'User-Agent': 'myagent'}
        response=requests.get(url,headers=headers)
        response.encoding='utf-8'
        reader = csv.reader(response.text.splitlines(),delimiter=',')
        header_row = next(reader)
        when=datetime.datetime.utcnow().replace(microsecond=0)
        for row in reader:
            if len(row)<1 or (not row[0].startswith("OCUPACION")):
                continue

            print(row[1])

            try:
                data={
                    'id': row[1],
		            'name': catalogo[row[1]],
                    'free': row[2],
                    'when': str(when)                
                }
                json_data=json.dumps(data)
                print(json_data)
                rows_to_insert.append(data)
                json_data=json.dumps(data)           

            except:
                pass        

    except:
        pass

    errors = client.insert_rows(table, rows_to_insert)  # API request
    print(errors)
    return f'Insertado!'
