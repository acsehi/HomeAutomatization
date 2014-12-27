from azure.storage import TableService, Entity
import time


class AzureDataServices:
    _partition = 'presence'

    def __init__(self, table):
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

    def insert_data(self, task, rowkey):
        """
        Insert the object to azure
        """
        task.PartitionKey = self._partition

        if  rowkey: 
            t = rowkey
        else:
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            
        task.RowKey = t
        self._table_service.insert_entity(self._partition, task)

    def update_data(self, task, rowkey):
        """
        Insert the object to azure
        """
        task.PartitionKey = self._partition
            
        task.RowKey = rowkey
        self._table_service.update_entity(self._partition, self._partition,rowkey, task)

    def insert_data(self, task):
        """
        Insert the object to azure
        """
        self.insert_data(self, task, None)

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