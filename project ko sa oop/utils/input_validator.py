from utils.logger import setup_logging
from utils.ui_constants import MSG_REQUIRED, MSG_INVALID_FORMAT, MSG_INVALID_NUMBER

logger = setup_logging(__name__)


class InputValidator:
    @staticmethod
    def validate_required(value, field_name):
        if not value or (isinstance(value, str) and not value.strip()):
            return False, MSG_REQUIRED.format(field=field_name)
        return True, None
    
    @staticmethod
    def validate_integer(value, field_name):
        try:
            converted = int(str(value).strip())
            return True, None, converted
        except (ValueError, TypeError):
            return False, f"{field_name} must be a whole number", None
    
    @staticmethod
    def validate_float(value, field_name):
        try:
            converted = float(str(value).strip())
            if converted < 0:
                return False, f"{field_name} cannot be negative", None
            return True, None, converted
        except (ValueError, TypeError):
            return False, MSG_INVALID_NUMBER.format(field=field_name), None
    
    @staticmethod
    def validate_phone(value, field_name="Phone"):
        is_valid, error = InputValidator.validate_required(value, field_name)
        if not is_valid:
            return False, error
        
        # Remove common separators
        cleaned = str(value).replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        
        if not cleaned.isdigit() or len(cleaned) < 7:
            return False, f"{field_name} must be a valid phone number"
        
        return True, None
    
    @staticmethod
    def validate_email(value, field_name="Email"):
        if not value or not str(value).strip():
            # Email might be optional, return True with empty email
            return True, None
        
        email = str(value).strip()
        if '@' not in email or '.' not in email:
            return False, f"{field_name} format is invalid"
        
        return True, None
    
    @staticmethod
    def validate_date(year, month, day):
        try:
            from datetime import datetime
            year_int = int(year)
            month_int = int(month)
            day_int = int(day)
            
            if month_int < 1 or month_int > 12:
                return False, "Month must be between 1 and 12"
            if day_int < 1 or day_int > 31:
                return False, "Day must be between 1 and 31"
            
            datetime(year_int, month_int, day_int)
            return True, None
        except ValueError as e:
            return False, f"Invalid date: {str(e)}"
    
    @staticmethod
    def validate_time(hour, minute):
        try:
            hour_int = int(hour)
            minute_int = int(minute)
            
            if hour_int < 0 or hour_int > 23:
                return False, "Hour must be between 0 and 23"
            if minute_int < 0 or minute_int > 59:
                return False, "Minute must be between 0 and 59"
            
            return True, None
        except ValueError:
            return False, "Invalid time format"
    
    @staticmethod
    def validate_combobox_selection(value, field_name):
        if not value or str(value).startswith("Select"):
            return False, f"Please select a {field_name}"
        
        return True, None
    
    @staticmethod
    def sanitize_string(value, max_length=None):
        cleaned = str(value).strip()
        
        if max_length:
            cleaned = cleaned[:max_length]
        
        return cleaned
    
    @staticmethod
    def validate_age(age_value):
        is_valid, error, value = InputValidator.validate_integer(age_value, "Age")
        if not is_valid:
            return False, error, None
        
        if value < 0 or value > 150:
            return False, "Age must be between 0 and 150", None
        
        return True, None, value
    
    @staticmethod
    def get_age_group(age):
        try:
            age_int = int(age) if age else 0
            return "Kids" if age_int < 18 else "Adult"
        except (ValueError, TypeError):
            return "Adult" 