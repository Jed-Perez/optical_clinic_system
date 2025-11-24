import customtkinter as ctk
from tkinter import messagebox

class AlertSystem:
    # Color schemes
    COLORS = {
        'success': {'bg': '#27ae60', 'fg': 'white', 'icon': '✅'},
        'warning': {'bg': '#f39c12', 'fg': 'white', 'icon': '⚠️'},
        'error': {'bg': '#e74c3c', 'fg': 'white', 'icon': '❌'},
        'info': {'bg': '#3498db', 'fg': 'white', 'icon': 'ℹ️'}
    }
    
    @staticmethod
    def success(title: str, message: str):
        AlertSystem._show_alert(title, message, 'success')
    
    @staticmethod
    def warning(title: str, message: str):
        AlertSystem._show_alert(title, message, 'warning')
    
    @staticmethod
    def error(title: str, message: str):
        AlertSystem._show_alert(title, message, 'error')
    
    @staticmethod
    def info(title: str, message: str):
        AlertSystem._show_alert(title, message, 'info')
    
    @staticmethod
    def _show_alert(title: str, message: str, alert_type: str):
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
        return messagebox.askyesno(f"❓ {title}", message)
