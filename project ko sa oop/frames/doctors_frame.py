import customtkinter as ctk
from tkinter import messagebox
from utils.alert_system import AlertSystem

class DoctorsFrame(ctk.CTkFrame):
    def __init__(self, master, manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.manager = manager
        self.build()
    
    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='👨‍⚕️ Doctor Management', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)
        
        # Separator
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)
        
        # Main container
        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Left panel - Input form
        left = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"), width=350)
        left.pack(side='left', fill='both', expand=False, padx=0, pady=0)
        left.pack_propagate(False)
        
        # Form title
        form_title = ctk.CTkLabel(left, text='Add New Doctor', font=('Segoe UI', 16, 'bold'))
        form_title.pack(pady=15, padx=20)
        
        # Create scrollable frame for form
        scroll_frame = ctk.CTkScrollableFrame(left, fg_color=("transparent"))
        scroll_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Form frame
        frm = ctk.CTkFrame(scroll_frame, fg_color=("transparent"))
        frm.pack(padx=20, pady=10, fill='x')
        
        ctk.CTkLabel(frm, text='Surname *', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.surname = ctk.CTkEntry(frm, placeholder_text='Enter surname', height=35, font=('Segoe UI', 12))
        self.surname.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='First Name *', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.firstname = ctk.CTkEntry(frm, placeholder_text='Enter first name', height=35, font=('Segoe UI', 12))
        self.firstname.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Middle Initial', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.middle_initial = ctk.CTkEntry(frm, placeholder_text='M.I. (optional)', height=35, font=('Segoe UI', 12))
        self.middle_initial.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='License No *', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.lic = ctk.CTkEntry(frm, placeholder_text='License number', height=35, font=('Segoe UI', 12))
        self.lic.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Specialization *', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.spec = ctk.CTkEntry(frm, placeholder_text='Specialization', height=35, font=('Segoe UI', 12))
        self.spec.pack(fill='x', pady=(0, 20))
        
        # Button frame
        btn_frm = ctk.CTkFrame(frm, fg_color=("transparent"))
        btn_frm.pack(fill='x', pady=10)
        
        ctk.CTkButton(btn_frm, text='➕ Add Doctor', command=self.add_doctor, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#27ae60", "#1e8449")).pack(fill='x', pady=5)
        ctk.CTkButton(btn_frm, text='👁️ View Doctors', command=self.view_doctors, height=40, font=('Segoe UI', 12, 'bold')).pack(fill='x', pady=5)
        ctk.CTkButton(btn_frm, text='📑 View Archive', command=self.view_archive, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#f39c12", "#d68910")).pack(fill='x', pady=5)
        
        # Delete doctor section
        ctk.CTkLabel(frm, text='Delete Doctor', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(15, 3))
        self.delete_id = ctk.CTkEntry(frm, placeholder_text='Enter Doctor ID to delete', height=35, font=('Segoe UI', 12))
        self.delete_id.pack(fill='x', pady=(0, 10))
        ctk.CTkButton(frm, text='🗑️ Delete Doctor', command=self.delete_doctor, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#e74c3c", "#c0392b")).pack(fill='x', pady=5)
        
        # Right panel - Display
        right = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        right.pack(side='right', fill='both', expand=True, padx=15, pady=15)
        
        # Display title and search
        title_search = ctk.CTkFrame(right, fg_color=("transparent"))
        title_search.pack(fill='x', pady=(0, 10))
        ctk.CTkLabel(title_search, text='Doctor List', font=('Segoe UI', 16, 'bold')).pack(side='left')
        
        # Search frame
        search_frm = ctk.CTkFrame(right, fg_color=("transparent"))
        search_frm.pack(fill='x', pady=(0, 10))
        ctk.CTkLabel(search_frm, text='🔍 Search:', font=('Segoe UI', 11)).pack(side='left', padx=(0, 5))
        self.search_entry = ctk.CTkEntry(search_frm, placeholder_text='Search by name or specialization...', height=32, font=('Segoe UI', 11))
        self.search_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_doctors())
        
        ctk.CTkButton(search_frm, text='Clear', command=self.view_doctors, height=32, width=60, font=('Segoe UI', 11)).pack(side='left')
        
        self.txt = ctk.CTkTextbox(right, font=('Consolas', 11), fg_color=("#f5f5f5", "#1a1a1a"))
        self.txt.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.view_doctors()
    def add_doctor(self):
        try:
            surname = self.surname.get().strip()
            firstname = self.firstname.get().strip()
            middle_initial = self.middle_initial.get().strip()
            lic = self.lic.get().strip()
            spec = self.spec.get().strip()
            
            if not surname:
                AlertSystem.error('Validation Error', 'Surname is required')
                return
            if not firstname:
                AlertSystem.error('Validation Error', 'First name is required')
                return
            if not lic:
                AlertSystem.error('Validation Error', 'License number is required')
                return
            if not spec:
                AlertSystem.error('Validation Error', 'Specialization is required')
                return
         
            if middle_initial:
                full_name = f"{surname}, {firstname} {middle_initial}."
            else:
                full_name = f"{surname}, {firstname}"
            
            if not AlertSystem.confirm('Add Doctor', f"Add doctor '{full_name}'?"):
                return
            
            self.manager.add_doctor(surname, firstname, middle_initial, lic, spec, '', '')
            AlertSystem.success('Success', 'Doctor added successfully')
            self.surname.delete(0, 'end')
            self.firstname.delete(0, 'end')
            self.middle_initial.delete(0, 'end')
            self.lic.delete(0, 'end')
            self.spec.delete(0, 'end')
            self.view_doctors()
        except Exception as e:
            AlertSystem.error('Error', str(e))
    
    def view_doctors(self):
        rows=self.manager.list_doctors(); self.txt.delete('1.0','end')
        for r in rows: self.txt.insert('end', f"{r['Doctor_ID']} | {r['Name']} | {r['Specialization']} | {r['License_No']}\n")
    
    def search_doctors(self):
        """Search doctors by name or specialization"""
        query = self.search_entry.get().strip().lower()
        if not query:
            self.view_doctors()
            return
        
        rows = self.manager.list_doctors()
        self.txt.delete('1.0', 'end')
        matched = 0
        for r in rows:
            if query in r['Name'].lower() or query in r.get('Specialization', '').lower():
                self.txt.insert('end', f"{r['Doctor_ID']} | {r['Name']} | {r['Specialization']} | {r['License_No']}\n")
                matched += 1
        
        if matched == 0:
            self.txt.insert('end', f"No doctors found matching '{query}'")
    
    def view_archive(self):
        rows=self.manager.list_archived(); self.txt.delete('1.0','end')
        for r in rows: self.txt.insert('end', f"{r['Doctor_ID']} | {r['Name']} | Deleted: {r['Deleted_On']}\n")

    def delete_doctor(self):
        try:
            doctor_id = self.delete_id.get().strip()
            
            if not doctor_id:
                AlertSystem.error('Validation Error', 'Doctor ID is required')
                return
            if not AlertSystem.confirm('Delete Doctor', f"Delete doctor with ID {doctor_id}? This will move it to archive."):
                return
            
            self.manager.delete_doctor(doctor_id)
            AlertSystem.success('Success', 'Doctor deleted successfully')
            self.delete_id.delete(0, 'end')
            self.view_doctors()
        except Exception as e:
            AlertSystem.error('Error', str(e))

