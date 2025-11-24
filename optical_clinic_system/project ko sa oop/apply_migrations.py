"""
Database migration scripts for common updates.
Run this file to apply migrations to your database.

Usage:
    python apply_migrations.py
"""
from database.db_connection import Database
from database.migration import DatabaseMigration
from utils.logger import setup_logging

logger = setup_logging(__name__)


def apply_migrations():
    """Apply all pending database migrations."""
    
    try:
        db = Database(raise_on_error=True)
        migration = DatabaseMigration(db)
        
        logger.info("=" * 60)
        logger.info("Starting Database Migrations")
        logger.info("=" * 60)
        
        # ===== EXAMPLE MIGRATIONS (Uncomment to use) =====
        
        # 1. ADD NEW COLUMNS TO PATIENTS TABLE
        # migration.add_column('patients', 'Phone_Backup', "VARCHAR(20) DEFAULT NULL")
        # migration.add_column('patients', 'Blood_Type', "VARCHAR(10) DEFAULT NULL")
        # migration.add_column('patients', 'Emergency_Contact', "VARCHAR(100) DEFAULT NULL")
        
        # 2. ADD NEW COLUMNS TO DOCTORS TABLE
        # migration.add_column('doctors', 'Email', "VARCHAR(100) DEFAULT NULL")
        # migration.add_column('doctors', 'Phone', "VARCHAR(20) DEFAULT NULL")
        # migration.add_column('doctors', 'Available', "BOOLEAN DEFAULT TRUE")
        
        # 3. CREATE NEW TABLE FOR MEDICAL HISTORY
        # medical_history_table = """
        #     CREATE TABLE `medical_history` (
        #       `History_ID` int NOT NULL AUTO_INCREMENT,
        #       `Patient_ID` int NOT NULL,
        #       `Condition` varchar(255) NOT NULL,
        #       `Date_Diagnosed` date NOT NULL,
        #       `Status` varchar(50) DEFAULT 'Active',
        #       PRIMARY KEY (`History_ID`),
        #       FOREIGN KEY (`Patient_ID`) REFERENCES patients(`Patient_ID`)
        #     ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        # """
        # migration.create_table('medical_history', medical_history_table)
        
        # 4. ADD INDEXES FOR BETTER PERFORMANCE
        # migration.add_index('patients', 'idx_contact', 'Contact')
        # migration.add_index('patients', 'idx_gender', 'Gender')
        # migration.add_index('appointments', 'idx_patient', 'Patient_ID')
        # migration.add_index('appointments', 'idx_doctor', 'Doctor_ID')
        
        # 5. MODIFY EXISTING COLUMNS
        # migration.modify_column('patients', 'Contact', "VARCHAR(20) NOT NULL UNIQUE")
        # migration.modify_column('doctors', 'License_No', "VARCHAR(50) NOT NULL UNIQUE")
        
        # 6. UPDATE DATA IN EXISTING RECORDS
        # migration.update_data('patients', {'Age_Group': 'Adult'}, "Age >= 18")
        # migration.update_data('patients', {'Age_Group': 'Kids'}, "Age < 18")
        
        # 7. BACKUP TABLE BEFORE MAJOR CHANGES
        # backup_name = migration.backup_table('patients')
        # logger.info(f"Backup created: {backup_name}")
        
        # 8. GET TABLE INFORMATION
        # table_info = migration.get_table_info('patients')
        # logger.info(f"Table structure: {table_info}")
        
        # ===== UNCOMMENT AND MODIFY AS NEEDED =====
        
        logger.info("=" * 60)
        logger.info("Migrations completed successfully!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


if __name__ == '__main__':
    apply_migrations()
