import customtkinter as ctk
from tkinter import messagebox
from utils.ui_constants import *

class MedicalRecordsFrame(ctk.CTkFrame):
    def __init__(self, master, managers, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.managers = managers
        self.record_manager = managers['mr_m']
        self.patient_manager = managers['pm']
        self.doctor_manager = managers['dm']
        self.build()

    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='📋 Medical Records', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)

        # Separator
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)

        # Main container
        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=15, pady=15)

        # Left panel - Patient selection
        left = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"), width=350)
        left.pack(side='left', fill='both', expand=False, padx=(0, 7.5), pady=0)
        left.pack_propagate(False)

        form_title = ctk.CTkLabel(left, text='Add New Record', font=('Segoe UI', 16, 'bold'))
        form_title.pack(pady=15, padx=20)

        # Scrollable frame for form
        scroll_frm = ctk.CTkScrollableFrame(left, fg_color=("transparent"))
        scroll_frm.pack(fill='both', expand=True, padx=20, pady=10)

        frm = ctk.CTkFrame(scroll_frm, fg_color=("transparent"))
        frm.pack(fill='x')

        # Form fields - Patient Selection
        ctk.CTkLabel(frm, text='Select Patient *', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(10, 3))
        self.patient_combo = ctk.CTkComboBox(frm, values=['Select a patient...'], state='readonly', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.patient_combo.set('Select a patient...')
        self.patient_combo.pack(fill='x', pady=(0, 10))

        # Doctor Selection
        ctk.CTkLabel(frm, text='Select Doctor *', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(10, 3))
        self.doctor_combo = ctk.CTkComboBox(frm, values=['Select a doctor...'], state='readonly', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.doctor_combo.set('Select a doctor...')
        self.doctor_combo.pack(fill='x', pady=(0, 10))

        ctk.CTkLabel(frm, text='Diagnosis *', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(10, 3))
        self.diagnosis = ctk.CTkEntry(frm, placeholder_text='e.g., Myopia', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.diagnosis.pack(fill='x', pady=(0, 10))

        ctk.CTkLabel(frm, text='Clinical Notes', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(10, 3))
        self.notes = ctk.CTkTextbox(frm, height=100, font=FONT_LABEL_NORMAL)
        self.notes.pack(fill='x', pady=(0, 20))

        # Buttons
        ctk.CTkButton(frm, text='➕ Add Record', command=self.add_record, height=BUTTON_HEIGHT, font=FONT_BUTTON, fg_color=BTN_SUCCESS).pack(fill='x', pady=5)
        ctk.CTkButton(frm, text='🔄 Refresh List', command=self.view_records, height=BUTTON_HEIGHT, font=FONT_BUTTON).pack(fill='x', pady=5)
        
        # Store patient data
        self.patients_dict = {}
        self.load_patients()
        self.load_doctors()

        # Right panel - Display area
        right = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        right.pack(side='right', fill='both', expand=True, padx=(7.5, 0), pady=0)

        # Right panel header with view button
        right_header = ctk.CTkFrame(right, fg_color=("transparent"))
        right_header.pack(fill='x', pady=15, padx=15)
        
        ctk.CTkLabel(right_header, text='Medical Records', font=FONT_TITLE_MEDIUM).pack(side='left')
        
        view_btn_frame = ctk.CTkFrame(right_header, fg_color=("transparent"))
        view_btn_frame.pack(side='right')
        
        ctk.CTkButton(view_btn_frame, text='👁 View Record', command=self.view_selected_record, height=BUTTON_HEIGHT, font=FONT_BUTTON, width=140).pack(side='right', padx=5)

        self.txt = ctk.CTkTextbox(right, font=FONT_MONO, fg_color=COLOR_TEXT_BG)
        self.txt.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        self.view_records()

    def load_patients(self):
        """Load all patients into the dropdown"""
        try:
            patients = self.patient_manager.list_patients()
            self.patients_dict.clear()
            
            if not patients:
                self.patient_combo.configure(values=['No patients available'])
                return
            
            patient_list = []
            for p in patients:
                patient_display = f"{p['Patient_ID']}: {p['Surname']}, {p['FirstName']} ({p['Age']}, {p['Gender']})"
                patient_list.append(patient_display)
                self.patients_dict[patient_display] = p
            
            self.patient_combo.configure(values=patient_list)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load patients: {str(e)}')
    
    def load_doctors(self):
        """Load all doctors into the dropdown"""
        try:
            doctors = self.doctor_manager.list_doctors()
            
            if not doctors:
                self.doctor_combo.configure(values=['No doctors available'])
                return
            
            doctor_list = [f"{d['Doctor_ID']}: {d['Name']}" for d in doctors]
            self.doctor_combo.configure(values=doctor_list)
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load doctors: {str(e)}')

    def add_record(self):
        try:
            patient_selection = self.patient_combo.get()
            if not patient_selection or patient_selection in ['Select a patient...', 'No patients available']:
                messagebox.showerror('Validation Error', 'Please select a patient.')
                return
            
            # Extract patient ID from selection
            patient_id = patient_selection.split(':')[0].strip()
            
            doctor_selection = self.doctor_combo.get()
            if not doctor_selection or doctor_selection in ['Select a doctor...', 'No doctors available']:
                messagebox.showerror('Validation Error', 'Please select a doctor.')
                return
            
            # Extract doctor ID from selection (format: "ID: Name")
            doctor_id = doctor_selection.split(':')[0].strip()
            
            diagnosis = self.diagnosis.get().strip()
            notes = self.notes.get("1.0", "end-1c").strip()

            if not diagnosis:
                messagebox.showerror('Validation Error', 'Diagnosis is required.')
                return

            self.record_manager.add_record(patient_id, doctor_id, None, diagnosis, 'N/A', notes, 'N/A')
            messagebox.showinfo('Success', 'Medical record added successfully.')
            
            # Clear form
            self.patient_combo.set('Select a patient...')
            self.doctor_combo.set('Select a doctor...')
            self.diagnosis.delete(0, 'end')
            self.notes.delete("1.0", "end")
            self.view_records()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def view_records(self):
        try:
            records = self.record_manager.get_all_records()
            self.txt.delete('1.0', 'end')
            if not records:
                self.txt.insert('end', 'No medical records found.\n\nTip: Select a patient from the dropdown to view their detailed records.')
                return

            header = f"{'ID':<8} {'Patient':<30} {'Doctor':<30} {'Date':<20}\n"
            self.txt.insert('end', header)
            self.txt.insert('end', "="*90 + "\n")

            for r in records:
                self.txt.insert('end', f"{r['Record_ID']:<8} {r['Patient_Name']:<30} {r['Doctor_Name']:<30} {str(r['Recorded_Date']):<20}\n")
            
            self.txt.insert('end', "\n" + "="*90 + "\n")
            self.txt.insert('end', f"Total Records: {len(records)}")
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load records: {str(e)}')
    
    def view_selected_record(self):
        """View detailed records for selected patient"""
        try:
            patient_selection = self.patient_combo.get()
            if not patient_selection or patient_selection in ['Select a patient...', 'No patients available']:
                messagebox.showwarning('No Selection', 'Please select a patient to view their records.')
                return
            
            # Extract patient ID
            patient_id = patient_selection.split(':')[0].strip()
            
            # Get all records
            all_records = self.record_manager.get_all_records()
            
            # Filter by patient ID
            patient_records = [r for r in all_records if str(r.get('Patient_ID')) == patient_id]
            
            self.txt.delete('1.0', 'end')
            
            if not patient_records:
                patient = self.patients_dict.get(patient_selection)
                patient_name = f"{patient['Surname']}, {patient['FirstName']}" if patient else "Selected Patient"
                self.txt.insert('end', f'No medical records found for {patient_name}.\n')
                return
            
            # Display patient info
            patient = self.patients_dict.get(patient_selection)
            if patient:
                self.txt.insert('end', "=" * 90 + "\n")
                self.txt.insert('end', f"PATIENT INFORMATION\n")
                self.txt.insert('end', "=" * 90 + "\n")
                self.txt.insert('end', f"ID: {patient['Patient_ID']}\n")
                self.txt.insert('end', f"Name: {patient['Surname']}, {patient['FirstName']}\n")
                self.txt.insert('end', f"Age: {patient['Age']} | Gender: {patient['Gender']}\n")
                self.txt.insert('end', f"Contact: {patient.get('ContactNumber', 'N/A')}\n")
                self.txt.insert('end', f"Address: {patient.get('Address', 'N/A')}\n")
                self.txt.insert('end', "\n")
            
            # Display records
            self.txt.insert('end', "=" * 90 + "\n")
            self.txt.insert('end', f"MEDICAL RECORDS ({len(patient_records)} record(s))\n")
            self.txt.insert('end', "=" * 90 + "\n\n")
            
            for idx, r in enumerate(patient_records, 1):
                self.txt.insert('end', f"Record #{idx}\n")
                self.txt.insert('end', "-" * 90 + "\n")
                self.txt.insert('end', f"Record ID: {r.get('Record_ID', 'N/A')}\n")
                self.txt.insert('end', f"Date: {r.get('Recorded_Date', 'N/A')}\n")
                self.txt.insert('end', f"Doctor: {r.get('Doctor_Name', 'N/A')}\n")
                self.txt.insert('end', f"Diagnosis: {r.get('Diagnosis', 'N/A')}\n")
                self.txt.insert('end', f"Notes: {r.get('Clinical_Notes', 'N/A')}\n")
                self.txt.insert('end', "\n")
            
            self.txt.insert('end', "=" * 90 + "\n")
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to view records: {str(e)}')

    def pack(self, *args, **kwargs):
        self.view_records()
        super().pack(*args, **kwargs)