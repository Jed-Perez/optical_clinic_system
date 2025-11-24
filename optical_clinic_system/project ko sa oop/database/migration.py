"""
Database migration and update utilities.
Handles schema changes, column additions, and data updates.
"""
from database.db_connection import Database
from utils.logger import setup_logging

logger = setup_logging(__name__)


class DatabaseMigration:
    """Handles database schema migrations and updates."""
    
    def __init__(self, db: Database):
        """
        Initialize migration handler.
        
        Args:
            db: Database connection instance
        """
        self.db = db
    
    def add_column(self, table_name, column_name, column_definition):
        """
        Add a column to a table if it doesn't exist.
        
        Args:
            table_name: Name of the table
            column_name: Name of the column to add
            column_definition: SQL definition (e.g., 'VARCHAR(100) NOT NULL DEFAULT ""')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if column exists
            columns = self.db.fetch(f"SHOW COLUMNS FROM {table_name}")
            column_names = [col['Field'] for col in columns]
            
            if column_name in column_names:
                logger.info(f"Column '{column_name}' already exists in table '{table_name}'")
                return True
            
            # Add column
            query = f"ALTER TABLE {table_name} ADD COLUMN `{column_name}` {column_definition}"
            self.db.execute(query)
            logger.info(f"Column '{column_name}' added to table '{table_name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to add column '{column_name}' to '{table_name}': {str(e)}")
            raise
    
    def modify_column(self, table_name, column_name, new_definition):
        """
        Modify a column's type or constraints.
        
        Args:
            table_name: Name of the table
            column_name: Name of the column to modify
            new_definition: New SQL definition
            
        Returns:
            True if successful, False otherwise
        """
        try:
            query = f"ALTER TABLE {table_name} MODIFY COLUMN `{column_name}` {new_definition}"
            self.db.execute(query)
            logger.info(f"Column '{column_name}' in table '{table_name}' modified")
            return True
        except Exception as e:
            logger.error(f"Failed to modify column '{column_name}' in '{table_name}': {str(e)}")
            raise
    
    def drop_column(self, table_name, column_name):
        """
        Drop a column from a table.
        
        Args:
            table_name: Name of the table
            column_name: Name of the column to drop
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if column exists first
            columns = self.db.fetch(f"SHOW COLUMNS FROM {table_name}")
            column_names = [col['Field'] for col in columns]
            
            if column_name not in column_names:
                logger.info(f"Column '{column_name}' doesn't exist in table '{table_name}'")
                return True
            
            query = f"ALTER TABLE {table_name} DROP COLUMN `{column_name}`"
            self.db.execute(query)
            logger.info(f"Column '{column_name}' dropped from table '{table_name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to drop column '{column_name}' from '{table_name}': {str(e)}")
            raise
    
    def rename_column(self, table_name, old_name, new_name, definition):
        """
        Rename a column.
        
        Args:
            table_name: Name of the table
            old_name: Current column name
            new_name: New column name
            definition: Column definition (required for rename)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            query = f"ALTER TABLE {table_name} CHANGE COLUMN `{old_name}` `{new_name}` {definition}"
            self.db.execute(query)
            logger.info(f"Column '{old_name}' renamed to '{new_name}' in table '{table_name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to rename column in '{table_name}': {str(e)}")
            raise
    
    def add_index(self, table_name, index_name, columns):
        """
        Add an index to a table.
        
        Args:
            table_name: Name of the table
            index_name: Name of the index
            columns: List of column names or single column name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if isinstance(columns, str):
                columns = [columns]
            
            columns_str = ', '.join([f"`{col}`" for col in columns])
            query = f"ALTER TABLE {table_name} ADD INDEX `{index_name}` ({columns_str})"
            self.db.execute(query)
            logger.info(f"Index '{index_name}' added to table '{table_name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to add index '{index_name}' to '{table_name}': {str(e)}")
            raise
    
    def add_foreign_key(self, table_name, fk_name, column_name, ref_table, ref_column):
        """
        Add a foreign key constraint.
        
        Args:
            table_name: Name of the table
            fk_name: Name of the foreign key
            column_name: Column in this table
            ref_table: Referenced table name
            ref_column: Referenced column name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            query = f"""ALTER TABLE {table_name} 
                       ADD CONSTRAINT `{fk_name}` 
                       FOREIGN KEY (`{column_name}`) 
                       REFERENCES {ref_table}(`{ref_column}`)"""
            self.db.execute(query)
            logger.info(f"Foreign key '{fk_name}' added to table '{table_name}'")
            return True
        except Exception as e:
            logger.error(f"Failed to add foreign key '{fk_name}' to '{table_name}': {str(e)}")
            raise
    
    def create_table(self, table_name, table_definition):
        """
        Create a new table.
        
        Args:
            table_name: Name of the table
            table_definition: SQL CREATE TABLE definition
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if table exists
            tables = self.db.fetch("SHOW TABLES")
            table_names = [list(row.values())[0] for row in tables]
            
            if table_name in table_names:
                logger.info(f"Table '{table_name}' already exists")
                return True
            
            self.db.execute(table_definition)
            logger.info(f"Table '{table_name}' created")
            return True
        except Exception as e:
            logger.error(f"Failed to create table '{table_name}': {str(e)}")
            raise
    
    def update_data(self, table_name, updates_dict, where_clause=None):
        """
        Update data in a table.
        
        Args:
            table_name: Name of the table
            updates_dict: Dict of {column: new_value}
            where_clause: WHERE condition (optional)
            
        Returns:
            Number of affected rows
        """
        try:
            set_clause = ', '.join([f"`{k}`=%s" for k in updates_dict.keys()])
            values = list(updates_dict.values())
            
            query = f"UPDATE {table_name} SET {set_clause}"
            if where_clause:
                query += f" WHERE {where_clause}"
            
            result = self.db.execute(query, tuple(values))
            logger.info(f"Updated {result} rows in table '{table_name}'")
            return result
        except Exception as e:
            logger.error(f"Failed to update data in '{table_name}': {str(e)}")
            raise
    
    def backup_table(self, table_name, backup_name=None):
        """
        Create a backup copy of a table.
        
        Args:
            table_name: Name of the table to backup
            backup_name: Name of the backup table (default: {table_name}_backup_{timestamp})
            
        Returns:
            Name of backup table
        """
        try:
            from datetime import datetime
            
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{table_name}_backup_{timestamp}"
            
            query = f"CREATE TABLE {backup_name} AS SELECT * FROM {table_name}"
            self.db.execute(query)
            logger.info(f"Table '{table_name}' backed up to '{backup_name}'")
            return backup_name
        except Exception as e:
            logger.error(f"Failed to backup table '{table_name}': {str(e)}")
            raise
    
    def get_table_info(self, table_name):
        """
        Get detailed information about a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dict with table structure information
        """
        try:
            columns = self.db.fetch(f"SHOW COLUMNS FROM {table_name}")
            indexes = self.db.fetch(f"SHOW INDEXES FROM {table_name}")
            
            return {
                'table_name': table_name,
                'columns': columns,
                'indexes': indexes
            }
        except Exception as e:
            logger.error(f"Failed to get info for table '{table_name}': {str(e)}")
            raise
