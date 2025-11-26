from database.db_connection import Database
from abc import ABC, abstractmethod


class BaseManager(ABC):
    
    def __init__(self, db: Database):
        self.db = db
        self.table_name = None
        self.archived_table_name = None
        self.id_column = None
    
    def archive(self, record_id):
        if not self.table_name or not self.archived_table_name or not self.id_column:
            raise NotImplementedError("Subclass must define table_name, archived_table_name, and id_column")
        
        try:
            columns = self.db.fetch(f"SHOW COLUMNS FROM {self.table_name}")
            column_names = [col['Field'] for col in columns]
            column_list = ", ".join(column_names)
            
            archive_query = f"""
                INSERT INTO {self.archived_table_name} ({column_list}, Deleted_On)
                SELECT {column_list}, NOW()
                FROM {self.table_name} WHERE {self.id_column}=%s
            """
            self.db.execute(archive_query, (record_id,))
            
            self.db.execute(f'DELETE FROM {self.table_name} WHERE {self.id_column}=%s', (record_id,))
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to archive {self.table_name} record: {str(e)}")
    
    def restore(self, record_id):
        if not self.table_name or not self.archived_table_name or not self.id_column:
            raise NotImplementedError("Subclass must define table_name, archived_table_name, and id_column")
        
        try:
            row = self.db.fetch(f'SELECT * FROM {self.archived_table_name} WHERE {self.id_column}=%s', (record_id,))
            if not row:
                return None
            
            record = row[0]
            columns = self.db.fetch(f"SHOW COLUMNS FROM {self.table_name}")
            column_names = [col['Field'] for col in columns]
            
            # Build insert values
            placeholders = ', '.join(['%s'] * len(column_names))
            column_list = ', '.join(column_names)
            
            values = tuple(record.get(col) for col in column_names)
            
            insert_query = f'INSERT INTO {self.table_name} ({column_list}) VALUES ({placeholders})'
            self.db.execute(insert_query, values)
            
            self.db.execute(f'DELETE FROM {self.archived_table_name} WHERE {self.id_column}=%s', (record_id,))
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to restore {self.table_name} record: {str(e)}")
    
    def list_archived(self):
        if not self.archived_table_name:
            raise NotImplementedError("Subclass must define archived_table_name")
        
        query = f'SELECT * FROM {self.archived_table_name} ORDER BY Deleted_On DESC'
        return self.db.fetch(query)
    
    @abstractmethod
    def validate_input(self, **kwargs):
        pass
