import customtkinter as ctk
from tkinter import messagebox
from utils.alert_system import AlertSystem
from utils.date_picker import DatePicker

class PrescriptionsFrame(ctk.CTkFrame):
    def __init__(self, master, prescription_manager, patient_manager, doctor_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pm = prescription_manager
        self.pat_m = patient_manager
        self.doc_m = doctor_manager
        self.build()

    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='👓 Prescription Management', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)
   
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)
        
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        left_frame = ctk.CTkFrame(main_container, fg_color=("white", "#0f0f0f"))
        left_frame.pack(side='left', fill='both', expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(left_frame, text='➕ New Prescription', font=('Segoe UI', 15, 'bold')).pack(anchor='w', pady=(0, 10))
        
        form_frame = ctk.CTkFrame(left_frame, fg_color=("#f0f0f0", "#1a1a1a"))
        form_frame.pack(padx=10, pady=10, fill='x')
        
        ctk.CTkLabel(form_frame, text='Patient', font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=10, pady=(8, 2))
        self.patient_combo = ctk.CTkComboBox(form_frame, state='readonly', height=32, font=('Segoe UI', 11))
        self.patient_combo.pack(fill='x', padx=10, pady=(0, 8))
        
        ctk.CTkLabel(form_frame, text='Doctor', font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=10, pady=(5, 2))
        self.doctor_combo = ctk.CTkComboBox(form_frame, state='readonly', height=32, font=('Segoe UI', 11))
        self.doctor_combo.pack(fill='x', padx=10, pady=(0, 8))

        ctk.CTkLabel(form_frame, text='🔴 Right Eye (OD)', font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        
        od_frame = ctk.CTkFrame(form_frame, fg_color=("transparent"))
        od_frame.pack(fill='x', padx=10, pady=(0, 8))
        
        ctk.CTkLabel(od_frame, text='Sph', font=('Segoe UI', 10)).pack(side='left', padx=2)
        self.od_sph = ctk.CTkEntry(od_frame, placeholder_text='-0.50', width=60, height=28, font=('Segoe UI', 10))
        self.od_sph.pack(side='left', padx=2)
        
        ctk.CTkLabel(od_frame, text='Cyl', font=('Segoe UI', 10)).pack(side='left', padx=2)
        self.od_cyl = ctk.CTkEntry(od_frame, placeholder_text='-0.50', width=60, height=28, font=('Segoe UI', 10))
        self.od_cyl.pack(side='left', padx=2)
        
        ctk.CTkLabel(od_frame, text='Axis', font=('Segoe UI', 10)).pack(side='left', padx=2)
        self.od_axis = ctk.CTkEntry(od_frame, placeholder_text='180', width=50, height=28, font=('Segoe UI', 10))
        self.od_axis.pack(side='left', padx=2)
        
        ctk.CTkLabel(od_frame, text='Add', font=('Segoe UI', 10)).pack(side='left', padx=2)
        self.od_add = ctk.CTkEntry(od_frame, placeholder_text='+2.50', width=60, height=28, font=('Segoe UI', 10))
        self.od_add.pack(side='left', padx=2)

        ctk.CTkLabel(form_frame, text='🔵 Left Eye (OS)', font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        
        os_frame = ctk.CTkFrame(form_frame, fg_color=("transparent"))
        os_frame.pack(fill='x', padx=10, pady=(0, 8))
        
        ctk.CTkLabel(os_frame, text='Sph', font=('Segoe UI', 10)).pack(side='left', padx=2)
        self.os_sph = ctk.CTkEntry(os_frame, placeholder_text='-0.50', width=60, height=28, font=('Segoe UI', 10))
        self.os_sph.pack(side='left', padx=2)
        
        ctk.CTkLabel(os_frame, text='Cyl', font=('Segoe UI', 10)).pack(side='left', padx=2)
        self.os_cyl = ctk.CTkEntry(os_frame, placeholder_text='-0.50', width=60, height=28, font=('Segoe UI', 10))
        self.os_cyl.pack(side='left', padx=2)
        
        ctk.CTkLabel(os_frame, text='Axis', font=('Segoe UI', 10)).pack(side='left', padx=2)
        self.os_axis = ctk.CTkEntry(os_frame, placeholder_text='180', width=50, height=28, font=('Segoe UI', 10))
        self.os_axis.pack(side='left', padx=2)
        
        ctk.CTkLabel(os_frame, text='Add', font=('Segoe UI', 10)).pack(side='left', padx=2)
        self.os_add = ctk.CTkEntry(os_frame, placeholder_text='+2.50', width=60, height=28, font=('Segoe UI', 10))
        self.os_add.pack(side='left', padx=2)
        
        ctk.CTkLabel(form_frame, text='Notes', font=('Segoe UI', 11, 'bold')).pack(anchor='w', padx=10, pady=(10, 2))
        self.notes = ctk.CTkTextbox(form_frame, height=80, font=('Segoe UI', 10))
        self.notes.pack(fill='x', padx=10, pady=(0, 8))
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color=("transparent"))
        btn_frame.pack(fill='x', padx=10, pady=10)
        ctk.CTkButton(btn_frame, text='✅ Create', command=self.create_prescription, height=35, font=('Segoe UI', 11, 'bold'), fg_color=("#27ae60", "#1e8449")).pack(fill='x', pady=4)
        ctk.CTkButton(btn_frame, text='🔄 Refresh', command=self.load_prescriptions, height=35, font=('Segoe UI', 11, 'bold')).pack(fill='x', pady=4)
        
        right_frame = ctk.CTkFrame(main_container, fg_color=("white", "#0f0f0f"))
        right_frame.pack(side='right', fill='both', expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(right_frame, text='📋 All Prescriptions', font=('Segoe UI', 15, 'bold')).pack(anchor='w', pady=(0, 10))
        
        self.prescriptions_txt = ctk.CTkTextbox(right_frame, font=('Consolas', 9), fg_color=("#f5f5f5", "#1a1a1a"))
        self.prescriptions_txt.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.load_combos()
        self.load_prescriptions()

    def load_combos(self):
        try:
            patients = self.pat_m.list_patients()
            patient_list = [f"{p['Patient_ID']} - {p['Name']}" for p in patients]
            self.patient_combo.configure(values=patient_list)
            
            doctors = self.doc_m.list_doctors()
            doctor_list = [f"{d['Doctor_ID']} - {d['Name']}" for d in doctors]
            self.doctor_combo.configure(values=doctor_list)
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def create_prescription(self):
        try:
            patient_id = int(self.patient_combo.get().split(' - ')[0]) if self.patient_combo.get() else None
            doctor_id = int(self.doctor_combo.get().split(' - ')[0]) if self.doctor_combo.get() else None
            
            if not patient_id or not doctor_id:
                messagebox.showerror('Validation Error', 'Patient and Doctor are required')
                return
            
            od_sph = float(self.od_sph.get()) if self.od_sph.get() else None
            od_cyl = float(self.od_cyl.get()) if self.od_cyl.get() else None
            od_axis = int(self.od_axis.get()) if self.od_axis.get() else None
            od_add = float(self.od_add.get()) if self.od_add.get() else None
            
            os_sph = float(self.os_sph.get()) if self.os_sph.get() else None
            os_cyl = float(self.os_cyl.get()) if self.os_cyl.get() else None
            os_axis = int(self.os_axis.get()) if self.os_axis.get() else None
            os_add = float(self.os_add.get()) if self.os_add.get() else None
            
            notes = self.notes.get('1.0', 'end').strip()
            
            self.pm.create_prescription(patient_id, doctor_id, None, 
                                       od_sph, od_cyl, od_axis, od_add,
                                       os_sph, os_cyl, os_axis, os_add, notes)
            
            messagebox.showinfo('Success', 'Prescription created successfully')
            self.clear_form()
            self.load_prescriptions()
        except ValueError as e:
            messagebox.showerror('Validation Error', f'Invalid numeric value: {str(e)}')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def load_prescriptions(self):
        try:
            prescriptions = self.pm.get_all_prescriptions()
            self.prescriptions_txt.delete('1.0', 'end')
            
            if not prescriptions:
                self.prescriptions_txt.insert('end', 'No prescriptions found')
                return
            
            for p in prescriptions:
                self.prescriptions_txt.insert('end', 
                    f"ID: {p['Prescription_ID']} | Patient: {p['Patient_Name']} | Doctor: {p['Doctor_Name']}\n"
                    f"  OD: {p['OD_Sphere']} {p['OD_Cylinder']} x{p['OD_Axis']} +{p['OD_Add']}\n"
                    f"  OS: {p['OS_Sphere']} {p['OS_Cylinder']} x{p['OS_Axis']} +{p['OS_Add']}\n"
                    f"  Issued: {p['Issued_Date']} | Expires: {p['Expiry_Date']}\n"
                    f"  Notes: {p['Notes']}\n\n")
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def clear_form(self):
        self.patient_combo.set('')
        self.doctor_combo.set('')
        self.od_sph.delete(0, 'end')
        self.od_cyl.delete(0, 'end')
        self.od_axis.delete(0, 'end')
        self.od_add.delete(0, 'end')
        self.os_sph.delete(0, 'end')
        self.os_cyl.delete(0, 'end')
        self.os_axis.delete(0, 'end')
        self.os_add.delete(0, 'end')
        self.notes.delete('1.0', 'end')
