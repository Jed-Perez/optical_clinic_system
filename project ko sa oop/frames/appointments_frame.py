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

        ctk.CTkLabel(frm, text='Select Patient', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.patient_combo = ctk.CTkComboBox(frm, values=self.get_patients_list(), state='readonly', height=35, font=('Segoe UI', 12))
        self.patient_combo.pack(fill='x', pady=(0, 10))

        ctk.CTkLabel(frm, text='Select Doctor', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.doctor_combo = ctk.CTkComboBox(frm, values=self.get_doctors_list(), state='readonly', height=35, font=('Segoe UI', 12))
        self.doctor_combo.pack(fill='x', pady=(0, 10))

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

        ctk.CTkLabel(frm, text='Cancel Appointment', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(15, 3))
        self.delete_combo = ctk.CTkComboBox(frm, values=[], state='readonly', height=35, font=('Segoe UI', 12))
        self.delete_combo.pack(fill='x', pady=(0, 10))
        ctk.CTkButton(frm, text='🗑️ Cancel Appointment', command=self.delete_appointment, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#e74c3c", "#c0392b")).pack(fill='x', pady=5)

        ctk.CTkLabel(frm, text='Mark Appointment as Done', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(15, 3))
        self.done_combo = ctk.CTkComboBox(frm, values=[], state='readonly', height=35, font=('Segoe UI', 12))
        self.done_combo.pack(fill='x', pady=(0, 10))
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

    def get_patients_list(self):
        try:
            patients = self.patient_manager.list_patients()
            if not patients:
                return ['No patients found']
            patient_list = []
            for p in patients:
                display = f"{p['Patient_ID']}: {p['Surname']}, {p['FirstName']}"
                patient_list.append(display)
            return patient_list
        except:
            return ['Error loading patients']

    def get_doctors_list(self):
        try:
            doctors = self.doctor_manager.list_doctors()
            if not doctors:
                return ['No doctors found']
            doctor_list = []
            for d in doctors:
                display = f"{d['Doctor_ID']}: {d['Name']}"
                doctor_list.append(display)
            return doctor_list
        except:
            return ['Error loading doctors']

    def get_appointments_list(self):
        try:
            appointments = self.manager.list_appointments()
            if not appointments:
                return ['No appointments found']
            appt_list = []
            for appt in appointments:
                appt_id = appt.get('Appointment_ID', '?')
                patient_id = appt.get('Patient_ID', '?')
                date = str(appt.get('Appointment_Date', ''))
                time = str(appt.get('Appointment_Time', ''))
                status = appt.get('Status', 'N/A')
                display = f"{appt_id}: Patient {patient_id} - {date} {time} ({status})"
                appt_list.append(display)
            return appt_list
        except:
            return ['Error loading appointments']

    def schedule_appointment(self):
        try:
            patient_selection = self.patient_combo.get().strip()
            doctor_selection = self.doctor_combo.get().strip()

            if not patient_selection or not doctor_selection or 'No patients' in patient_selection or 'No doctors' in doctor_selection:
                messagebox.showerror('Validation Error', 'Please select both a patient and a doctor.')
                return

            patient_id = patient_selection.split(':')[0].strip()
            doctor_id = doctor_selection.split(':')[0].strip()

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
            
            self.update_appointment_dropdowns()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load appointments: {str(e)}')
            self.txt.delete('1.0', 'end')
            self.txt.insert('end', f'Error: {str(e)}')

    def update_appointment_dropdowns(self):
        try:
            appt_list = self.get_appointments_list()
            if hasattr(self, 'delete_combo'):
                self.delete_combo.configure(values=appt_list)
                if appt_list and 'No appointments' not in appt_list[0]:
                    self.delete_combo.set(appt_list[0])
            if hasattr(self, 'done_combo'):
                self.done_combo.configure(values=appt_list)
                if appt_list and 'No appointments' not in appt_list[0]:
                    self.done_combo.set(appt_list[0])
        except:
            pass

    def delete_appointment(self):
        try:
            appointment_selection = self.delete_combo.get().strip()
            if not appointment_selection or 'No appointments' in appointment_selection:
                messagebox.showerror('Validation Error', 'Please select an appointment to cancel.')
                return

            appointment_id = appointment_selection.split(':')[0].strip()

            if not messagebox.askyesno('Confirm Cancellation', f'Are you sure you want to cancel appointment ID {appointment_id}? This will archive it.'):
                return

            success = self.manager.archive(appointment_id)
            if success:
                messagebox.showinfo('Success', f'Appointment {appointment_id} has been cancelled and archived.')
                self.view_appointments()
            else:
                messagebox.showerror('Error', f'Could not cancel appointment {appointment_id}. It may not exist.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def mark_as_done(self):
        try:
            appointment_selection = self.done_combo.get().strip()
            if not appointment_selection or 'No appointments' in appointment_selection:
                messagebox.showerror('Validation Error', 'Please select an appointment to mark as done.')
                return

            appointment_id = appointment_selection.split(':')[0].strip()

            if not messagebox.askyesno('Confirm Done', f'Are you sure you want to mark appointment ID {appointment_id} as done? This will archive it.'):
                return

            success = self.manager.mark_as_done(appointment_id)
            if success:
                messagebox.showinfo('Success', f'Appointment {appointment_id} has been marked as done and archived.')
                self.view_appointments()
            else:
                messagebox.showerror('Error', f'Could not mark appointment {appointment_id} as done. It may not exist.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def pack(self, *args, **kwargs):
        """Override pack to refresh data when the frame is shown."""
        self.view_appointments()
        super().pack(*args, **kwargs)