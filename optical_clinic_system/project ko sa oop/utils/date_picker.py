"""Calendar date picker widget"""
import customtkinter as ctk
from datetime import datetime, timedelta

class DatePicker(ctk.CTkToplevel):
    """Calendar-based date picker dialog"""
    
    def __init__(self, parent, title="Select Date"):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x320")
        self.resizable(False, False)
        self.selected_date = None
        
    
        self.transient(parent)
        self.grab_set()
        
        self.current_date = datetime.now()
        self.build()
    
    def build(self):
        """Build calendar UI"""
        # Month/Year header
        header = ctk.CTkFrame(self, fg_color=("#3498db", "#1f6aa5"))
        header.pack(fill='x', padx=0, pady=0, ipady=10)
        
        # Navigation buttons and month/year display
        nav_frame = ctk.CTkFrame(header, fg_color="transparent")
        nav_frame.pack(fill='x', padx=10)
        
        ctk.CTkButton(nav_frame, text="◀", command=self.prev_month, width=40, height=30, font=('Segoe UI', 12, 'bold')).pack(side='left')
        
        self.month_label = ctk.CTkLabel(nav_frame, text="", font=('Segoe UI', 14, 'bold'), text_color='white')
        self.month_label.pack(side='left', expand=True)
        
        ctk.CTkButton(nav_frame, text="▶", command=self.next_month, width=40, height=30, font=('Segoe UI', 12, 'bold')).pack(side='right')
        
        # Days of week header
        days_frame = ctk.CTkFrame(self, fg_color=("transparent"))
        days_frame.pack(fill='x', padx=5, pady=5)
        
        for day in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']:
            ctk.CTkLabel(days_frame, text=day, font=('Segoe UI', 10, 'bold'), width=8).pack(side='left', fill='both', expand=True, padx=2)
        
        # Calendar grid
        self.calendar_frame = ctk.CTkFrame(self, fg_color=("transparent"))
        self.calendar_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color=("transparent"))
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Cancel", command=self.cancel, height=30, font=('Segoe UI', 11)).pack(side='left', fill='x', expand=True, padx=2)
        ctk.CTkButton(btn_frame, text="Today", command=self.select_today, height=30, font=('Segoe UI', 11)).pack(side='left', fill='x', expand=True, padx=2)
        ctk.CTkButton(btn_frame, text="OK", command=self.ok, height=30, font=('Segoe UI', 11), fg_color="#27ae60").pack(side='left', fill='x', expand=True, padx=2)
        
        self.update_calendar()
    
    def update_calendar(self):
        """Update calendar display for current month"""
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Update header
        month_name = self.current_date.strftime("%B %Y")
        self.month_label.configure(text=month_name)
        
        # Get first day and number of days in month
        first_day = datetime(self.current_date.year, self.current_date.month, 1)
        days_in_month = (first_day.replace(day=28) + timedelta(days=4)).day
        start_weekday = first_day.weekday()  # 0=Monday, 6=Sunday
        
        day_num = 1
        for week in range(6):
            for day_of_week in range(7):
                if (week == 0 and day_of_week < start_weekday) or day_num > days_in_month:
                    # Empty cell
                    ctk.CTkLabel(self.calendar_frame, text="", fg_color="transparent").grid(row=week, column=day_of_week, padx=2, pady=2, sticky='nsew')
                else:
                    btn = ctk.CTkButton(
                        self.calendar_frame, text=str(day_num),
                        command=lambda d=day_num: self.select_date(d),
                        height=30, font=('Segoe UI', 11),
                        fg_color=("#3498db" if day_num != datetime.now().day else "#27ae60", "#1f6aa5"),
                        hover_color=("#2980b9", "#164d7a")
                    )
                    btn.grid(row=week, column=day_of_week, padx=2, pady=2, sticky='nsew')
                    day_num += 1
    
    def prev_month(self):
        """Go to previous month"""
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.update_calendar()
    
    def next_month(self):
        """Go to next month"""
        self.current_date = self.current_date.replace(day=1) + timedelta(days=32)
        self.current_date = self.current_date.replace(day=1)
        self.update_calendar()
    
    def select_date(self, day: int):
        """Select a date"""
        self.selected_date = self.current_date.replace(day=day)
        self.ok()
    
    def select_today(self):
        """Select today"""
        self.selected_date = datetime.now()
        self.ok()
    
    def ok(self):
        """Confirm selection"""
        if not self.selected_date:
            self.selected_date = self.current_date
        self.destroy()
    
    def cancel(self):
        """Cancel selection"""
        self.selected_date = None
        self.destroy()
