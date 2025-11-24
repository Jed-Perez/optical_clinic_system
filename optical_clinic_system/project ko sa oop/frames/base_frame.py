"""
Base frame class for all GUI frames.
Provides common functionality to reduce duplication across frames.
"""
import customtkinter as ctk
from tkinter import messagebox
from utils.logger import setup_logging
from utils.ui_constants import (
    COLOR_HEADER_BG, COLOR_SEPARATOR, FONT_TITLE_LARGE, PADDING_LARGE, PADDING_NORMAL
)

logger = setup_logging(__name__)


class BaseFrame(ctk.CTkFrame):
    """Base class for all application frames with common functionality."""
    
    def __init__(self, master, title, icon="", *args, **kwargs):
        """
        Initialize base frame with common header and layout.
        
        Args:
            master: Parent widget
            title: Frame title (text only, without icon)
            icon: Icon emoji (optional)
            *args, **kwargs: Additional arguments for CTkFrame
        """
        super().__init__(master, *args, **kwargs)
        self.title = title
        self.icon = icon
        self.logger = logger
    
    def build_header(self, title=None, icon=None):
        """
        Build standard header with title and optional refresh button.
        
        Args:
            title: Header title (uses self.title if None)
            icon: Header icon (uses self.icon if None)
            
        Returns:
            Header frame widget
        """
        title = title or self.title
        icon = icon or self.icon
        
        header = ctk.CTkFrame(self, fg_color=COLOR_HEADER_BG)
        header.pack(fill='x', padx=0, pady=0)
        
        # Title with icon
        title_text = f"{icon} {title}" if icon else title
        ctk.CTkLabel(header, text=title_text, font=FONT_TITLE_LARGE).pack(
            side='left', padx=PADDING_LARGE, pady=15
        )
        
        return header
    
    def build_separator(self):
        """
        Build standard separator line.
        
        Returns:
            Separator frame widget
        """
        separator = ctk.CTkLabel(self, text="", fg_color=COLOR_SEPARATOR, height=1)
        separator.pack(fill='x', padx=0, pady=0)
        return separator
    
    def show_error(self, title, message, log=True):
        """
        Show error message dialog and optionally log it.
        
        Args:
            title: Dialog title
            message: Error message
            log: Whether to log the error (default True)
        """
        if log:
            self.logger.error(f"{title}: {message}")
        messagebox.showerror(title, message)
    
    def show_success(self, title, message, log=True):
        """
        Show success message dialog and optionally log it.
        
        Args:
            title: Dialog title
            message: Success message
            log: Whether to log the success (default True)
        """
        if log:
            self.logger.info(f"{title}: {message}")
        messagebox.showinfo(title, message)
    
    def show_warning(self, title, message, log=True):
        """
        Show warning message dialog and optionally log it.
        
        Args:
            title: Dialog title
            message: Warning message
            log: Whether to log the warning (default True)
        """
        if log:
            self.logger.warning(f"{title}: {message}")
        messagebox.showwarning(title, message)
    
    def show_info(self, title, message, log=True):
        """
        Show info message dialog and optionally log it.
        
        Args:
            title: Dialog title
            message: Info message
            log: Whether to log the info (default True)
        """
        if log:
            self.logger.info(f"{title}: {message}")
        messagebox.showinfo(title, message)
    
    def ask_confirmation(self, title, message):
        """
        Show yes/no confirmation dialog.
        
        Args:
            title: Dialog title
            message: Confirmation message
            
        Returns:
            True if user clicks Yes, False if No
        """
        return messagebox.askyesno(title, message)
    
    def safe_db_operation(self, operation, error_title="Database Error"):
        """
        Safely execute a database operation with error handling.
        
        Args:
            operation: Callable that performs the DB operation
            error_title: Title for error dialog if operation fails
            
        Returns:
            Result of operation if successful, None if failed
        """
        try:
            return operation()
        except ValueError as e:
            self.show_error("Validation Error", str(e))
            return None
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"{error_title}: {error_msg}")
            self.show_error(error_title, error_msg)
            return None
    
    def clear_widgets(self, container):
        """
        Clear all widgets from a container.
        
        Args:
            container: Container frame to clear
        """
        for widget in container.winfo_children():
            widget.destroy()
