import customtkinter as ctk
from tkinter import messagebox

class ProceduresFrame(ctk.CTkFrame):
    def __init__(self, master, procedure_manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.proc_m = procedure_manager
        self.build()

    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='⚕️ Clinic Procedures', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)
        
        # Separator
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)
        
        # Main container
        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Left panel
        left = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        left.pack(side='left', fill='both', expand=False, padx=0, pady=0)
        
        form_title = ctk.CTkLabel(left, text='Add Procedure', font=('Segoe UI', 16, 'bold'))
        form_title.pack(pady=15, padx=20)
        
        frm = ctk.CTkFrame(left, fg_color=("transparent"))
        frm.pack(padx=20, pady=10, fill='x')
        
        ctk.CTkLabel(frm, text='Procedure Name', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.name_entry = ctk.CTkEntry(frm, placeholder_text='Procedure Name', height=35, font=('Segoe UI', 12))
        self.name_entry.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Description', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.desc_entry = ctk.CTkEntry(frm, placeholder_text='Description', height=35, font=('Segoe UI', 12))
        self.desc_entry.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Price (₱)', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.price_entry = ctk.CTkEntry(frm, placeholder_text='Default Price', height=35, font=('Segoe UI', 12))
        self.price_entry.pack(fill='x', pady=(0, 20))
        
        btn_frm = ctk.CTkFrame(frm, fg_color=("transparent"))
        btn_frm.pack(fill='x', pady=10)
        
        ctk.CTkButton(btn_frm, text='➕ Add Procedure', command=self.add_procedure, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#27ae60", "#1e8449")).pack(fill='x', pady=5)
        ctk.CTkButton(btn_frm, text='🔄 Refresh', command=self.refresh_list, height=40, font=('Segoe UI', 12, 'bold')).pack(fill='x', pady=5)
        
        # Right panel
        right = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        right.pack(side='right', fill='both', expand=True, padx=15, pady=15)
        
        display_title = ctk.CTkLabel(right, text='Available Procedures', font=('Segoe UI', 16, 'bold'))
        display_title.pack(pady=(0, 10))
        
        self.listbox = ctk.CTkTextbox(right, font=('Consolas', 11), fg_color=("#f5f5f5", "#1a1a1a"))
        self.listbox.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.refresh_list()

    def add_procedure(self):
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        price = self.price_entry.get().strip()
        if not name or not price:
            messagebox.showwarning("Missing Info", "Please fill all fields.")
            return
        try:
            self.proc_m.add_procedure(name, desc, float(price))
            messagebox.showinfo("Success", "Procedure added successfully.")
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_list(self):
        data = self.proc_m.get_all_procedures()
        self.listbox.delete("1.0", "end")
        if not data:
            return
        for d in data:
            pid = d.get('Procedure_ID') or d.get('id') or d.get('ID') or '?'
            pname = d.get('Procedure_Name') or d.get('name') or d.get('Name') or 'Unnamed'
            pprice = d.get('Default_Price') or d.get('price') or d.get('Price') or ''
            self.listbox.insert("end", f"{pid}: {pname} - ₱{pprice}\n")
