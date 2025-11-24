import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import calendar

class AppointmentsFrame(ctk.CTkFrame):
    def __init__(self, master, manager, patient_manager, doctor_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.manager = manager
        self.patient_manager = patient_manager
        self.doctor_manager = doctor_manager
        self.build()

    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='📅 Appointment Management', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)

        # Separator
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)

        # Main container
        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=15, pady=15)

        # Left panel - Input form
        left = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"), width=350)
        left.pack(side='left', fill='both', expand=False, padx=0, pady=0)
        left.pack_propagate(False)

        form_title = ctk.CTkLabel(left, text='Schedule New Appointment', font=('Segoe UI', 16, 'bold'))
        form_title.pack(pady=15, padx=20)

        scroll_frame = ctk.CTkScrollableFrame(left, fg_color="transparent")
        scroll_frame.pack(fill='both', expand=True, padx=0, pady=0)

        frm = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        frm.pack(padx=20, pady=10, fill='x')

        # Form fields
        ctk.CTkLabel(frm, text='Patient ID', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.patient_id = ctk.CTkEntry(frm, placeholder_text='Enter Patient ID', height=35, font=('Segoe UI', 12))
        self.patient_id.pack(fill='x', pady=(0, 10))

        ctk.CTkLabel(frm, text='Doctor ID', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.doctor_id = ctk.CTkEntry(frm, placeholder_text='Enter Doctor ID', height=35, font=('Segoe UI', 12))
        self.doctor_id.pack(fill='x', pady=(0, 10))

        # Date Picker
        ctk.CTkLabel(frm, text='Appointment Date', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        date_frame = ctk.CTkFrame(frm, fg_color="transparent")
        date_frame.pack(fill='x', pady=(0, 10))
        
        current_year = datetime.now().year
        self.year_var = ctk.StringVar(value=str(current_year))
        self.month_var = ctk.StringVar(value=datetime.now().strftime('%B'))
        self.day_var = ctk.StringVar(value=str(datetime.now().day))

        self.year_combo = ctk.CTkComboBox(date_frame, values=[str(y) for y in range(current_year, current_year + 5)], variable=self.year_var, command=self.update_days, width=80)
        self.year_combo.pack(side='left', padx=(0, 5), fill='x', expand=True)

        self.month_combo = ctk.CTkComboBox(date_frame, values=[calendar.month_name[i] for i in range(1, 13)], variable=self.month_var, command=self.update_days, width=120)
        self.month_combo.pack(side='left', padx=5, fill='x', expand=True)

        self.day_combo = ctk.CTkComboBox(date_frame, values=[], variable=self.day_var, width=70)
        self.day_combo.pack(side='left', padx=(5, 0), fill='x', expand=True)
        self.update_days()

        # Time Picker
        ctk.CTkLabel(frm, text='Appointment Time', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        time_frame = ctk.CTkFrame(frm, fg_color="transparent")
        time_frame.pack(fill='x', pady=(0, 20))

        self.hour_var = ctk.StringVar(value='09')
        self.minute_var = ctk.StringVar(value='00')

        self.hour_combo = ctk.CTkComboBox(time_frame, values=[f"{h:02d}" for h in range(8, 18)], variable=self.hour_var, width=80)
        self.hour_combo.pack(side='left', padx=(0, 5), fill='x', expand=True)

        ctk.CTkLabel(time_frame, text=":", font=('Segoe UI', 14, 'bold')).pack(side='left')

        self.minute_combo = ctk.CTkComboBox(time_frame, values=['00', '15', '30', '45'], variable=self.minute_var, width=80)
        self.minute_combo.pack(side='left', padx=5, fill='x', expand=True)

        # Buttons
        btn_frm = ctk.CTkFrame(frm, fg_color="transparent")
        btn_frm.pack(fill='x', pady=10)
        ctk.CTkButton(btn_frm, text='➕ Schedule Appointment', command=self.schedule_appointment, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#27ae60", "#1e8449")).pack(fill='x', pady=5)
        ctk.CTkButton(btn_frm, text='🔄 Refresh List', command=self.view_appointments, height=40, font=('Segoe UI', 12, 'bold')).pack(fill='x', pady=5)

        # Delete section
        ctk.CTkLabel(frm, text='Cancel Appointment by ID', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(15, 3))
        self.delete_id = ctk.CTkEntry(frm, placeholder_text='Enter Appointment ID to cancel', height=35, font=('Segoe UI', 12))
        self.delete_id.pack(fill='x', pady=(0, 10))
        ctk.CTkButton(frm, text='🗑️ Cancel Appointment', command=self.delete_appointment, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#e74c3c", "#c0392b")).pack(fill='x', pady=5)

        # Mark as Done section
        ctk.CTkLabel(frm, text='Mark Appointment as Done', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(15, 3))
        self.done_id = ctk.CTkEntry(frm, placeholder_text='Enter Appointment ID to mark as done', height=35, font=('Segoe UI', 12))
        self.done_id.pack(fill='x', pady=(0, 10))
        ctk.CTkButton(frm, text='✔️ Mark as Done', command=self.mark_as_done, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#2ecc71", "#27ae60")).pack(fill='x', pady=5)

        # Right panel - Display area
        right = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        right.pack(side='right', fill='both', expand=True, padx=15, pady=15)

        ctk.CTkLabel(right, text='Scheduled Appointments', font=('Segoe UI', 16, 'bold')).pack(pady=(0, 10))

        self.txt = ctk.CTkTextbox(right, font=('Consolas', 11), fg_color=("#f5f5f5", "#1a1a1a"))
        self.txt.pack(fill='both', expand=True, padx=0, pady=0)

        self.view_appointments()

    def update_days(self, *args):
        """Updates the days in the day dropdown based on the selected month and year."""
        try:
            year = int(self.year_var.get())
            month_name = self.month_var.get()
            month_num = list(calendar.month_name).index(month_name)
            
            _, num_days = calendar.monthrange(year, month_num)
            
            days = [str(i) for i in range(1, num_days + 1)]
            self.day_combo.configure(values=days)
            
            if self.day_var.get() not in days:
                self.day_var.set('1')
        except (ValueError, IndexError) as e:
            print(f"Error updating days: {e}")
            self.day_combo.configure(values=[str(i) for i in range(1, 32)])

    def schedule_appointment(self):
        try:
            patient_id = self.patient_id.get().strip()
            doctor_id = self.doctor_id.get().strip()

            if not patient_id or not doctor_id:
                messagebox.showerror('Validation Error', 'Patient ID and Doctor ID are required.')
                return

            year = self.year_var.get()
            month_name = self.month_var.get()
            month_num = list(calendar.month_name).index(month_name)
            day = self.day_var.get()
            date_str = f"{year}-{month_num:02d}-{day:02s}"

            hour = self.hour_var.get()
            minute = self.minute_var.get()
            time_str = f"{hour}:{minute}"

            self.manager.schedule(patient_id, doctor_id, date_str, time_str)
            messagebox.showinfo('Success', 'Appointment scheduled successfully')
            self.patient_id.delete(0, 'end')
            self.doctor_id.delete(0, 'end')
            self.view_appointments()
        except ValueError as ve:
            messagebox.showerror('Scheduling Conflict', str(ve))
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def view_appointments(self):
        try:
            appointments = self.manager.list_appointments()
            self.txt.delete('1.0', 'end')
            if not appointments:
                self.txt.insert('end', 'No appointments scheduled.')
                return

            header = f"{'ID':<5} {'Patient ID':<12} {'Doctor ID':<12} {'Date':<15} {'Time':<10} {'Status':<15}\n"
            self.txt.insert('end', header)
            self.txt.insert('end', "="*70 + "\n")

            for appt in appointments:
                appt_id = appt.get('Appointment_ID', '?')
                patient_id = appt.get('Patient_ID', '?')
                doctor_id = appt.get('Doctor_ID', '?')
                date = str(appt.get('Appointment_Date', ''))
                time = str(appt.get('Appointment_Time', ''))
                status = appt.get('Status', 'N/A')
                
                self.txt.insert('end', f"{appt_id:<5} {patient_id:<12} {doctor_id:<12} {date:<15} {time:<10} {status:<15}\n")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load appointments: {str(e)}')
            self.txt.delete('1.0', 'end')
            self.txt.insert('end', f'Error: {str(e)}')

    def delete_appointment(self):
        try:
            appointment_id = self.delete_id.get().strip()
            if not appointment_id:
                messagebox.showerror('Validation Error', 'Appointment ID is required to cancel.')
                return

            if not messagebox.askyesno('Confirm Cancellation', f'Are you sure you want to cancel appointment ID {appointment_id}? This will archive it.'):
                return

            success = self.manager.archive(appointment_id)
            if success:
                messagebox.showinfo('Success', f'Appointment {appointment_id} has been cancelled and archived.')
                self.delete_id.delete(0, 'end')
                self.view_appointments()
            else:
                messagebox.showerror('Error', f'Could not cancel appointment {appointment_id}. It may not exist.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def mark_as_done(self):
        try:
            appointment_id = self.done_id.get().strip()
            if not appointment_id:
                messagebox.showerror('Validation Error', 'Appointment ID is required to mark as done.')
                return

            if not messagebox.askyesno('Confirm Done', f'Are you sure you want to mark appointment ID {appointment_id} as done? This will archive it.'):
                return

            success = self.manager.mark_as_done(appointment_id)
            if success:
                messagebox.showinfo('Success', f'Appointment {appointment_id} has been marked as done and archived.')
                self.done_id.delete(0, 'end')
                self.view_appointments()
            else:
                messagebox.showerror('Error', f'Could not mark appointment {appointment_id} as done. It may not exist.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def pack(self, *args, **kwargs):
        """Override pack to refresh data when the frame is shown."""
        self.view_appointments()
        super().pack(*args, **kwargs)