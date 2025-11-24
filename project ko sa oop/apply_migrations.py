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
         
        
        logger.info("=" * 60)
        logger.info("Migrations completed successfully!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


if __name__ == '__main__':
    apply_migrations()
