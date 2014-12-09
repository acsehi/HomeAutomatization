from azure.storage import TableService, Entity
import time
import json


class AzureDataServices:
    _partition = 'presence'

    def __init__(self):
        with open('azure.txt') as f:
            lines = f.readlines()
        acc = lines[0].strip()
        key = lines[1].strip()
        self._table_service = TableService(account_name=acc, account_key=key)
    
    def create_table(self):
        '''
        Creates azure storage table
        '''
        self._table_service.create_table(self._partition)
    
    def insert_presence(self, p):
        '''
        Uploads value to azure table storage
        '''
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        task = Entity()
        task.PartitionKey = self._partition
        task.RowKey = t

        task.users_arrived = ','.join(map(str, p.users_arrived)) 
        task.users_left = ','.join(map(str, p.users_left)) 

        self._table_service.insert_entity(self._partition, task)

    def get_presence(self):
        tasks = self._table_service.query_entities('presence', "PartitionKey eq 'presence'")
        return tasks