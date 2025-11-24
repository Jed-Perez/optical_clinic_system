"""
Application-wide constants to avoid magic numbers and hardcoded values.
"""

# Billing and Financial Constants
DEFAULT_TAX_RATE = 0.12  # 12% tax
INVOICE_TAX_RATE = DEFAULT_TAX_RATE

# Prescription Constants
PRESCRIPTION_VALIDITY_DAYS = 365  # 1 year validity
PRESCRIPTION_EXPIRY_WARNING_DAYS = 30  # Warn 30 days before expiry

# Medical Records Constants
DEFAULT_FOLLOWUP_DAYS = 90

# Password Policy Constants
MIN_PASSWORD_LENGTH = 8
PASSWORD_HASH_ALGORITHM = "bcrypt"  # Options: 'bcrypt', 'argon2'

# UI Constants
APP_TITLE = "Optical Clinic - Dashboard"
LOGIN_WINDOW_TITLE = "Clinic Login"
APP_GEOMETRY = "1100x700"
LOGIN_GEOMETRY = "420x300"
SIDEBAR_WIDTH = 200
HEADER_HEIGHT = 70

# Database Constants
DATABASE_NAME = "optical_clinic_db"
CURSOR_TYPE = "dictionary"  # MySQL connector cursor type

# Appearance Constants
APPEARANCE_MODE = "dark"
COLOR_THEME = "dark-blue"

# Logging Constants
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "logs/clinic_system.log"

# Error Messages
ERROR_INVALID_CREDENTIALS = "Invalid username or password"
ERROR_DB_CONNECTION = "Failed to connect to database. Please check:\n1. MySQL server is running\n2. Database credentials in database/db_config.py are correct\n3. Database '{}' exists"
ERROR_DUPLICATE_BOOKING = "Double booking detected for this time slot"
ERROR_GENERIC = "An unexpected error occurred"

# Success Messages
SUCCESS_USER_CREATED = "User created successfully"
SUCCESS_RECORD_ARCHIVED = "Record archived successfully"
SUCCESS_RECORD_RESTORED = "Record restored successfully"
