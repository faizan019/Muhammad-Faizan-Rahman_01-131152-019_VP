#!/usr/bin/env python
# coding: utf-8

# In[1]:


import arrow
import os
import json
import base64
import logging
from string import Template
# from dotenv import load_dotenv
import google.auth
from google.cloud import bigquery
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# load_dotenv()
from ws_kpi import kpi_function
# from backfill import backfill
# GOOGLE_CLOUD_PROJECT = os.environ['PROJECT_ID']
# CLIENT_ID = os.environ['CLIENT_ID']
def main(event, context):
    def read_firebase():
        firebase_admin.initialize_app(options={'databaseURL': f'https://{GOOGLE_CLOUD_PROJECT}.firebaseio.com', })
        db = firestore.client()
        collections = db.collection('client_configs').document(CLIENT_ID).collections()
        config_json = {}
        for collection in collections:
            for doc in collection.stream():
                if doc.id in ['kpi_config','ws_config','main_config']:
                    config_json[doc.id] = doc.to_dict()
        doc_ref = db.collection('client_configs').document(CLIENT_ID).get()
        client_id = doc_ref.to_dict()['client_id']
        config_json['client_id'] = client_id
        firebase_admin.delete_app(firebase_admin.get_app())
        return config_json
    # payload = read_firebase()
    # with open("payload.json", "w") as outfile:
    #     json.dump(payload, outfile)
    with open('payload.json') as file:
        payload = json.loads(file.read())
        file.close()
    client_id = payload['client_id']
    config = payload['kpi_config']
    timezone = payload['main_config']['timezone']
    device_id = payload['ws_config']['device_id']
    # start_time = arrow.utcnow().floor('day').shift(hours=-24)
    # end_time = arrow.utcnow().floor('day').shift(minutes=-15)
    start_time = arrow.get('2022-12-01 00:00:00')
    end_time = arrow.get('2022-12-31 23:45:00')
    kwargs = {
        'start_time': start_time,
        'end_time': end_time,
        'project': os.environ.get('PROJECT_ID'),
        'client_id': client_id,
        'dataset_src': os.environ.get('SRC_DATASET_ID'),
        'location': os.environ.get('LOCATION'),
        'dataset_dest': os.environ.get('DEST_DATASET_ID'),
        'table_src': os.environ.get('SRC_TABLE_ID'),
        'table_dest': os.environ.get('DEST_TABLE_ID'),
        'config': config,
        'device_id': device_id
    }
    print(kwargs)
    kpi_function(kwargs)
if __name__ == '__main__':
    main('event', 'content')


# In[ ]:




