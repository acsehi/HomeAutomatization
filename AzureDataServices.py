from azure.storage import TableService, Entity
import time
import os
import azure


class AzureDataServices:
    _partition = 'presence'

    def __init__(self, table):

        if os.environ.get('raspberry') is None:
            # Test table for dev environments
            table += 'Test'

        self._partition = table
        with open('azure.txt') as f:
            lines = f.readlines()
        acc = lines[0].strip()
        key = lines[1].strip()
        self._table_service = TableService(account_name=acc, account_key=key)
    
    def create_table(self):
        """
        Creates azure storage table
        """
        self._table_service.create_table(self._partition)

    def insert_data(self, task):
        """
        Insert the object to azure
        """
        self.insert_data_with_key(task, None)

    def insert_data_with_key(self, task, row_key):
        """
        Insert the object to azure
        """
        task.PartitionKey = self._partition

        if row_key:
            t = row_key
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            
        task.RowKey = t
        self._table_service.insert_entity(self._partition, task)

    def update_or_insert(self, task, row_key):
        """
        Update or insert the object to azure
        """
        task.PartitionKey = self._partition
        task.RowKey = row_key

        try:
            self._table_service.update_entity(self._partition, self._partition,row_key, task)
        except azure.WindowsAzureMissingResourceError:
            self._table_service.insert_entity(self._partition, task)

    def insert_presence(self, p):
        """
        Uploads value to azure table storage
        """
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        task = Entity()
        task.PartitionKey = self._partition
        task.RowKey = t

        task.users_arrived = ','.join(map(str, p.users_arrived)) 
        task.users_left = ','.join(map(str, p.users_left)) 

        self._table_service.insert_entity(self._partition, task)

    def get_presence(self):
        tasks = self._table_service.query_entities(self._partition, "PartitionKey eq 'presence'")
        return tasks