"""Patient history and comprehensive view"""
import customtkinter as ctk
from tkinter import messagebox

class PatientHistoryFrame(ctk.CTkFrame):
    def __init__(self, master, patient_manager, prescription_manager, medical_records_manager, 
                 appointment_manager, sales_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pat_m = patient_manager
        self.pres_m = prescription_manager
        self.mr_m = medical_records_manager
        self.apt_m = appointment_manager
        self.sales_m = sales_manager
        self.current_patient = None
        self.build()

    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='👤 Patient History & Overview', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)
        
        # Separator
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)
        
        # Main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # ===== TOP: PATIENT SELECTION =====
        top_frame = ctk.CTkFrame(main_container, fg_color=("#f0f0f0", "#1a1a1a"))
        top_frame.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(top_frame, text='Select Patient:', font=('Segoe UI', 12, 'bold')).pack(side='left', padx=10, pady=10)
        self.patient_combo = ctk.CTkComboBox(top_frame, state='readonly', height=32, font=('Segoe UI', 11))
        self.patient_combo.pack(side='left', fill='x', expand=True, padx=10, pady=10)
        
        ctk.CTkButton(top_frame, text='📊 View', command=self.view_patient_history, height=32, font=('Segoe UI', 11, 'bold'), 
                      fg_color=("#3498db", "#2471a3")).pack(side='left', padx=5, pady=10)
        ctk.CTkButton(top_frame, text='🔄 Refresh', command=self.load_patients, height=32, font=('Segoe UI', 11)).pack(side='left', padx=5, pady=10)
        
        # ===== MAIN CONTENT AREA =====
        content_frame = ctk.CTkFrame(main_container)
        content_frame.pack(fill='both', expand=True)
        
        # Left sidebar - navigation
        nav_frame = ctk.CTkFrame(content_frame, fg_color=("#f0f0f0", "#1a1a1a"), width=180)
        nav_frame.pack(side='left', fill='y', padx=(0, 15))
        nav_frame.pack_propagate(False)
        
        ctk.CTkLabel(nav_frame, text='📑 Sections', font=('Segoe UI', 12, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.nav_buttons = {}
        sections = ['Overview', 'Appointments', 'Prescriptions', 'Medical Records', 'Sales History']
        for section in sections:
            btn = ctk.CTkButton(nav_frame, text=section, command=lambda s=section: self.show_section(s),
                               anchor='w', height=40, font=('Segoe UI', 11), fg_color=("#34495e", "#2c3e50"),
                               hover_color=("#3498db", "#2471a3"))
            btn.pack(fill='x', padx=5, pady=3)
            self.nav_buttons[section] = btn
        
        # Main display area
        display_frame = ctk.CTkFrame(content_frame, fg_color=("white", "#0f0f0f"))
        display_frame.pack(side='left', fill='both', expand=True)
        
        ctk.CTkLabel(display_frame, text='📄 Patient Information', font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=15, pady=(15, 10))
        
        self.content_txt = ctk.CTkTextbox(display_frame, font=('Consolas', 10), fg_color=("#f5f5f5", "#1a1a1a"))
        self.content_txt.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Load initial data
        self.load_patients()

    def load_patients(self):
        """Load list of patients"""
        try:
            patients = self.pat_m.list_patients()
            patient_list = [f"{p['Patient_ID']} - {p['Name']}" for p in patients]
            self.patient_combo.configure(values=patient_list)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def view_patient_history(self):
        """Load patient history"""
        try:
            patient_str = self.patient_combo.get()
            if not patient_str:
                messagebox.showerror('Error', 'Select a patient')
                return
            
            patient_id = int(patient_str.split(' - ')[0])
            patient = self.pat_m.list_patients()
            self.current_patient = next((p for p in patient if p['Patient_ID'] == patient_id), None)
            
            if not self.current_patient:
                messagebox.showerror('Error', 'Patient not found')
                return
            
            self.show_section('Overview')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def show_section(self, section):
        """Display selected section"""
        if not self.current_patient:
            messagebox.showerror('Error', 'Select a patient first')
            return
        
        try:
            self.content_txt.delete('1.0', 'end')
            
            if section == 'Overview':
                self.show_overview()
            elif section == 'Appointments':
                self.show_appointments()
            elif section == 'Prescriptions':
                self.show_prescriptions()
            elif section == 'Medical Records':
                self.show_medical_records()
            elif section == 'Sales History':
                self.show_sales_history()
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def show_overview(self):
        """Show patient overview"""
        p = self.current_patient
        created_date = p.get('Created_Date', 'N/A')
        self.content_txt.insert('end', 
            f"👤 PATIENT OVERVIEW\n{'='*60}\n\n"
            f"Patient ID: {p['Patient_ID']}\n"
            f"Name: {p['Name']}\n"
            f"Age: {p['Age']} years\n"
            f"Gender: {p['Gender']}\n"
            f"Contact: {p['Contact']}\n"
            f"Email: {p['Email']}\n"
            f"Address: {p['Address']}\n"
            f"Medical History: {p['Medical_History']}\n"
            f"Member Since: {created_date}\n\n")
        
        # Quick stats
        apts = [a for a in self.apt_m.list_appointments() if a['Patient_ID'] == p['Patient_ID']]
        presc = self.pres_m.get_patient_prescriptions(p['Patient_ID'])
        records = self.mr_m.get_patient_records(p['Patient_ID'])
        
        self.content_txt.insert('end', 
            f"📊 QUICK STATS\n{'='*60}\n"
            f"Total Appointments: {len(apts)}\n"
            f"Prescriptions: {len(presc) if presc else 0}\n"
            f"Medical Records: {len(records) if records else 0}\n\n")
        
        # Next follow-up
        followups = self.mr_m.check_due_followups()
        due = [f for f in followups if f['Patient_ID'] == p['Patient_ID']]
        if due:
            self.content_txt.insert('end', f"⚠️  DUE FOR FOLLOW-UP: {due[0]['Diagnosis']} (Since {due[0]['Recorded_Date']})\n")

    def show_appointments(self):
        """Show appointment history"""
        apts = [a for a in self.apt_m.list_appointments() if a['Patient_ID'] == self.current_patient['Patient_ID']]
        
        self.content_txt.insert('end', f"📅 APPOINTMENT HISTORY ({len(apts)} total)\n{'='*60}\n\n")
        
        if not apts:
            self.content_txt.insert('end', 'No appointments found')
            return
        
        for apt in sorted(apts, key=lambda x: x.get('Appointment_Date', x.get('Date', '')), reverse=True):
            apt_date = apt.get('Appointment_Date', apt.get('Date', 'N/A'))
            apt_time = apt.get('Appointment_Time', apt.get('Time', 'N/A'))
            self.content_txt.insert('end',
                f"ID: {apt.get('Appointment_ID', 'N/A')}\n"
                f"  Date: {apt_date} at {apt_time}\n"
                f"  Doctor: Dr. {apt.get('Doctor_ID', 'N/A')}\n"
                f"  Status: {apt.get('Status', 'N/A')}\n\n")

    def show_prescriptions(self):
        """Show prescription history"""
        presc = self.pres_m.get_patient_prescriptions(self.current_patient['Patient_ID'])
        
        self.content_txt.insert('end', f"👓 PRESCRIPTION HISTORY ({len(presc) if presc else 0} total)\n{'='*60}\n\n")
        
        if not presc:
            self.content_txt.insert('end', 'No prescriptions found')
            return
        
        for p in presc:
            valid = "✅ VALID" if p['Expiry_Date'] and p['Expiry_Date'] >= str(__import__('datetime').date.today()) else "❌ EXPIRED"
            self.content_txt.insert('end',
                f"ID: {p['Prescription_ID']} {valid}\n"
                f"  Issued: {p['Issued_Date']} | Expires: {p['Expiry_Date']}\n"
                f"  Doctor: {p['Doctor_Name']}\n"
                f"  Right Eye (OD): {p['OD_Sphere']} {p['OD_Cylinder']} x{p['OD_Axis']} +{p['OD_Add']}\n"
                f"  Left Eye (OS): {p['OS_Sphere']} {p['OS_Cylinder']} x{p['OS_Axis']} +{p['OS_Add']}\n"
                f"  Notes: {p['Notes']}\n\n")

    def show_medical_records(self):
        """Show medical records"""
        records = self.mr_m.get_patient_records(self.current_patient['Patient_ID'])
        
        self.content_txt.insert('end', f"📋 MEDICAL RECORDS ({len(records) if records else 0} total)\n{'='*60}\n\n")
        
        if not records:
            self.content_txt.insert('end', 'No medical records found')
            return
        
        for r in records:
            self.content_txt.insert('end',
                f"ID: {r['Record_ID']}\n"
                f"  Date: {r['Recorded_Date']}\n"
                f"  Doctor: {r['Doctor_Name']}\n"
                f"  Diagnosis: {r['Diagnosis']} ({r['Severity']})\n"
                f"  Clinical Notes: {r['Clinical_Notes']}\n"
                f"  Recommendations: {r['Recommendations']}\n"
                f"  Follow-up: {r['Follow_up_Days']} days\n\n")

    def show_sales_history(self):
        """Show sales/purchases history"""
        try:
            all_sales = self.sales_m.get_all_sales()
            # Filter sales by patient (linked through invoices)
            self.content_txt.insert('end', f"💰 SALES HISTORY\n{'='*60}\n\n")
            self.content_txt.insert('end', "Note: Sales linked to invoices/patient records\n\n")
            
            if all_sales:
                for sale in all_sales[:10]:
                    self.content_txt.insert('end',
                        f"Sale ID: {sale['id']}\n"
                        f"  Customer: {sale['customer_name']}\n"
                        f"  Total: ₱{sale['total']:,.2f}\n"
                        f"  Date: {sale['sale_date']}\n\n")
            else:
                self.content_txt.insert('end', 'No sales found')
        except Exception as e:
            self.content_txt.insert('end', f'Error: {str(e)}')
