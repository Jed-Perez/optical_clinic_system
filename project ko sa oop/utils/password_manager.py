import bcrypt
from utils.logger import setup_logging

logger = setup_logging(__name__)


class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        if not password or not isinstance(password, str):
            raise ValueError("Password must be a non-empty string")
        
        try:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Error hashing password: {str(e)}")
            raise RuntimeError("Failed to hash password")
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        if not password or not hashed_password:
            return False
        
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False
