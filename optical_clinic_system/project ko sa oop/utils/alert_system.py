"""Color-coded alert system for user feedback"""
import customtkinter as ctk
from tkinter import messagebox

class AlertSystem:
    """Provides color-coded alerts (success, warning, error)"""
    
    # Color schemes
    COLORS = {
        'success': {'bg': '#27ae60', 'fg': 'white', 'icon': '✅'},
        'warning': {'bg': '#f39c12', 'fg': 'white', 'icon': '⚠️'},
        'error': {'bg': '#e74c3c', 'fg': 'white', 'icon': '❌'},
        'info': {'bg': '#3498db', 'fg': 'white', 'icon': 'ℹ️'}
    }
    
    @staticmethod
    def success(title: str, message: str):
        """Show green success alert"""
        AlertSystem._show_alert(title, message, 'success')
    
    @staticmethod
    def warning(title: str, message: str):
        """Show yellow warning alert"""
        AlertSystem._show_alert(title, message, 'warning')
    
    @staticmethod
    def error(title: str, message: str):
        """Show red error alert"""
        AlertSystem._show_alert(title, message, 'error')
    
    @staticmethod
    def info(title: str, message: str):
        """Show blue info alert"""
        AlertSystem._show_alert(title, message, 'info')
    
    @staticmethod
    def _show_alert(title: str, message: str, alert_type: str):
        """Internal method to show colored alert"""
        colors = AlertSystem.COLORS.get(alert_type, AlertSystem.COLORS['info'])
        
        if alert_type == 'success':
            messagebox.showinfo(f"{colors['icon']} {title}", message)
        elif alert_type == 'warning':
            messagebox.showwarning(f"{colors['icon']} {title}", message)
        elif alert_type == 'error':
            messagebox.showerror(f"{colors['icon']} {title}", message)
        else:
            messagebox.showinfo(f"{colors['icon']} {title}", message)
    
    @staticmethod
    def confirm(title: str, message: str) -> bool:
        """Show confirmation dialog"""
        return messagebox.askyesno(f"❓ {title}", message)
