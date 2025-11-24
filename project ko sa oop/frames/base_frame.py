import customtkinter as ctk
from tkinter import messagebox
from utils.logger import setup_logging
from utils.ui_constants import (
    COLOR_HEADER_BG, COLOR_SEPARATOR, FONT_TITLE_LARGE, PADDING_LARGE, PADDING_NORMAL
)

logger = setup_logging(__name__)


class BaseFrame(ctk.CTkFrame):
    
    def __init__(self, master, title, icon="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title = title
        self.icon = icon
        self.logger = logger
    
    def build_header(self, title=None, icon=None):
        title = title or self.title
        icon = icon or self.icon
        
        header = ctk.CTkFrame(self, fg_color=COLOR_HEADER_BG)
        header.pack(fill='x', padx=0, pady=0)
        
        title_text = f"{icon} {title}" if icon else title
        ctk.CTkLabel(header, text=title_text, font=FONT_TITLE_LARGE).pack(
            side='left', padx=PADDING_LARGE, pady=15
        )
        
        return header
    
    def build_separator(self):
        separator = ctk.CTkLabel(self, text="", fg_color=COLOR_SEPARATOR, height=1)
        separator.pack(fill='x', padx=0, pady=0)
        return separator
    
    def show_error(self, title, message, log=True):
        if log:
            self.logger.error(f"{title}: {message}")
        messagebox.showerror(title, message)
    
    def show_success(self, title, message, log=True):
        if log:
            self.logger.info(f"{title}: {message}")
        messagebox.showinfo(title, message)
    
    def show_warning(self, title, message, log=True):
        if log:
            self.logger.warning(f"{title}: {message}")
        messagebox.showwarning(title, message)
    
    def show_info(self, title, message, log=True):
        if log:
            self.logger.info(f"{title}: {message}")
        messagebox.showinfo(title, message)
    
    def ask_confirmation(self, title, message):
        return messagebox.askyesno(title, message)
    
    def safe_db_operation(self, operation, error_title="Database Error"):
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
        for widget in container.winfo_children():
            widget.destroy()
