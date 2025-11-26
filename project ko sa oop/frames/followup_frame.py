import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import customtkinter as ctk
from datetime import datetime, timedelta
from utils.logger import setup_logging
from utils.constants import *
from utils.ui_constants import *

logger = setup_logging(__name__)

class FollowUpFrame(ctk.CTkFrame):
    def __init__(self, parent, managers):
        super().__init__(parent, fg_color="transparent")
        self.pm = managers.get('pm')
        self.dm = managers.get('dm')
        self.am = managers.get('am')
        self.doctors_list = []
        self.patients_dict = {}
        
        self.build()
    
    def build(self):
        title = ctk.CTkLabel(self, text='Schedule Follow-up Appointments', font=FONT_TITLE_LARGE)
        title.pack(pady=PADDING_NORMAL, padx=PADDING_LARGE)
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_NORMAL)
        
        # Left panel - Form
        left = ctk.CTkFrame(main_frame, fg_color=COLOR_PANEL_BG, width=450)
        left.pack(side='left', fill='both', expand=False, padx=(0, PADDING_NORMAL))
        left.pack_propagate(False)
        
        ctk.CTkLabel(left, text='New Follow-up', font=FONT_TITLE_MEDIUM).pack(pady=PADDING_NORMAL, padx=PADDING_LARGE)
        
        scroll_frame = ctk.CTkScrollableFrame(left, fg_color="transparent")
        scroll_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        frm = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        frm.pack(padx=PADDING_LARGE, pady=PADDING_SMALL, fill='x')
        
        # Patient selection
        ctk.CTkLabel(frm, text='Select Patient *', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.patient_list = self.get_patients_list()
        self.patient_combo = ctk.CTkComboBox(frm, values=self.patient_list, state='readonly', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL, command=self.on_patient_selected)
        self.patient_combo.pack(fill='x', pady=(0, 10))
        
        # Patient info
        self.patient_info = ctk.CTkLabel(frm, text='', font=FONT_LABEL_SMALL, justify='left')
        self.patient_info.pack(anchor='w', padx=PADDING_LARGE, pady=PADDING_SMALL)
        
        ctk.CTkLabel(frm, text="", fg_color=COLOR_SEPARATOR, height=1).pack(fill='x', padx=0, pady=PADDING_SMALL)
        
        # Follow-up Type
        ctk.CTkLabel(frm, text='Follow-up Type *', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_NORMAL, 3))
        self.followup_type = ctk.CTkComboBox(frm, values=['Glasses Fitting', 'Eye Check', 'Contact Lens Trial', 'Routine Check', 'Prescription Review'], state='readonly', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.followup_type.pack(fill='x', pady=(0, 10))
        
        # Days from now
        ctk.CTkLabel(frm, text='Schedule Date *', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.followup_days = ctk.CTkComboBox(frm, values=['7 days', '14 days', '30 days', '60 days', '90 days'], state='readonly', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.followup_days.pack(fill='x', pady=(0, 10))
        
        # Doctor selection
        ctk.CTkLabel(frm, text='Preferred Doctor *', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.doctors_list = self.get_doctors_list()
        self.doctor_combo = ctk.CTkComboBox(frm, values=self.doctors_list, state='readonly', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.doctor_combo.pack(fill='x', pady=(0, 10))
        
        # Notes
        ctk.CTkLabel(frm, text='Notes', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.notes = ctk.CTkTextbox(frm, font=FONT_MONO_SMALL, fg_color=COLOR_TEXT_BG, height=80)
        self.notes.pack(fill='x', pady=(0, 20))
        
        # Schedule button
        ctk.CTkButton(frm, text=f'{ICON_ADD} Schedule Follow-up', command=self.schedule_followup, height=BUTTON_HEIGHT, font=FONT_BUTTON, fg_color=BTN_SUCCESS).pack(fill='x', pady=PADDING_SMALL)
        
        # Right panel - Scheduled Follow-ups List
        right = ctk.CTkFrame(main_frame, fg_color=COLOR_PANEL_BG)
        right.pack(side='right', fill='both', expand=True)
        
        ctk.CTkLabel(right, text='Scheduled Follow-ups', font=FONT_TITLE_MEDIUM).pack(anchor='w', padx=PADDING_LARGE, pady=PADDING_NORMAL)
        
        self.list_textbox = ctk.CTkTextbox(right, font=FONT_MONO_SMALL, fg_color=COLOR_TEXT_BG)
        self.list_textbox.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_SMALL)
        
        # Refresh button
        ctk.CTkButton(right, text='Refresh List', command=self.load_followups, height=BUTTON_HEIGHT, font=FONT_BUTTON, fg_color=BTN_INFO).pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_NORMAL))
        
        self.load_followups()
    
    def get_patients_list(self):
        try:
            patients = self.pm.list_patients()
            if not patients:
                return ['No patients found']
            
            patient_list = []
            self.patients_dict = {}
            for p in patients:
                display_name = f"{p['Patient_ID']}: {p['Surname']}, {p['FirstName']} ({p['Age']})"
                patient_list.append(display_name)
                self.patients_dict[display_name] = p
            
            return patient_list
        except Exception as e:
            logger.error(f"Error getting patients list: {e}")
            return ['Error loading patients']
    
    def get_doctors_list(self):
        try:
            doctors = self.dm.list_doctors()
            return [d['Name'] for d in doctors] if doctors else ['No doctors available']
        except:
            return ['No doctors available']
    
    def on_patient_selected(self, event=None):
        try:
            selected = self.patient_combo.get()
            if selected and selected in self.patients_dict:
                patient = self.patients_dict[selected]
                patient_info = f"Patient: {patient['Surname']}, {patient['FirstName']}\nID: {patient['Patient_ID']}\nAge: {patient['Age']} | {patient['Gender']}\nContact: {patient['Contact']}"
                self.patient_info.configure(text=patient_info)
        except Exception as e:
            logger.error(f"Error selecting patient: {e}")
    
    def schedule_followup(self):
        try:
            patient_sel = self.patient_combo.get()
            followup_type = self.followup_type.get()
            days_str = self.followup_days.get()
            doctor_name = self.doctor_combo.get()
            notes = self.notes.get('1.0', 'end-1c').strip()
            
            if not all([patient_sel, followup_type, days_str, doctor_name]):
                self.show_error('Validation Error', 'Please fill all required fields')
                return
            
            if patient_sel not in self.patients_dict:
                self.show_error('Error', 'Please select a valid patient')
                return
            
            patient = self.patients_dict[patient_sel]
            
            doctors = self.dm.list_doctors()
            doctor_id = None
            for doc in doctors:
                if doc['Name'] == doctor_name:
                    doctor_id = doc['Doctor_ID']
                    break
            
            if not doctor_id:
                self.show_error('Error', 'Invalid doctor selection')
                return

            days = int(days_str.split()[0])
            appointment_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            appointment_time = '10:00'  
            
            self.am.schedule(
                patient_id=patient['Patient_ID'],
                doctor_id=doctor_id,
                date=appointment_date,
                time=appointment_time
            )
         
            self.show_success('Success', f'Follow-up scheduled!\n\nPatient: {patient["Surname"]}, {patient["FirstName"]}\nType: {followup_type}\nDate: {appointment_date}\nDoctor: {doctor_name}')
        
            self.patient_combo.set('')
            self.followup_type.set('')
            self.followup_days.set('')
            self.doctor_combo.set('')
            self.notes.delete('1.0', 'end')
            self.patient_info.configure(text='')
            
            # Reload list
            self.load_followups()
            
        except Exception as e:
            logger.error(f"Error scheduling follow-up: {e}")
            self.show_error('Error', f'Failed to schedule: {str(e)}')
    
    def load_followups(self):
        self.list_textbox.delete('1.0', 'end')
        try:
            appointments = self.am.list_appointments()
            if not appointments:
                self.list_textbox.insert('end', 'No scheduled follow-ups.')
                return
            self.list_textbox.insert('end', 'UPCOMING FOLLOW-UPS:\n' + '='*50 + '\n')
            count = 0
            for appt in appointments:
                try:
                    # Use correct field names from appointments table
                    patient = self.pm.get_patient(appt.get('Patient_ID'))
                    doctor = None
                    for d in self.dm.list_doctors():
                        if d['Doctor_ID'] == appt.get('Doctor_ID'):
                            doctor = d
                            break
                    if patient and doctor and appt.get('Status') == 'Scheduled':
                        name = f"{patient['Surname']}, {patient['FirstName']}"
                        date = appt.get('Appointment_Date', 'N/A')
                        time = appt.get('Appointment_Time', '10:00')
                        status = appt.get('Status', 'Pending')
                        self.list_textbox.insert('end', f"\nPatient: {name}\nDoctor: {doctor['Name']}\nDate: {date} {time}\nStatus: {status}\n{'-'*50}\n")
                        count += 1
                except Exception as e:
                    logger.error(f"Error displaying appointment: {e}")
                    continue
            if count == 0:
                self.list_textbox.insert('end', 'No upcoming follow-ups found.')
        except Exception as e:
            logger.error(f"Error loading follow-ups: {e}")
            self.list_textbox.insert('end', f'Error loading appointments: {str(e)}')
    
    def show_error(self, title, message):
        from tkinter import messagebox
        messagebox.showerror(title, message)
    
    def show_success(self, title, message):
        from tkinter import messagebox
        messagebox.showinfo(title, message)
