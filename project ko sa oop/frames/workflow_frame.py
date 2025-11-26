import customtkinter as ctk
from tkinter import messagebox
from frames.base_frame import BaseFrame
from utils.input_validator import InputValidator
from utils.logger import setup_logging
from utils.ui_constants import *
from datetime import datetime, timedelta

logger = setup_logging(__name__)


class WorkflowFrame(BaseFrame):
    def __init__(self, master, managers, *args, **kwargs):
        super().__init__(master, "Patient Management", ICON_PATIENT, *args, **kwargs)
        self.managers = managers
        self.pm = managers['pm']
        self.pres_m = managers['pres_m']
        self.mr_m = managers['mr_m']
        self.bm = managers['bm']
        self.sm = managers['sm']
        self.dm = managers['dm']
        self.im = managers['im'] 
        
        self.current_patient = None
        self.current_step = 0
        self.doctors_list = []
        self.workflow_steps = [
            {"title": "1️⃣ Patient Check-In", "name": "registration"},
            {"title": "2️⃣ Eye Examination", "name": "examination"},
            {"title": "3️⃣ Sales", "name": "sales"},
            {"title": "4️⃣ Billing", "name": "billing"},
        ]
        self.build()

    def build(self):
        self.build_header()
        self.build_separator()
        
        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=PADDING_NORMAL, pady=PADDING_NORMAL)
        
        self.build_step_indicator(main)
        
        self.content_frame = ctk.CTkFrame(main, fg_color=COLOR_PANEL_BG)
        self.content_frame.pack(fill='both', expand=True, padx=0, pady=(PADDING_NORMAL, 0))
        
        self.show_step(0)

    def build_step_indicator(self, parent):
        indicator_frame = ctk.CTkFrame(parent, fg_color=COLOR_PANEL_LIGHT)
        indicator_frame.pack(fill='x', pady=(0, PADDING_NORMAL), padx=0)
        
        steps_row = ctk.CTkFrame(indicator_frame, fg_color="transparent")
        steps_row.pack(fill='x', padx=PADDING_NORMAL, pady=PADDING_NORMAL)
        
        for i, step in enumerate(self.workflow_steps):
            step_btn = ctk.CTkButton(
                steps_row, 
                text=step["title"], 
                command=lambda idx=i: self.show_step(idx),
                height=40,
                font=FONT_LABEL_BOLD,
                fg_color=BTN_INFO if i == 0 else ("#95a5a6", "#34495e"),
                hover_color=BTN_INFO if i <= self.current_step else ("#7f8c8d", "#2c3e50")
            )
            step_btn.pack(side='left', fill='x', expand=True, padx=(0, 5) if i < len(self.workflow_steps) - 1 else 0)

    def show_step(self, step_index):
        self.current_step = step_index
        
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        step = self.workflow_steps[step_index]
        
        if step["name"] == "registration":
            self.build_registration_step()
        elif step["name"] == "examination":
            self.build_examination_step()
        elif step["name"] == "billing":
            self.build_billing_step()
        elif step["name"] == "sales":
            self.build_sales_step()

    def build_registration_step(self):
        left = ctk.CTkFrame(self.content_frame, fg_color=COLOR_PANEL_BG, width=LEFT_PANEL_WIDTH)
        left.pack(side='left', fill='both', expand=False, padx=0, pady=0)
        left.pack_propagate(False)
        
        ctk.CTkLabel(left, text='Add New Patient', font=('Segoe UI', 20, 'bold')).pack(pady=15, padx=PADDING_LARGE)
        
        scroll_frame = ctk.CTkScrollableFrame(left, fg_color="transparent")
        scroll_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        frm = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        frm.pack(padx=PADDING_LARGE, pady=PADDING_SMALL, fill='x')
        
        ctk.CTkLabel(frm, text='Surname', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(10, 5))
        self.reg_surname = ctk.CTkEntry(frm, placeholder_text='Last name', height=45, font=('Segoe UI', 14))
        self.reg_surname.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='First Name', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.reg_firstname = ctk.CTkEntry(frm, placeholder_text='First name', height=45, font=('Segoe UI', 14))
        self.reg_firstname.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Middle Initial', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.reg_middleinit = ctk.CTkEntry(frm, placeholder_text='Middle initial', height=45, font=('Segoe UI', 14))
        self.reg_middleinit.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Age', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.reg_age = ctk.CTkEntry(frm, placeholder_text='Age', height=45, font=('Segoe UI', 14))
        self.reg_age.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Gender', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.reg_gender = ctk.CTkComboBox(frm, values=GENDERS, state='readonly', height=45, font=('Segoe UI', 14))
        self.reg_gender.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Contact', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.reg_contact = ctk.CTkEntry(frm, placeholder_text='Phone number', height=45, font=('Segoe UI', 14))
        self.reg_contact.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Address', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.reg_address = ctk.CTkEntry(frm, placeholder_text='Address', height=45, font=('Segoe UI', 14))
        self.reg_address.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Email', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.reg_email = ctk.CTkEntry(frm, placeholder_text='Email', height=45, font=('Segoe UI', 14))
        self.reg_email.pack(fill='x', pady=(0, 20))
        
        ctk.CTkButton(frm, text=f'{ICON_ADD} Register Patient', command=self.register_patient, height=50, font=('Segoe UI', 14, 'bold'), fg_color=BTN_SUCCESS).pack(fill='x', pady=10)
        
        ctk.CTkLabel(frm, text="", fg_color=COLOR_SEPARATOR, height=2).pack(fill='x', padx=0, pady=15)
        
        ctk.CTkLabel(frm, text='Delete Patient', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(10, 5))
        self.delete_patient_id = ctk.CTkEntry(frm, placeholder_text='Enter Patient ID to delete', height=45, font=('Segoe UI', 14))
        self.delete_patient_id.pack(fill='x', pady=(0, 10))
        
        ctk.CTkButton(frm, text=f'{ICON_DELETE} Delete Patient', command=self.delete_patient, height=50, font=('Segoe UI', 14, 'bold'), fg_color=BTN_DANGER).pack(fill='x', pady=10)
        
        right = ctk.CTkFrame(self.content_frame, fg_color=COLOR_PANEL_BG)
        right.pack(side='right', fill='both', expand=True, padx=PADDING_NORMAL, pady=0)
        
        ctk.CTkLabel(right, text='Recent Patients', font=('Segoe UI', 20, 'bold')).pack(anchor='w', padx=PADDING_LARGE, pady=(15, 10))
        
        self.patient_textbox = ctk.CTkTextbox(right, font=('Consolas', 14), fg_color=COLOR_TEXT_BG, height=300)
        self.patient_textbox.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=(0, PADDING_NORMAL))
        
        ctk.CTkButton(right, text='Select Patient for Examination', command=self.select_patient_for_examination, height=50, font=('Segoe UI', 14, 'bold'), fg_color=BTN_INFO).pack(fill='x', padx=PADDING_LARGE, pady=(0, PADDING_NORMAL))
        
        self.load_patients()

    def build_examination_step(self):
        main_container = ctk.CTkFrame(self.content_frame, fg_color=COLOR_PANEL_BG)
        main_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        scroll_frame = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        scroll_frame.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        frm = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        frm.pack(fill='both', expand=True, padx=20, pady=10)

        ctk.CTkLabel(frm, text='Select Patient *', font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(10, 5))
        self.exam_patient_list = self.get_patients_list()
        self.exam_patient = ctk.CTkComboBox(frm, values=self.exam_patient_list, state='readonly', height=45, font=('Segoe UI', 14), command=self.on_patient_selected)
        self.exam_patient.pack(fill='x', pady=(0, 10))
        
        self.exam_patient_info = ctk.CTkLabel(frm, text='', font=('Segoe UI', 13), justify='left')
        self.exam_patient_info.pack(anchor='w', padx=10, pady=10)
        
        ctk.CTkLabel(frm, text="", fg_color=COLOR_SEPARATOR, height=2).pack(fill='x', padx=0, pady=15)
        
        ctk.CTkLabel(frm, text='Examining Doctor *', font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(10, 5))
        self.exam_doctor = ctk.CTkComboBox(frm, values=self.get_doctors_list(), state='readonly', height=45, font=('Segoe UI', 14))
        self.exam_doctor.pack(fill='x', pady=(0, 20))
        
        ctk.CTkLabel(frm, text='OD (Right Eye) - Prescription', font=('Segoe UI', 18, 'bold'), text_color=("#2980b9", "#3498db")).pack(anchor='w', pady=(15, 10))
        
        od_frame = ctk.CTkFrame(frm, fg_color="transparent")
        od_frame.pack(fill='x', pady=(0, 20))
        
        od_left = ctk.CTkFrame(od_frame, fg_color="transparent")
        od_left.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ctk.CTkLabel(od_left, text='SPH (Sphere)', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 5))
        self.od_sphere = ctk.CTkEntry(od_left, placeholder_text='e.g., -2.00, +1.50', height=50, font=('Segoe UI', 16))
        self.od_sphere.pack(fill='x')
        
        od_right = ctk.CTkFrame(od_frame, fg_color="transparent")
        od_right.pack(side='left', fill='x', expand=True, padx=(10, 0))
        ctk.CTkLabel(od_right, text='CYL (Cylinder)', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 5))
        self.od_cylinder = ctk.CTkEntry(od_right, placeholder_text='e.g., -0.75, +0.50', height=50, font=('Segoe UI', 16))
        self.od_cylinder.pack(fill='x')
        
        ctk.CTkLabel(frm, text='OS (Left Eye) - Prescription', font=('Segoe UI', 18, 'bold'), text_color=("#27ae60", "#2ecc71")).pack(anchor='w', pady=(20, 10))
        
        os_frame = ctk.CTkFrame(frm, fg_color="transparent")
        os_frame.pack(fill='x', pady=(0, 20))
        
        os_left = ctk.CTkFrame(os_frame, fg_color="transparent")
        os_left.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ctk.CTkLabel(os_left, text='SPH (Sphere)', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 5))
        self.os_sphere = ctk.CTkEntry(os_left, placeholder_text='e.g., -2.00, +1.50', height=50, font=('Segoe UI', 16))
        self.os_sphere.pack(fill='x')
        
        os_right = ctk.CTkFrame(os_frame, fg_color="transparent")
        os_right.pack(side='left', fill='x', expand=True, padx=(10, 0))
        ctk.CTkLabel(os_right, text='CYL (Cylinder)', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(0, 5))
        self.os_cylinder = ctk.CTkEntry(os_right, placeholder_text='e.g., -0.75, +0.50', height=50, font=('Segoe UI', 16))
        self.os_cylinder.pack(fill='x')
        
        ctk.CTkLabel(frm, text="", fg_color=COLOR_SEPARATOR, height=2).pack(fill='x', padx=0, pady=20)
        
        ctk.CTkLabel(frm, text='Diagnosis *', font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(10, 5))
        diagnosis_values = [
            'Myopia (Nearsightedness)',
            'Hyperopia (Farsightedness)',
            'Astigmatism',
            'Presbyopia',
            'Myopia with Astigmatism',
            'Hyperopia with Astigmatism',
            'Emmetropia (Normal Vision)',
            'Amblyopia (Lazy Eye)',
            'Strabismus (Eye Misalignment)',
            'Cataracts',
            'Glaucoma',
            'Dry Eye Syndrome',
            'Conjunctivitis',
            'Keratoconus',
            'Retinal Detachment',
            'Macular Degeneration',
            'Diabetic Retinopathy',
            'Other - See Notes'
        ]
        self.exam_diagnosis = ctk.CTkComboBox(frm, values=diagnosis_values, state='readonly', height=50, font=('Segoe UI', 16))
        self.exam_diagnosis.set('Select Diagnosis')
        self.exam_diagnosis.pack(fill='x', pady=(0, 20))
        
        ctk.CTkLabel(frm, text='Clinical Notes', font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(10, 5))
        self.exam_notes = ctk.CTkTextbox(frm, font=('Segoe UI', 14), fg_color=COLOR_TEXT_BG, height=120)
        self.exam_notes.pack(fill='x', pady=(0, 20))
    
        ctk.CTkLabel(frm, text='Vision Test Results', font=('Segoe UI', 18, 'bold')).pack(anchor='w', pady=(20, 10))
        
        vision_grid = ctk.CTkFrame(frm, fg_color="transparent")
        vision_grid.pack(fill='x', pady=(0, 20))
        
        vision_left = ctk.CTkFrame(vision_grid, fg_color="transparent")
        vision_left.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ctk.CTkLabel(vision_left, text='OD Uncorrected Vision', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.va_od_before = ctk.CTkComboBox(vision_left, values=['20/20', '20/30', '20/40', '20/50', '20/60', '20/100'], state='readonly', height=45, font=('Segoe UI', 14))
        self.va_od_before.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(vision_left, text='OD Corrected Vision', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.va_od_after = ctk.CTkComboBox(vision_left, values=['20/20', '20/25', '20/30', '20/40', '20/50'], state='readonly', height=45, font=('Segoe UI', 14))
        self.va_od_after.pack(fill='x', pady=(0, 15))
        
        vision_right = ctk.CTkFrame(vision_grid, fg_color="transparent")
        vision_right.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        ctk.CTkLabel(vision_right, text='OS Uncorrected Vision', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.va_os_before = ctk.CTkComboBox(vision_right, values=['20/20', '20/30', '20/40', '20/50', '20/60', '20/100'], state='readonly', height=45, font=('Segoe UI', 14))
        self.va_os_before.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(vision_right, text='OS Corrected Vision', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.va_os_after = ctk.CTkComboBox(vision_right, values=['20/20', '20/25', '20/30', '20/40', '20/50'], state='readonly', height=45, font=('Segoe UI', 14))
        self.va_os_after.pack(fill='x', pady=(0, 15))
        
        additional_tests = ctk.CTkFrame(frm, fg_color="transparent")
        additional_tests.pack(fill='x', pady=(10, 20))
        
        test_left = ctk.CTkFrame(additional_tests, fg_color="transparent")
        test_left.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ctk.CTkLabel(test_left, text='Color Vision Test', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.color_vision = ctk.CTkComboBox(test_left, values=['Normal', 'Deficient', 'Color Blind'], state='readonly', height=45, font=('Segoe UI', 14))
        self.color_vision.pack(fill='x')
        
        test_right = ctk.CTkFrame(additional_tests, fg_color="transparent")
        test_right.pack(side='left', fill='x', expand=True, padx=(10, 0))
        ctk.CTkLabel(test_right, text='Intraocular Pressure (IOP)', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.iop = ctk.CTkEntry(test_right, placeholder_text='e.g., 16 mmHg', height=45, font=('Segoe UI', 14))
        self.iop.pack(fill='x')
        
        ctk.CTkButton(frm, text=f'{ICON_ADD} Complete Examination & Add ₱500 to Bill', command=self.complete_examination, height=55, font=('Segoe UI', 16, 'bold'), fg_color=BTN_SUCCESS).pack(fill='x', pady=(30, 20))

    def build_procedures_step(self):
        pass

    def build_billing_step(self):
        left = ctk.CTkFrame(self.content_frame, fg_color=COLOR_PANEL_BG, width=LEFT_PANEL_WIDTH)
        left.pack(side='left', fill='both', expand=False, padx=0, pady=0)
        left.pack_propagate(False)
        
        ctk.CTkLabel(left, text='Billing Management', font=('Segoe UI', 20, 'bold')).pack(pady=15, padx=PADDING_LARGE)
        
        scroll_frame = ctk.CTkScrollableFrame(left, fg_color="transparent")
        scroll_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        frm = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        frm.pack(padx=PADDING_LARGE, pady=PADDING_SMALL, fill='x')
        
        ctk.CTkLabel(frm, text='Select Patient *', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(10, 5))
        self.billing_patient_list = self.get_patients_list()
        self.billing_patient = ctk.CTkComboBox(frm, values=self.billing_patient_list, state='readonly', height=45, font=('Segoe UI', 14), command=self.on_billing_patient_selected)
        self.billing_patient.pack(fill='x', pady=(0, 10))
        
        self.billing_patient_info = ctk.CTkLabel(frm, text='', font=('Segoe UI', 13), justify='left')
        self.billing_patient_info.pack(anchor='w', padx=10, pady=10)
        
        ctk.CTkLabel(frm, text="", fg_color=COLOR_SEPARATOR, height=2).pack(fill='x', padx=0, pady=10)
       
        ctk.CTkLabel(frm, text='Add Additional Charges', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(10, 5))
        
        ctk.CTkLabel(frm, text='Service Type', font=('Segoe UI', 13)).pack(anchor='w', pady=(5, 5))
        self.additional_service = ctk.CTkComboBox(frm, values=['Contact Lens Fitting', 'Visual Field Test', 'Fundus Exam', 'Retinal Imaging', 'Other'], state='readonly', height=45, font=('Segoe UI', 14))
        self.additional_service.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Amount (₱)', font=('Segoe UI', 13)).pack(anchor='w', pady=(5, 5))
        self.additional_amount = ctk.CTkEntry(frm, placeholder_text='500-2000', height=45, font=('Segoe UI', 14))
        self.additional_amount.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Description', font=('Segoe UI', 13)).pack(anchor='w', pady=(5, 5))
        self.additional_notes = ctk.CTkTextbox(frm, font=('Segoe UI', 13), fg_color=COLOR_TEXT_BG, height=80)
        self.additional_notes.pack(fill='x', pady=(0, 20))
        
        ctk.CTkButton(frm, text=f'{ICON_ADD} Add Charge', command=self.add_billing_charge, height=50, font=('Segoe UI', 14, 'bold'), fg_color=BTN_SUCCESS).pack(fill='x', pady=10)
        
        right = ctk.CTkFrame(self.content_frame, fg_color=COLOR_PANEL_BG)
        right.pack(side='right', fill='both', expand=True, padx=PADDING_NORMAL, pady=0)
        
        ctk.CTkLabel(right, text='Bill Summary', font=('Segoe UI', 20, 'bold')).pack(anchor='w', padx=PADDING_LARGE, pady=15)
        
        self.bill_textbox = ctk.CTkTextbox(right, font=('Consolas', 14), fg_color=COLOR_TEXT_BG, height=300)
        self.bill_textbox.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_SMALL)
       
        button_frame = ctk.CTkFrame(right, fg_color="transparent")
        button_frame.pack(fill='x', padx=PADDING_LARGE, pady=PADDING_NORMAL)
        
        ctk.CTkButton(button_frame, text='Refresh Bills', command=self.refresh_billing_summary, height=50, font=('Segoe UI', 14, 'bold'), fg_color=BTN_INFO).pack(side='left', fill='x', expand=True, padx=(0, 5))
        ctk.CTkButton(button_frame, text='Apply Discount', command=self.apply_bill_discount, height=50, font=('Segoe UI', 14, 'bold'), fg_color=BTN_WARNING).pack(side='left', fill='x', expand=True, padx=(5, 0))

    def build_sales_step(self):
        scroll_container = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent")
        scroll_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        frm = ctk.CTkFrame(scroll_container, fg_color="transparent")
        frm.pack(fill='both', expand=True, padx=PADDING_LARGE, pady=PADDING_LARGE)
        
        ctk.CTkLabel(frm, text='Sales Management', font=('Segoe UI', 24, 'bold')).pack(anchor='w', pady=(0, 20))
        
        ctk.CTkLabel(frm, text='Select Patient *', font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(10, 5))
        self.sales_patient_list = self.get_patients_list()
        self.sales_patient = ctk.CTkComboBox(frm, values=self.sales_patient_list, state='readonly', height=50, font=('Segoe UI', 16), command=self.on_sales_patient_selected)
        self.sales_patient.pack(fill='x', pady=(0, 15))
        
        self.sales_patient_info = ctk.CTkLabel(frm, text='', font=('Segoe UI', 14), justify='left')
        self.sales_patient_info.pack(anchor='w', padx=10, pady=(0, 15))
        
        ctk.CTkLabel(frm, text="", fg_color=COLOR_SEPARATOR, height=2).pack(fill='x', padx=0, pady=15)
        
        ctk.CTkLabel(frm, text='Add Product to Sale', font=('Segoe UI', 18, 'bold')).pack(anchor='w', pady=(10, 15))
        
        ctk.CTkLabel(frm, text='Product Category *', font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(5, 5))
        self.product_category = ctk.CTkComboBox(frm, values=['Glasses', 'Frames', 'Lenses', 'Contact Lenses', 'Eye Care Products', 'Cleaning Solutions', 'Cases & Accessories', 'Reading Glasses', 'Sunglasses', 'Blue Light Glasses'], state='readonly', height=50, font=('Segoe UI', 16), command=self.on_category_selected)
        self.product_category.set('Glasses')
        self.product_category.pack(fill='x', pady=(0, 15))
        
        self.dynamic_fields_container = ctk.CTkFrame(frm, fg_color="transparent")
        self.dynamic_fields_container.pack(fill='x', pady=(0, 10))
        
        self.glasses_fields_frame = ctk.CTkFrame(self.dynamic_fields_container, fg_color="transparent")
        
        ctk.CTkLabel(self.glasses_fields_frame, text='Select Glasses Product (Optional)', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.glasses_product_combo = ctk.CTkComboBox(self.glasses_fields_frame, values=[], state='readonly', height=50, font=('Segoe UI', 16), command=self.on_glasses_product_selected)
        self.glasses_product_combo.set('Select from inventory or enter manually')
        self.glasses_product_combo.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(self.glasses_fields_frame, text='Frame Type', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.frame_type = ctk.CTkComboBox(self.glasses_fields_frame, values=['Full Frame', 'Half Frame', 'Rimless', 'Cat Eye', 'Oversized'], state='readonly', height=50, font=('Segoe UI', 16))
        self.frame_type.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(self.glasses_fields_frame, text='Lens Type', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.lens_type = ctk.CTkComboBox(self.glasses_fields_frame, values=['Single Vision', 'Bifocal', 'Progressive'], state='readonly', height=50, font=('Segoe UI', 16))
        self.lens_type.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(self.glasses_fields_frame, text='Lens Coating', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.lens_coating = ctk.CTkComboBox(self.glasses_fields_frame, values=['Standard', 'Anti-Glare', 'UV Protection', 'Blue Light', 'Transition'], state='readonly', height=50, font=('Segoe UI', 16))
        self.lens_coating.pack(fill='x', pady=(0, 15))

        self.generic_fields_frame = ctk.CTkFrame(self.dynamic_fields_container, fg_color="transparent")
        
        ctk.CTkLabel(self.generic_fields_frame, text='Select Product', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.product_name_combo = ctk.CTkComboBox(self.generic_fields_frame, values=[], state='readonly', height=50, font=('Segoe UI', 16), command=self.on_product_name_selected)
        self.product_name_combo.set('Select Product')
        self.product_name_combo.pack(fill='x', pady=(0, 15))
        self.product_map = {}
        
        ctk.CTkLabel(self.generic_fields_frame, text='Description', font=('Segoe UI', 14, 'bold')).pack(anchor='w', pady=(5, 5))
        self.product_description = ctk.CTkEntry(self.generic_fields_frame, placeholder_text='Product description', height=50, font=('Segoe UI', 16), state='readonly')
        self.product_description.pack(fill='x', pady=(0, 15))
        
        self.glasses_fields_frame.pack(fill='x', pady=0)
        
        self.load_products_by_category('Glasses')
        
        ctk.CTkLabel(frm, text='Quantity *', font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(5, 5))
        self.product_quantity = ctk.CTkEntry(frm, placeholder_text='1', height=50, font=('Segoe UI', 16))
        self.product_quantity.insert(0, '1')
        self.product_quantity.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(frm, text='Price (₱) *', font=('Segoe UI', 16, 'bold')).pack(anchor='w', pady=(5, 5))
        self.product_price = ctk.CTkEntry(frm, placeholder_text='Enter price', height=50, font=('Segoe UI', 16))
        self.product_price.pack(fill='x', pady=(0, 20))
        
        button_container = ctk.CTkFrame(frm, fg_color="transparent")
        button_container.pack(fill='x', pady=(10, 0))
        
        ctk.CTkButton(button_container, text=f'{ICON_ADD} Add to Sale', command=self.add_product_to_sales, height=55, font=('Segoe UI', 16, 'bold'), fg_color=BTN_SUCCESS).pack(side='left', fill='x', expand=True, padx=(0, 5))
        ctk.CTkButton(button_container, text='Complete Sale', command=self.complete_sales_visit, height=55, font=('Segoe UI', 16, 'bold'), fg_color=BTN_PRIMARY).pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        ctk.CTkLabel(frm, text="", fg_color=COLOR_SEPARATOR, height=2).pack(fill='x', padx=0, pady=20)
        
        ctk.CTkLabel(frm, text='Sales Summary', font=('Segoe UI', 18, 'bold')).pack(anchor='w', pady=(10, 10))
        
        self.sales_summary_textbox = ctk.CTkTextbox(frm, font=('Consolas', 14), fg_color=COLOR_TEXT_BG, height=250)
        self.sales_summary_textbox.pack(fill='x', pady=(0, 10))

    def on_billing_patient_selected(self, selected=None):
        try:
            if not selected:
                selected = self.billing_patient.get()
            if selected and selected in self.patients_dict:
                self.billing_patient_info_obj = self.patients_dict[selected]
                
                patient_info = f"Patient: {self.billing_patient_info_obj['Surname']}, {self.billing_patient_info_obj['FirstName']}\nID: {self.billing_patient_info_obj['Patient_ID']}\nAge: {self.billing_patient_info_obj['Age']} | {self.billing_patient_info_obj['Gender']}\nContact: {self.billing_patient_info_obj['Contact']}"
                self.billing_patient_info.configure(text=patient_info)
                
                self.refresh_billing_summary()
        except Exception as e:
            logger.error(f"Error selecting billing patient: {e}")
            self.show_error('Error', str(e))

    def on_sales_patient_selected(self, selected=None):
        try:
            if not selected:
                selected = self.sales_patient.get()
            if selected and selected in self.patients_dict:
                self.sales_patient_info_obj = self.patients_dict[selected]
                
                patient_info = f"Patient: {self.sales_patient_info_obj['Surname']}, {self.sales_patient_info_obj['FirstName']}\nID: {self.sales_patient_info_obj['Patient_ID']}\nAge: {self.sales_patient_info_obj['Age']} | {self.sales_patient_info_obj['Gender']}\nContact: {self.sales_patient_info_obj['Contact']}"
                self.sales_patient_info.configure(text=patient_info)
                
                self.refresh_sales_summary()
        except Exception as e:
            logger.error(f"Error selecting sales patient: {e}")
            self.show_error('Error', str(e))

    def load_patients(self):
        self.patient_textbox.delete('1.0', 'end')
        try:
            patients = self.pm.list_patients()
            if not patients:
                self.patient_textbox.insert('end', 'No patients found.')
                return
            
            self.patient_textbox.insert('end', f"{'ID':<6} {'Name':<30} {'Age':<6} {'Contact':<12}\n")
            self.patient_textbox.insert('end', "=" * 60 + "\n")
            
            for p in patients[-20:]:  # Show last 20
                name = f"{p['Surname']}, {p['FirstName']}"
                self.patient_textbox.insert('end', f"{p['Patient_ID']:<6} {name:<30} {p['Age']:<6} {p['Contact']:<12}\n")
        except Exception as e:
            logger.error(f"Error loading patients: {e}")
            self.patient_textbox.insert('end', f"Error: {e}")

    def get_doctors_list(self):
        try:
            self.doctors_list = self.dm.list_doctors()  # Store full list
            return [d['Name'] for d in self.doctors_list] if self.doctors_list else ['No doctors available']
        except:
            self.doctors_list = []
            return ['No doctors available']

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

    def on_patient_selected(self, selected=None):
        try:
            if not selected:
                selected = self.exam_patient.get()
            if selected and selected in self.patients_dict:
                self.current_patient = self.patients_dict[selected]
                patient_info = f"Patient: {self.current_patient['Surname']}, {self.current_patient['FirstName']}\nID: {self.current_patient['Patient_ID']}\nAge: {self.current_patient['Age']} | {self.current_patient['Gender']}\nContact: {self.current_patient['Contact']}"
                self.exam_patient_info.configure(text=patient_info)
        except Exception as e:
            logger.error(f"Error selecting patient: {e}")
            self.show_error('Error', str(e))

    def register_patient(self):
        try:
            surname = self.reg_surname.get().strip()
            firstname = self.reg_firstname.get().strip()
            middleinit = self.reg_middleinit.get().strip()
            age = self.reg_age.get().strip()
            gender = self.reg_gender.get()
            contact = self.reg_contact.get().strip()
            address = self.reg_address.get().strip()
            email = self.reg_email.get().strip()
            
            if not surname or not firstname or not gender or not contact:
                self.show_error('Validation Error', 'Please fill in required fields')
                return
            
            age_int = int(age) if age else None
            age_group = InputValidator.get_age_group(age_int) if age_int else 'Adult'
            
            self.pm.add_patient(surname, firstname, middleinit, age_int, gender, age_group, address, contact, email, '')
            
            self.show_success('Success', f'Patient {firstname} {surname} registered successfully!')
            
            # Set as current patient
            patients = self.pm.list_patients()
            self.current_patient = patients[0] if patients else None
            
            self.reg_surname.delete(0, 'end')
            self.reg_firstname.delete(0, 'end')
            self.reg_middleinit.delete(0, 'end')
            self.reg_age.delete(0, 'end')
            self.reg_contact.delete(0, 'end')
            self.reg_address.delete(0, 'end')
            self.reg_email.delete(0, 'end')
            
            self.load_patients()
            
        except Exception as e:
            logger.error(f"Error registering patient: {e}")
            self.show_error('Error', str(e))

    def delete_patient(self):
        try:
            patient_id = self.delete_patient_id.get().strip()
            
            if not patient_id:
                self.show_error('Validation Error', 'Please enter a Patient ID')
                return
            
            # Get patient info for confirmation
            try:
                patient = self.pm.get_patient_by_id(patient_id)
                if not patient:
                    self.show_error('Error', f'Patient ID {patient_id} not found')
                    return
                
                patient_name = f"{patient['Surname']}, {patient['FirstName']}"
                
                from tkinter import messagebox
                confirm = messagebox.askyesno(
                    'Delete Patient',
                    f'Are you sure you want to delete:\n\n{patient_name}\nID: {patient_id}\n\nThis will move the patient to the archive.'
                )
                
                if not confirm:
                    return
                
                self.pm.archive_patient(patient_id)
                self.show_success('Success', f'Patient {patient_name} has been moved to archive')
                
                self.delete_patient_id.delete(0, 'end')
                self.load_patients()
                
            except Exception as e:
                self.show_error('Error', f'Patient ID {patient_id} not found')
                
        except Exception as e:
            logger.error(f"Error deleting patient: {e}")
            self.show_error('Error', str(e))

    def select_patient_for_examination(self):
        try:
            patients = self.pm.list_patients()
            if not patients:
                self.show_error('Error', 'No patients available')
                return
            
            patient_names = [f"{p['Patient_ID']}: {p['Surname']}, {p['FirstName']}" for p in patients]
            
            self.current_patient = patients[0]
            self.show_success('Success', f'Selected: {self.current_patient["Surname"]}, {self.current_patient["FirstName"]}')
            
            self.show_step(1)
        except Exception as e:
            logger.error(f"Error selecting patient: {e}")
            self.show_error('Error', str(e))

    def complete_examination(self):
        if not self.current_patient:
            self.show_error('Error', 'No patient selected')
            return
        
        if self.current_step != 1:
            self.show_error('Error', 'Please stay on examination step to complete exam')
            return
        
        try:
            if not hasattr(self, 'exam_notes'):
                self.show_error('Error', 'Please stay on examination step to complete exam')
                return
            
            doctor_name = self.exam_doctor.get().strip()
            od_sphere = self.od_sphere.get().strip()
            od_cylinder = self.od_cylinder.get().strip()
            os_sphere = self.os_sphere.get().strip()
            os_cylinder = self.os_cylinder.get().strip()
            diagnosis = self.exam_diagnosis.get().strip()
            notes = self.exam_notes.get('1.0', 'end-1c').strip()
            
            # Vision test data
            va_od_before = self.va_od_before.get()
            va_od_after = self.va_od_after.get()
            va_os_before = self.va_os_before.get()
            va_os_after = self.va_os_after.get()
            color_vision = self.color_vision.get()
            iop = self.iop.get().strip()
        except Exception as e:
            logger.error(f"Error accessing examination form fields: {e}")
            self.show_error('Error', 'Please stay on examination step to complete exam')
            return
        
        try:
            if not doctor_name:
                self.show_error('Error', 'Please select a doctor')
                return
            
            if not od_sphere or not os_sphere:
                self.show_error('Error', 'Please enter OD and OS sphere values')
                return
            
            if not diagnosis:
                self.show_error('Error', 'Please enter diagnosis')
                return
            
            doctor_id = None
            for doc in self.doctors_list:
                if doc['Name'] == doctor_name:
                    doctor_id = doc['Doctor_ID']
                    break
            
            if not doctor_id:
                self.show_error('Error', 'Invalid doctor selection')
                return
            
            patient_id = self.current_patient['Patient_ID']
            exam_cost = 500
            
            vision_test_notes = f"VA OD Uncorrected: {va_od_before}, Corrected: {va_od_after}\nVA OS Uncorrected: {va_os_before}, Corrected: {va_os_after}\nColor Vision: {color_vision}\nIOP: {iop}"
            full_notes = f"{notes}\n\nVision Tests:\n{vision_test_notes}"
            
            self.mr_m.add_record(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_id=None,
                diagnosis=diagnosis,
                severity='Normal',
                clinical_notes=full_notes,
                recommendations='Follow prescription',
                followup_days=90
            )
            
            self.pres_m.create_prescription(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_id=None,
                od_sph=od_sphere,
                od_cyl=od_cylinder or '0.00',
                od_axis='0',
                od_add='0.00',
                os_sph=os_sphere,
                os_cyl=os_cylinder or '0.00',
                os_axis='0',
                os_add='0.00',
                notes=notes or ''
            )
            
            self.bm.add_billing(
                patient_id=patient_id,
                amount=exam_cost,
                service='Eye Examination',
                method='Direct',
                status='Pending'
            )
            
            try:
                self.od_sphere.delete(0, 'end')
                self.od_cylinder.delete(0, 'end')
                self.os_sphere.delete(0, 'end')
                self.os_cylinder.delete(0, 'end')
                self.exam_diagnosis.delete(0, 'end')
                self.exam_notes.delete('1.0', 'end')
                self.va_od_before.set('')
                self.va_od_after.set('')
                self.va_os_before.set('')
                self.va_os_after.set('')
                self.color_vision.set('')
                self.iop.delete(0, 'end')
                self.exam_doctor.set('')
                self.exam_patient.set('')
                self.exam_patient_info.configure(text='')
            except Exception as e:
                pass
            
            self.current_patient = None
            
            self.show_success('Success', f'Examination & vision tests completed!\n₱{exam_cost} added to patient billing.\n\nMoving to billing step...')
            
            self.show_step(2)
            
        except Exception as e:
            logger.error(f"Error completing examination: {e}")
            self.show_error('Error', str(e))

    def schedule_procedure(self):
        try:
            if not self.current_patient:
                self.show_error('Error', 'No patient selected')
                return
            
            od_sphere = self.od_sphere.get().strip()
            os_sphere = self.os_sphere.get().strip()
            notes = self.prescription_notes.get('1.0', 'end').strip()
            
            if not od_sphere or not os_sphere:
                self.show_error('Error', 'Please enter sphere values for both eyes')
                return
            
            self.pres_m.create_prescription(
                self.current_patient['Patient_ID'],
                1,
                None,
                od_sphere,
                self.od_cylinder.get().strip(),
                self.od_axis.get().strip(),
                "",
                os_sphere,
                self.os_cylinder.get().strip(),
                self.os_axis.get().strip(),
                "",
                notes
            )
            
            self.show_success('Success', 'Prescription saved successfully!')
            
        except Exception as e:
            logger.error(f"Error saving prescription: {e}")
            self.show_error('Error', str(e))
    
    def save_prescription(self):
        return self.schedule_procedure()

    def create_bill(self):
        try:
            if not self.current_patient:
                self.show_error('Error', 'No patient selected')
                return
            
            amount = self.bill_amount.get().strip()
            method = self.bill_method.get()
            status = self.bill_status.get()
            
            if not amount or not method or not status:
                self.show_error('Error', 'Please fill all fields')
                return
            
            amount_float = float(amount)
            self.bm.add_billing(self.current_patient['Patient_ID'], amount_float, method, status)
            
            self.show_success('Success', f'Bill of ₱{amount} created!')
            
        except Exception as e:
            logger.error(f"Error creating bill: {e}")
            self.show_error('Error', str(e))

    def add_to_sale(self):
        try:
            if not self.current_patient:
                self.show_error('Error', 'No patient selected')
                return
            
            category = self.sales_category.get()
            desc = self.sales_desc.get().strip()
            price = self.sales_price.get().strip()
            qty = self.sales_qty.get().strip()
            
            if not category or not desc or not price or not qty:
                self.show_error('Error', 'Please fill all fields')
                return
            
            try:
                self.sm.add_product(desc, category, f"Sold to {self.current_patient['Surname']}", float(price), int(qty))
            except:
                pass
            
            self.show_success('Success', f'Added {qty} × {desc} to sale for ₱{price}!')
            
            self.sales_desc.delete(0, 'end')
            self.sales_price.delete(0, 'end')
            self.sales_qty.delete(0, 'end')
            self.sales_category.set('')
            
        except Exception as e:
            logger.error(f"Error adding to sale: {e}")
            self.show_error('Error', str(e))

    def add_billing_charge(self):
        try:
            if not hasattr(self, 'billing_patient_info_obj') or not self.billing_patient_info_obj:
                self.show_error('Error', 'Please select a patient first')
                return
            
            service = self.additional_service.get()
            amount = self.additional_amount.get().strip()
            
            if not service or not amount:
                self.show_error('Error', 'Please select service and enter amount')
                return
            
            amount_value = float(amount)
            patient_id = self.billing_patient_info_obj['Patient_ID']
            
            self.bm.add_billing(
                patient_id=patient_id,
                amount=amount_value,
                service=service,
                method='Direct',
                status='Pending'
            )
            
            self.show_success('Success', f'{service}\n₱{amount_value:.2f} added to bill')
            
            self.additional_service.set('')
            self.additional_amount.delete(0, 'end')
            self.additional_notes.delete('1.0', 'end')
            
            self.refresh_billing_summary()
            
        except ValueError:
            self.show_error('Error', 'Please enter a valid amount')
        except Exception as e:
            logger.error(f"Error adding charge: {e}")
            self.show_error('Error', str(e))

    def refresh_billing_summary(self):
        self.bill_textbox.delete('1.0', 'end')
        try:
            if not hasattr(self, 'billing_patient_info_obj') or not self.billing_patient_info_obj:
                self.bill_textbox.insert('end', 'Please select a patient to view their bills.')
                return
            
            bills = self.bm.list_bills()
            if not bills:
                self.bill_textbox.insert('end', 'No bills created yet.')
                return
            
            patient_bills = [b for b in bills if b['Patient_ID'] == self.billing_patient_info_obj['Patient_ID']]
            
            if not patient_bills:
                self.bill_textbox.insert('end', f"No bills for {self.billing_patient_info_obj['Surname']}, {self.billing_patient_info_obj['FirstName']}")
                return
            
            total = 0
            bill_text = "ITEMIZED BILL:\n" + "="*40 + "\n"
            for bill in patient_bills:
                amount = float(bill['Amount'])
                total += amount
                method = bill.get('Payment_Method', 'N/A')
                bill_text += f"Bill #{bill['Bill_ID']:<13} ₱{amount:>8.2f} ({method})\n"
            
            bill_text += "-"*40 + "\n"
            bill_text += f"{'SUBTOTAL':<20} ₱{total:>8.2f}\n"
            bill_text += f"{'TAX (12%)':<20} ₱{(total*0.12):>8.2f}\n"
            bill_text += "="*40 + "\n"
            bill_text += f"{'TOTAL':<20} ₱{(total*1.12):>8.2f}\n"
            
            self.bill_textbox.insert('end', bill_text)
        except Exception as e:
            logger.error(f"Error loading bill summary: {e}")
            self.bill_textbox.insert('end', f"Error loading bills: {str(e)}")

    def apply_bill_discount(self):
        try:
            if not hasattr(self, 'billing_patient_info_obj'):
                self.show_error('Error', 'Please select a patient first')
                return
            
            self.show_success('Discount Applied', 'Discount feature coming soon!')
            
        except Exception as e:
            logger.error(f"Error applying discount: {e}")
            self.show_error('Error', str(e))

    def save_vision_test(self):
        try:
            if not self.current_patient:
                self.show_error('Error', 'No patient selected')
                return
            
            od_before = self.va_od_before.get()
            od_after = self.va_od_after.get()
            os_before = self.va_os_before.get()
            os_after = self.va_os_after.get()
            color_vision = self.color_vision.get()
            iop = self.iop.get().strip()
            notes = self.va_notes.get('1.0', 'end-1c').strip()
            
            if not all([od_before, od_after, os_before, os_after, color_vision]):
                self.show_error('Error', 'Please complete all vision tests')
                return
            
            test_summary = f"""
VISUAL ACUITY TEST RESULTS:
OD (Right): {od_before} → {od_after}
OS (Left): {os_before} → {os_after}
Color Vision: {color_vision}
IOP: {iop} mmHg
Notes: {notes}
            """
            
            self.show_success('Success', f'Vision test results saved!\n\n{test_summary}')
            self.load_bill_summary()
            
        except Exception as e:
            logger.error(f"Error saving vision test: {e}")
            self.show_error('Error', str(e))

    def confirm_bill(self):
        try:
            if not self.current_patient:
                self.show_error('Error', 'No patient selected')
                return
            
            bills = self.bm.list_bills()
            patient_bills = [b for b in bills if b['Patient_ID'] == self.current_patient['Patient_ID']]
            
            if not patient_bills:
                self.show_error('Error', 'No bills to confirm')
                return
            
            total = sum(float(b['Amount']) for b in patient_bills)
            
            self.show_success('Success', f'Bill confirmed!\n\nSubtotal: ₱{total:.2f}\nWith 12% Tax: ₱{total*1.12:.2f}\n\nReady for sales!')
            
        except Exception as e:
            logger.error(f"Error confirming bill: {e}")
            self.show_error('Error', str(e))

    def apply_discount(self):
        try:
            discount_window = ctk.CTkToplevel(self)
            discount_window.title("Apply Discount")
            discount_window.geometry("400x200")
            
            ctk.CTkLabel(discount_window, text="Discount Amount (₱)", font=FONT_LABEL_BOLD).pack(pady=10)
            discount_entry = ctk.CTkEntry(discount_window, placeholder_text="e.g., 100", height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
            discount_entry.pack(padx=20, fill='x', pady=5)
            
            ctk.CTkLabel(discount_window, text="Reason", font=FONT_LABEL_BOLD).pack(pady=10)
            reason_entry = ctk.CTkEntry(discount_window, placeholder_text="e.g., Senior Citizen, Student", height=ENTRY_HEIGHT, font=FONT_LABEL_NORMAL)
            reason_entry.pack(padx=20, fill='x', pady=5)
            
            def apply():
                try:
                    discount = float(discount_entry.get())
                    reason = reason_entry.get().strip()
                    if discount > 0:
                        self.show_success('Success', f'Discount of ₱{discount} applied!\nReason: {reason}')
                        discount_window.destroy()
                except:
                    self.show_error('Error', 'Invalid discount amount')
            
            ctk.CTkButton(discount_window, text='Apply', command=apply, height=BUTTON_HEIGHT, font=FONT_BUTTON, fg_color=BTN_SUCCESS).pack(pady=20, padx=20, fill='x')
            
        except Exception as e:
            logger.error(f"Error applying discount: {e}")

    def on_category_selected(self, choice=None):
        category = self.product_category.get()
        
        self.glasses_fields_frame.pack_forget()
        self.generic_fields_frame.pack_forget()
        
        if category == 'Glasses':
            self.glasses_fields_frame.pack(fill='x', pady=0)
            self.load_products_by_category(category)
        else:
            self.generic_fields_frame.pack(fill='x', pady=0)
            self.load_products_by_category(category)
    
    def load_products_by_category(self, category):
        try:
            if category == 'Glasses':
                if not hasattr(self, 'glasses_product_combo') or not self.glasses_product_combo.winfo_exists():
                    return
            else:
                if not hasattr(self, 'product_name_combo') or not self.product_name_combo.winfo_exists():
                    return
            
            all_products = self.im.list_items()
            
            category_products = [p for p in all_products if p.get('Category') == category]
            
            self.product_map.clear()
            
            if not category_products:
                if category == 'Glasses':
                    self.glasses_product_combo.configure(values=['No products available'])
                    self.glasses_product_combo.set('No products available')
                else:
                    self.product_name_combo.configure(values=['No products available'])
                    self.product_name_combo.set('No products available')
                return
            
            product_names = []
            for product in category_products:
                name = product.get('Item_Name', 'Unknown')
                price = product.get('Unit_Price', 0)
                display_name = f"{name} (\u20b1{price})"
                product_names.append(display_name)
                self.product_map[display_name] = product
            
            if category == 'Glasses':
                self.glasses_product_combo.configure(values=product_names)
                if product_names:
                    self.glasses_product_combo.set(product_names[0])
                    self.on_glasses_product_selected(product_names[0])
                else:
                    self.glasses_product_combo.set('Select from inventory or enter manually')
            else:
                self.product_name_combo.configure(values=product_names)
                if product_names:
                    self.product_name_combo.set(product_names[0])
                    self.on_product_name_selected(product_names[0])
                else:
                    self.product_name_combo.set('Select Product')
                
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            if category == 'Glasses':
                if hasattr(self, 'glasses_product_combo') and self.glasses_product_combo.winfo_exists():
                    self.glasses_product_combo.configure(values=['Error loading products'])
                    self.glasses_product_combo.set('Error loading products')
            else:
                if hasattr(self, 'product_name_combo') and self.product_name_combo.winfo_exists():
                    self.product_name_combo.configure(values=['Error loading products'])
                    self.product_name_combo.set('Error loading products')
    
    def on_product_name_selected(self, choice=None):
        try:
            if not choice or choice in ['Select Product', 'No products available', 'Error loading products']:
                return
            
            if not hasattr(self, 'product_description') or not self.product_description.winfo_exists():
                return
            
            product = self.product_map.get(choice)
            if product:
                category = product.get('Category', '')
                supplier = product.get('Supplier', '')
                desc = f"{category} - {supplier}" if supplier else category
                self.product_description.configure(state='normal')
                self.product_description.delete(0, 'end')
                self.product_description.insert(0, desc)
                self.product_description.configure(state='readonly')
                
                price = product.get('Unit_Price', 0)
                self.product_price.delete(0, 'end')
                self.product_price.insert(0, str(price))
        except Exception as e:
            # Silently ignore if widgets are destroyed
            pass
    
    def on_glasses_product_selected(self, choice=None):
        try:
            if not choice or choice in ['Select from inventory or enter manually', 'No products available', 'Error loading products']:
                return
            
            if not hasattr(self, 'product_price') or not self.product_price.winfo_exists():
                return
            
            product = self.product_map.get(choice)
            if product:
                price = product.get('Unit_Price', 0)
                self.product_price.delete(0, 'end')
                self.product_price.insert(0, str(price))
        except Exception as e:
            # Silently ignore if widgets are destroyed
            pass

    def add_product_to_sales(self):
        try:
            if not hasattr(self, 'sales_patient_info_obj') or not self.sales_patient_info_obj:
                self.show_error('Error', 'Please select a patient first')
                return
            
            category = self.product_category.get()
            quantity_str = self.product_quantity.get().strip()
            price_str = self.product_price.get().strip()
            
            if not quantity_str or not price_str:
                self.show_error('Error', 'Please enter quantity and price')
                return
            
            try:
                quantity = int(quantity_str)
                price = float(price_str)
            except ValueError:
                self.show_error('Error', 'Quantity must be a number and price must be numeric')
                return
            
            if category == 'Glasses':
                selected_glasses = self.glasses_product_combo.get()
                if selected_glasses and selected_glasses not in ['Select from inventory or enter manually', 'No products available', 'Error loading products']:
                    product_name = selected_glasses.split(' (₱')[0]
                else:
                    frame_type = self.frame_type.get()
                    lens_type = self.lens_type.get()
                    coating = self.lens_coating.get()
                    
                    if not all([frame_type, lens_type, coating]):
                        self.show_error('Error', 'Please select all glasses options or choose a product from inventory')
                        return
                    
                    product_name = f"{frame_type} - {lens_type} ({coating})"
            else:
                selected_product = self.product_name_combo.get()
                
                if not selected_product or selected_product in ['Select Product', 'No products available', 'Error loading products']:
                    self.show_error('Error', 'Please select a product')
                    return
                
                product_name = selected_product.split(' (₱')[0]
            
            try:
                patient_name = f"{self.sales_patient_info_obj['Surname']}, {self.sales_patient_info_obj['FirstName']}"
                total_price = price * quantity
                
                sale_query = "INSERT INTO sales (customer_name, total, sale_date) VALUES (%s, %s, NOW())"
                sale_id = self.sm.db.execute(sale_query, (patient_name, total_price))
                
                item_query = "INSERT INTO sales_products (name, category, description, price, quantity) VALUES (%s, %s, %s, %s, %s)"
                self.sm.db.execute(item_query, (product_name, category, f"Sale #{sale_id} - {patient_name}", price, quantity))

                # --- Add to billing automatically ---
                if hasattr(self, 'billing_patient_info_obj') and self.billing_patient_info_obj:
                    billing_patient_id = self.billing_patient_info_obj['Patient_ID']
                else:
                    # Try to get patient ID from sales_patient_info_obj
                    billing_patient_id = self.sales_patient_info_obj.get('Patient_ID')
                if billing_patient_id:
                    self.bm.add_billing(
                        patient_id=billing_patient_id,
                        amount=total_price,
                        service=f"{product_name} (Sales)",
                        method='Sales',
                        status='Pending'
                    )
                    if hasattr(self, 'bill_textbox'):
                        self.refresh_billing_summary()

                self.show_success('Success', f'Sale recorded successfully!\n\n{product_name}\nQty: {quantity} × ₱{price:.2f} = ₱{total_price:.2f}\n\nSale ID: #{sale_id}')
                
            except Exception as e:
                logger.error(f"Error recording sale: {e}")
                self.show_error('Error', f'Failed to record sale: {str(e)}')
                return
            
            if category == 'Glasses':
                self.glasses_product_combo.set('Select from inventory or enter manually')
                self.frame_type.set('')
                self.lens_type.set('')
                self.lens_coating.set('')
            
            self.product_quantity.delete(0, 'end')
            self.product_quantity.insert(0, '1')
            self.product_price.delete(0, 'end')
            
            # Refresh sales summary
            self.refresh_sales_summary()
            
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            self.show_error('Error', str(e))

    def add_glasses_to_sales(self):
        try:
            if not hasattr(self, 'sales_patient_info_obj'):
                self.show_error('Error', 'Please select a patient first')
                return
            
            frame_type = self.frame_type.get()
            lens_type = self.lens_type.get()
            coating = self.lens_coating.get()
            price = self.product_price.get().strip()
            
            if not all([frame_type, lens_type, coating, price]):
                self.show_error('Error', 'Please fill all fields')
                return
            
            price_float = float(price)
            desc = f"{frame_type} - {lens_type} ({coating})"
            
            try:
                self.sm.add_product(desc, 'Eyeglasses', f"Sold to {self.sales_patient_info_obj['Surname']}", price_float, 1)
            except:
                pass
            
            self.show_success('Success', f'Added to sale:\n{desc}\n₱{price_float:.2f}')
            
            self.frame_type.set('')
            self.lens_type.set('')
            self.lens_coating.set('')
            self.product_price.delete(0, 'end')
            
            # Refresh sales summary
            self.refresh_sales_summary()
            
        except Exception as e:
            logger.error(f"Error adding glasses: {e}")
            self.show_error('Error', str(e))

    def refresh_sales_summary(self):
        self.sales_summary_textbox.delete('1.0', 'end')
        try:
            if not hasattr(self, 'sales_patient_info_obj') or not self.sales_patient_info_obj:
                self.sales_summary_textbox.insert('end', 'Please select a patient to view their sales.')
                return
            
            all_sales = self.sm.get_all_sales()
            patient_name = f"{self.sales_patient_info_obj['Surname']}, {self.sales_patient_info_obj['FirstName']}"
            
            if not all_sales:
                self.sales_summary_textbox.insert('end', 'No sales records yet.')
                return
            
            patient_sales = [s for s in all_sales if s.get('customer_name') == patient_name]
            
            if not patient_sales:
                self.sales_summary_textbox.insert('end', f'No sales for {patient_name}')
                return
            
            sales_text = "SALES SUMMARY:\n" + "="*40 + "\n"
            total = 0
            for sale in patient_sales:
                amount = float(sale.get('total', 0))
                total += amount
                date = sale.get('sale_date', 'N/A')
                sales_text += f"Sale #{sale.get('id', '?'):<10} ₱{amount:>8.2f} ({date})\n"
            
            sales_text += "-"*40 + "\n"
            sales_text += f"{'TOTAL':<20} ₱{total:>8.2f}\n"
            self.sales_summary_textbox.insert('end', sales_text)
            
        except Exception as e:
            logger.error(f"Error loading sales summary: {e}")
            self.sales_summary_textbox.insert('end', f"Error loading sales: {str(e)}")

    def complete_sales_visit(self):
        try:
            if not hasattr(self, 'sales_patient_info_obj'):
                self.show_error('Error', 'Please select a patient first')
                return
            
            patient_name = f"{self.sales_patient_info_obj['Surname']}, {self.sales_patient_info_obj['FirstName']}"
            
            self.show_success('Visit Completed', f'Sales visit for {patient_name} completed successfully!\n\nPatient can now proceed to checkout.')
            
            self.sales_patient.set('')
            self.sales_patient_info.configure(text='')
            self.frame_type.set('')
            self.lens_type.set('')
            self.lens_coating.set('')
            self.product_price.delete(0, 'end')
            self.refresh_sales_summary()
            
        except Exception as e:
            logger.error(f"Error completing sales visit: {e}")
            self.show_error('Error', str(e))

    def complete_visit(self):
        try:
            patient_name = f"{self.current_patient['Surname']}, {self.current_patient['FirstName']}"
            
            completion_msg = f"""
VISIT COMPLETED SUCCESSFULLY!

Patient: {patient_name}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

✓ Eye examination performed
✓ Vision tested (Snellen chart)
✓ Prescription issued
✓ Bill calculated
✓ Glasses selected
✓ Follow-up appointment scheduled

NEXT STEPS:
• Patient to pick up glasses in 3-5 days
• Send appointment reminder 2 days before follow-up
• Recommend yearly check-ups

Thank you for visiting!
            """
            
            self.show_success('Visit Completed', completion_msg)
            
            self.current_patient = None
            self.current_step = 0
            self.show_step(0)
            
        except Exception as e:
            logger.error(f"Error completing visit: {e}")
            self.show_error('Error', str(e))