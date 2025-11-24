"""
Password hashing and verification utilities.
Provides secure password handling without storing plaintext passwords.
"""
import bcrypt
from utils.logger import setup_logging

logger = setup_logging(__name__)


class PasswordManager:
    """Handles password hashing and verification using bcrypt."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plaintext password using bcrypt.
        
        Args:
            password: Plaintext password to hash
            
        Returns:
            Hashed password string
            
        Raises:
            ValueError: If password is empty or None
        """
        if not password or not isinstance(password, str):
            raise ValueError("Password must be a non-empty string")
        
        try:
            # Generate hash with salt rounds of 12 (default is 12, provides good security/speed balance)
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Error hashing password: {str(e)}")
            raise RuntimeError("Failed to hash password")
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a plaintext password against a hashed password.
        
        Args:
            password: Plaintext password to verify
            hashed_password: Previously hashed password from database
            
        Returns:
            True if password matches, False otherwise
        """
        if not password or not hashed_password:
            return False
        
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False
