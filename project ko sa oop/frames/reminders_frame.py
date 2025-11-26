import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta

class RemindersFrame(ctk.CTkFrame):
    def __init__(self, master, managers, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.managers = managers
        self.reminder_manager = managers['rem_m']
        self.patient_manager = managers['pm']
        self.appointment_manager = managers['am']
        self.appointments_map = {}
        self.build()

    def build(self):
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='🔔 Reminder Management', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)

        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)

        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=15, pady=15)

        left = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"), width=400)
        left.pack(side='left', fill='both', expand=False, padx=(0, 7.5), pady=0)
        left.pack_propagate(False)

        form_title = ctk.CTkLabel(left, text='Create New Reminder', font=('Segoe UI', 16, 'bold'))
        form_title.pack(pady=15, padx=20)

        frm = ctk.CTkFrame(left, fg_color=("transparent"))
        frm.pack(padx=20, pady=10, fill='x')

        ctk.CTkLabel(frm, text='Select Appointment *', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.appointment_combo = ctk.CTkComboBox(frm, values=self.get_appointments_list(), state='readonly', height=40, font=('Segoe UI', 12), command=self.on_appointment_selected)
        self.appointment_combo.set('Select Appointment')
        self.appointment_combo.pack(fill='x', pady=(0, 10))

        ctk.CTkLabel(frm, text='Patient Info', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.patient_info_label = ctk.CTkLabel(frm, text='Select an appointment first', font=('Segoe UI', 11), justify='left', fg_color=("#e0e0e0", "#2a2a2a"), corner_radius=5)
        self.patient_info_label.pack(fill='x', pady=(0, 10), padx=5, ipady=8)

        ctk.CTkLabel(frm, text='Days Before Appointment', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.days_before = ctk.CTkComboBox(frm, values=['1', '2', '3', '7'], state='readonly', height=40, font=('Segoe UI', 12))
        self.days_before.set('1')
        self.days_before.pack(fill='x', pady=(0, 20))

        ctk.CTkButton(frm, text='➕ Create Reminder', command=self.create_reminder, height=45, font=('Segoe UI', 13, 'bold')).pack(fill='x', pady=5)
        ctk.CTkButton(frm, text='🔄 Refresh List', command=self.refresh_data, height=45, font=('Segoe UI', 13, 'bold')).pack(fill='x', pady=5)

        right = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        right.pack(side='right', fill='both', expand=True, padx=(7.5, 0), pady=0)

        ctk.CTkLabel(right, text='Pending Reminders', font=('Segoe UI', 16, 'bold')).pack(pady=15)

        self.txt = ctk.CTkTextbox(right, font=('Consolas', 11), fg_color=("#f5f5f5", "#1a1a1a"))
        self.txt.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        self.view_reminders()

    def get_appointments_list(self):
        """Get list of upcoming appointments"""
        try:
            appointments = self.appointment_manager.list_appointments()
            self.appointments_map.clear()
            
            appointment_list = []
            for appt in appointments:
                if appt.get('Status') == 'Scheduled':
                    # Format: "ID: Patient Name - Doctor Name (Date Time)"
                    patient_id = appt.get('Patient_ID')
                    patient = self.patient_manager.get_patient(patient_id)
                    patient_name = f"{patient.get('Surname', '')}, {patient.get('FirstName', '')}" if patient else f"Patient {patient_id}"
                    
                    doctor_id = appt.get('Doctor_ID')
                    # Get doctor name from managers
                    doctors = self.managers['dm'].list_doctors()
                    doctor_name = next((d['Name'] for d in doctors if d['Doctor_ID'] == doctor_id), f"Doctor {doctor_id}")
                    
                    date_str = str(appt.get('Appointment_Date', ''))
                    time_str = str(appt.get('Appointment_Time', ''))
                    
                    display = f"{appt['Appointment_ID']}: {patient_name} - {doctor_name} ({date_str} {time_str})"
                    appointment_list.append(display)
                    self.appointments_map[display] = appt
            
            return appointment_list if appointment_list else ['No scheduled appointments']
        except Exception as e:
            print(f"Error loading appointments: {e}")
            return ['Error loading appointments']
    
    def on_appointment_selected(self, choice=None):
        """When an appointment is selected, show patient info"""
        try:
            selected = self.appointment_combo.get()
            if selected in self.appointments_map:
                appt = self.appointments_map[selected]
                patient_id = appt.get('Patient_ID')
                patient = self.patient_manager.get_patient(patient_id)
                
                if patient:
                    info = f"ID: {patient['Patient_ID']}\n"
                    info += f"Name: {patient.get('Surname', '')}, {patient.get('FirstName', '')}\n"
                    info += f"Contact: {patient.get('Contact', 'N/A')}"
                    self.patient_info_label.configure(text=info)
        except Exception as e:
            self.patient_info_label.configure(text=f"Error: {str(e)}")

    def create_reminder(self):
        try:
            selected = self.appointment_combo.get()
            
            if selected not in self.appointments_map:
                messagebox.showerror('Validation Error', 'Please select an appointment.')
                return
            
            appt = self.appointments_map[selected]
            appt_id = appt['Appointment_ID']
            patient_id = appt['Patient_ID']
            days_before_str = self.days_before.get().strip()

            if not days_before_str:
                messagebox.showerror('Validation Error', 'Please select days before appointment.')
                return

            days_before = int(days_before_str)
            reminder_date = datetime.now().date() + timedelta(days=1-days_before)

            self.reminder_manager.create_reminder(appt_id, patient_id, reminder_date.strftime('%Y-%m-%d'), '09:00')
            messagebox.showinfo('Success', 'Reminder created successfully.')
            self.appointment_combo.set('Select Appointment')
            self.patient_info_label.configure(text='Select an appointment first')
            self.view_reminders()
        except ValueError:
            messagebox.showerror('Validation Error', '"Days Before" must be a number.')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def refresh_data(self):
        """Refresh appointments list and reminders"""
        self.appointment_combo.configure(values=self.get_appointments_list())
        self.appointment_combo.set('Select Appointment')
        self.patient_info_label.configure(text='Select an appointment first')
        self.view_reminders()

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