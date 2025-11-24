import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

class RemindersFrame(ctk.CTkFrame):
    def __init__(self, master, managers, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.managers = managers
        self.reminder_manager = managers['rem_m']
        self.patient_manager = managers['pm']
        self.build()

    def build(self):
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='🔔 Reminder Management', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)

        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)

        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=15, pady=15)

        left = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"), width=350)
        left.pack(side='left', fill='both', expand=False, padx=(0, 7.5), pady=0)
        left.pack_propagate(False)

        form_title = ctk.CTkLabel(left, text='Create New Reminder', font=('Segoe UI', 16, 'bold'))
        form_title.pack(pady=15, padx=20)

        frm = ctk.CTkFrame(left, fg_color=("transparent"))
        frm.pack(padx=20, pady=10, fill='x')

        ctk.CTkLabel(frm, text='Appointment ID', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.appointment_id = ctk.CTkEntry(frm, placeholder_text='Enter Appointment ID', height=35, font=('Segoe UI', 12))
        self.appointment_id.pack(fill='x', pady=(0, 10))

        ctk.CTkLabel(frm, text='Patient ID', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.patient_id = ctk.CTkEntry(frm, placeholder_text='Enter Patient ID', height=35, font=('Segoe UI', 12))
        self.patient_id.pack(fill='x', pady=(0, 10))

        ctk.CTkLabel(frm, text='Days Before Appointment', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.days_before = ctk.CTkEntry(frm, placeholder_text='e.g., 1 for one day before', height=35, font=('Segoe UI', 12))
        self.days_before.insert(0, "1")
        self.days_before.pack(fill='x', pady=(0, 20))

        ctk.CTkButton(frm, text='➕ Create Reminder', command=self.create_reminder, height=40, font=('Segoe UI', 12, 'bold')).pack(fill='x', pady=5)
        ctk.CTkButton(frm, text='🔄 Refresh List', command=self.view_reminders, height=40, font=('Segoe UI', 12, 'bold')).pack(fill='x', pady=5)

        right = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        right.pack(side='right', fill='both', expand=True, padx=(7.5, 0), pady=0)

        ctk.CTkLabel(right, text='Pending Reminders', font=('Segoe UI', 16, 'bold')).pack(pady=15)

        self.txt = ctk.CTkTextbox(right, font=('Consolas', 11), fg_color=("#f5f5f5", "#1a1a1a"))
        self.txt.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        self.view_reminders()

    def create_reminder(self):
        try:
            appt_id = self.appointment_id.get().strip()
            patient_id = self.patient_id.get().strip()
            days_before_str = self.days_before.get().strip()

            if not appt_id or not patient_id or not days_before_str:
                messagebox.showerror('Validation Error', 'All fields are required.')
                return

            days_before = int(days_before_str)
            reminder_date = datetime.now().date() + timedelta(days=1-days_before)

            self.reminder_manager.create_reminder(appt_id, patient_id, reminder_date.strftime('%Y-%m-%d'), '09:00')
            messagebox.showinfo('Success', 'Reminder created successfully.')
            self.appointment_id.delete(0, 'end')
            self.patient_id.delete(0, 'end')
            self.view_reminders()
        except ValueError:
            messagebox.showerror('Validation Error', '"Days Before" must be a number.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def view_reminders(self):
        try:
            reminders = self.reminder_manager.get_pending_reminders()
            self.txt.delete('1.0', 'end')
            if not reminders:
                self.txt.insert('end', 'No pending reminders.')
                return

            header = f"{'ID':<5} {'Patient':<25} {'Contact':<15} {'Reminder Date':<15} {'Status':<10}\n"
            self.txt.insert('end', header)
            self.txt.insert('end', "="*70 + "\n")

            for r in reminders:
                self.txt.insert('end', f"{r['Reminder_ID']:<5} {r['Name']:<25} {r['Contact']:<15} {str(r['Reminder_Date']):<15} {r['Status']:<10}\n")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load reminders: {str(e)}')

    def pack(self, *args, **kwargs):
        self.view_reminders()
        super().pack(*args, **kwargs)