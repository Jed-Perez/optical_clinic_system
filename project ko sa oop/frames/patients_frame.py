import customtkinter as ctk
from tkinter import messagebox
from frames.base_frame import BaseFrame
from utils.alert_system import AlertSystem
from utils.input_validator import InputValidator
from utils.logger import setup_logging
from utils.ui_constants import *

logger = setup_logging(__name__)


class PatientsFrame(BaseFrame):
    def __init__(self, master, managers, *args, **kwargs):
        super().__init__(master, "Patient Management", ICON_PATIENT, *args, **kwargs)
        self.pm = managers['pm'] 
        self.build()

    def build(self):
        self.build_header()
        self.build_separator()
        
        # Main container
        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=PADDING_NORMAL, pady=PADDING_NORMAL)
        
        # Left panel - Input form
        left = ctk.CTkFrame(main, fg_color=COLOR_PANEL_BG, width=LEFT_PANEL_WIDTH)
        left.pack(side='left', fill='both', expand=False, padx=0, pady=0)
        left.pack_propagate(False)
        
        form_title = ctk.CTkLabel(left, text='Add New Patient', font=FONT_TITLE_MEDIUM)
        form_title.pack(pady=PADDING_NORMAL, padx=PADDING_LARGE)
        
        scroll_frame = ctk.CTkScrollableFrame(left, fg_color="transparent")
        scroll_frame.pack(fill='both', expand=True, padx=0, pady=0)
    
        frm = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        frm.pack(padx=PADDING_LARGE, pady=PADDING_SMALL, fill='x')
        
        ctk.CTkLabel(frm, text='Surname', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.surname = ctk.CTkEntry(frm, placeholder_text='Enter patient surname', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.surname.pack(fill='x', pady=(0, PADDING_SMALL))

        ctk.CTkLabel(frm, text='First Name', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.firstname = ctk.CTkEntry(frm, placeholder_text='Enter patient first name', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.firstname.pack(fill='x', pady=(0, PADDING_SMALL))

        ctk.CTkLabel(frm, text='Middle Initial', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.middleinitial = ctk.CTkEntry(frm, placeholder_text='(Optional)', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.middleinitial.pack(fill='x', pady=(0, PADDING_SMALL))

        ctk.CTkLabel(frm, text='Age', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.age = ctk.CTkEntry(frm, placeholder_text='Enter age', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.age.pack(fill='x', pady=(0, PADDING_SMALL))
        ctk.CTkLabel(frm, text='(Age Group will be auto-detected: Kids <18, Adult 18+)', font=('Segoe UI', 9), text_color=("gray50", "gray70")).pack(anchor='w', pady=(0, PADDING_SMALL))

        ctk.CTkLabel(frm, text='Gender', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.gender = ctk.CTkComboBox(frm, values=GENDERS, state='readonly', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.gender.set(GENDERS[0])
        self.gender.pack(fill='x', pady=(0, PADDING_SMALL))

        ctk.CTkLabel(frm, text='Contact', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_SMALL, 3))
        self.contact = ctk.CTkEntry(frm, placeholder_text='Phone number', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.contact.pack(fill='x', pady=(0, 20))

        btn_frm = ctk.CTkFrame(frm, fg_color="transparent")
        btn_frm.pack(fill='x', pady=PADDING_SMALL)
        
        ctk.CTkButton(btn_frm, text=f'{ICON_ADD} Add Patient', command=self.add_patient, height=BUTTON_HEIGHT, font=FONT_BUTTON, fg_color=BTN_SUCCESS).pack(fill='x', pady=PADDING_SMALL)
        ctk.CTkButton(btn_frm, text=f'{ICON_VIEW} View Patients', command=self.view_patients, height=BUTTON_HEIGHT, font=FONT_BUTTON).pack(fill='x', pady=PADDING_SMALL)
        ctk.CTkButton(btn_frm, text=f'{ICON_ARCHIVE} View Archive', command=self.view_archive, height=BUTTON_HEIGHT, font=FONT_BUTTON, fg_color=BTN_WARNING).pack(fill='x', pady=PADDING_SMALL)
        
        ctk.CTkLabel(frm, text='Load Patient by ID', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_NORMAL, 3))
        self.load_id = ctk.CTkEntry(frm, placeholder_text='Enter Patient ID to load', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.load_id.pack(fill='x', pady=(0, PADDING_TINY))
        ctk.CTkButton(frm, text=f'{ICON_SEARCH} Load Patient', command=self.load_patient, height=BUTTON_HEIGHT, font=FONT_BUTTON, fg_color=BTN_INFO).pack(fill='x', pady=PADDING_TINY)

        ctk.CTkLabel(frm, text='Delete Patient', font=FONT_LABEL_BOLD).pack(anchor='w', pady=(PADDING_NORMAL, 3))
        self.delete_id = ctk.CTkEntry(frm, placeholder_text='Enter Patient ID to delete', height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
        self.delete_id.pack(fill='x', pady=(0, PADDING_TINY))
        ctk.CTkButton(frm, text=f'{ICON_DELETE} Delete Patient', command=self.delete_patient, height=BUTTON_HEIGHT, font=FONT_BUTTON, fg_color=BTN_DANGER).pack(fill='x', pady=PADDING_TINY)
        
        right = ctk.CTkFrame(main, fg_color=COLOR_PANEL_BG)
        right.pack(side='right', fill='both', expand=True, padx=PADDING_NORMAL, pady=PADDING_NORMAL)
        
        title_search = ctk.CTkFrame(right, fg_color="transparent")
        title_search.pack(fill='x', pady=(0, PADDING_SMALL))
        ctk.CTkLabel(title_search, text='Patient List', font=FONT_TITLE_MEDIUM).pack(side='left')

        search_frm = ctk.CTkFrame(right, fg_color="transparent")
        search_frm.pack(fill='x', pady=(0, PADDING_SMALL))
        ctk.CTkLabel(search_frm, text=f'{ICON_SEARCH} Search:', font=FONT_LABEL_SMALL).pack(side='left', padx=(0, PADDING_TINY))
        self.search_entry = ctk.CTkEntry(search_frm, placeholder_text='Search by name or contact...', height=BUTTON_HEIGHT_TINY, font=FONT_LABEL_SMALL)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0, PADDING_TINY))
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_patients())
        
        ctk.CTkButton(search_frm, text='Clear', command=self.view_patients, height=BUTTON_HEIGHT_TINY, width=60, font=FONT_LABEL_SMALL).pack(side='left')
        
        self.txt = ctk.CTkTextbox(right, font=TEXTBOX_FONT, fg_color=COLOR_TEXT_BG)
        self.txt.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.view_patients()

    def add_patient(self):
        def _operation():
            surname = InputValidator.sanitize_string(self.surname.get())
            firstname = InputValidator.sanitize_string(self.firstname.get())
            middleinitial = InputValidator.sanitize_string(self.middleinitial.get())
            contact = InputValidator.sanitize_string(self.contact.get())
            gender = self.gender.get()
            
            is_valid, error = InputValidator.validate_required(surname, "Surname")
            if not is_valid:
                raise ValueError(error)
            
            is_valid, error = InputValidator.validate_required(firstname, "First Name")
            if not is_valid:
                raise ValueError(error)
            
            is_valid, error = InputValidator.validate_required(contact, "Contact")
            if not is_valid:
                raise ValueError(error)
   
            is_valid, error = InputValidator.validate_phone(contact, "Contact")
            if not is_valid:
                raise ValueError(error)
   
            age = None
            age_group = "Adult"  
            if self.age.get().strip():
                is_valid, error, age = InputValidator.validate_age(self.age.get())
                if not is_valid:
                    raise ValueError(error)
                
                age_group = InputValidator.get_age_group(age)

            full_name = f"{surname}, {firstname} {middleinitial}".strip()
            age_display = f"Age: {age}" if age else "Age: Not specified"
            if not self.ask_confirmation('Add Patient', f"Add patient '{full_name}' ({gender}, {age_display}, {age_group})?"):
                return
            
            self.pm.add_patient(surname, firstname, middleinitial, age, gender, age_group, '', contact, '', '')
            self.show_success('Success', f'Patient added successfully (Auto-categorized as: {age_group})')

            self.surname.delete(0, 'end')
            self.firstname.delete(0, 'end')
            self.middleinitial.delete(0, 'end')
            self.age.delete(0, 'end')
            self.gender.set(GENDERS[0])
            self.contact.delete(0, 'end')
            
            self.view_patients()
        
        self.safe_db_operation(_operation)

    def view_patients(self):
        def _operation():
            rows = self.pm.list_patients()
            self.txt.delete('1.0', 'end')
            for r in rows:
                self.txt.insert('end', f"{r['Patient_ID']} | {r['Name']} | Age: {r['Age']} | {r['Gender']} | {r.get('Age_Group', 'Adult')}\n")
            return rows
        
        result = self.safe_db_operation(_operation, "Error Loading Patients")
        if result is not None:
            self.logger.info(f"Displayed {len(result)} patients")

    def search_patients(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.view_patients()
            return
        
        def _operation():
            rows = self.pm.list_patients()
            self.txt.delete('1.0', 'end')
            matched = 0
            for r in rows:
                if query in r['Name'].lower() or query in str(r.get('Contact', '')).lower():
                    self.txt.insert('end', f"{r['Patient_ID']} | {r['Name']} | Age: {r['Age']} | {r['Gender']} | {r.get('Age_Group', 'Adult')}\n")
                    matched += 1
            
            if matched == 0:
                self.txt.insert('end', f"No patients found matching '{query}'")
            
            return matched
        
        result = self.safe_db_operation(_operation, "Error Searching Patients")
        if result is not None:
            self.logger.info(f"Search found {result} matching patients")

    def view_archive(self):
        def _operation():
            rows = self.pm.list_archived()
            self.txt.delete('1.0', 'end')
            for r in rows:
                self.txt.insert('end', f"{r['Patient_ID']} | {r['Name']} | Deleted: {r['Deleted_On']}\n")
            return rows
        
        result = self.safe_db_operation(_operation, "Error Loading Archive")
        if result is not None:
            self.logger.info(f"Displayed {len(result)} archived patients")

    def load_patient(self):
        def _operation():
            patient_id = InputValidator.sanitize_string(self.load_id.get())
            
            is_valid, error = InputValidator.validate_required(patient_id, "Patient ID")
            if not is_valid:
                raise ValueError(error)
            
            patient = self.pm.get_patient(patient_id)
            if not patient:
                raise ValueError(f'No patient found with ID {patient_id}')
            self.txt.delete('1.0', 'end')
            details = f"""Patient ID: {patient['Patient_ID']}
Name: {patient['Name']}
Age: {patient.get('Age', 'N/A')}
Gender: {patient.get('Gender', 'N/A')}
Age Group: {patient.get('Age_Group', 'Adult')}
Contact: {patient.get('Contact', 'N/A')}
Address: {patient.get('Address', 'N/A')}
Email: {patient.get('Email', 'N/A')}
Medical History: {patient.get('Medical_History', 'N/A')}
"""
            self.txt.insert('end', details)
            self.show_success('Success', f'Patient {patient_id} loaded successfully')
            self.load_id.delete(0, 'end')
            return patient
        
        self.safe_db_operation(_operation, "Error Loading Patient")

    def delete_patient(self):
        """Delete (archive) patient record."""
        def _operation():
            patient_id = InputValidator.sanitize_string(self.delete_id.get())
            
            is_valid, error = InputValidator.validate_required(patient_id, "Patient ID")
            if not is_valid:
                raise ValueError(error)
            
            if not self.ask_confirmation('Delete Patient', f"Delete patient with ID {patient_id}? This will move it to archive."):
                return
            
            self.pm.delete_patient(patient_id)
            self.show_success('Success', 'Patient deleted successfully')
            self.delete_id.delete(0, 'end')
            self.view_patients()
        
        self.safe_db_operation(_operation, "Error Deleting Patient")
