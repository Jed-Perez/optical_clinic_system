import customtkinter as ctk
from tkinter import messagebox

class BillingFrame(ctk.CTkFrame):
    def __init__(self, master, manager, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.manager = manager
        self.build()
    
    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='💳 Billing Management', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)
        
        # Separator
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)
        
        # Main container
        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Left panel
        left = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"), width=300)
        left.pack(side='left', fill='both', expand=False, padx=0, pady=0)
        left.pack_propagate(False)
        
        form_title = ctk.CTkLabel(left, text='Create Bill', font=('Segoe UI', 16, 'bold'))
        form_title.pack(pady=15, padx=20)
        
        # Create scrollable frame for form
        scroll_frame = ctk.CTkScrollableFrame(left, fg_color=("transparent"))
        scroll_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        frm = ctk.CTkFrame(scroll_frame, fg_color=("transparent"))
        frm.pack(padx=20, pady=10, fill='x')
        
        ctk.CTkLabel(frm, text='Patient ID', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.pid = ctk.CTkEntry(frm, placeholder_text='Patient ID', height=35, font=('Segoe UI', 12))
        self.pid.pack(fill='x', pady=(0, 10))
        
        ctk.CTkLabel(frm, text='Amount (₱)', font=('Segoe UI', 12, 'bold')).pack(anchor='w', pady=(10, 3))
        self.amount = ctk.CTkEntry(frm, placeholder_text='Enter amount', height=35, font=('Segoe UI', 12))
        self.amount.pack(fill='x', pady=(0, 20))
        
        btn_frm = ctk.CTkFrame(frm, fg_color=("transparent"))
        btn_frm.pack(fill='x', pady=10)
        
        ctk.CTkButton(btn_frm, text='💸 Create Bill', command=self.create, height=40, font=('Segoe UI', 12, 'bold'), fg_color=("#27ae60", "#1e8449")).pack(fill='x', pady=5)
        ctk.CTkButton(btn_frm, text='👁️ View Bills', command=self.view, height=40, font=('Segoe UI', 12, 'bold')).pack(fill='x', pady=5)
        
        # Right panel
        right = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        right.pack(side='right', fill='both', expand=True, padx=15, pady=15)
        
        display_title = ctk.CTkLabel(right, text='Bills List', font=('Segoe UI', 16, 'bold'))
        display_title.pack(pady=(0, 10))
        
        self.txt = ctk.CTkTextbox(right, font=('Consolas', 13), fg_color=("#f5f5f5", "#1a1a1a"))
        self.txt.pack(fill='both', expand=True, padx=0, pady=0)
    def create(self):
        try:
            pid = self.pid.get().strip()
            amount_str = self.amount.get().strip()
            
            if not pid:
                messagebox.showerror('Validation Error', 'Patient ID is required')
                return
            if not amount_str:
                messagebox.showerror('Validation Error', 'Amount is required')
                return
            
            try:
                amt = float(amount_str)
            except ValueError:
                messagebox.showerror('Invalid','Amount must be numeric')
                return
            
            self.manager.create_bill(pid, amt, 'Cash')
            messagebox.showinfo('OK','Bill created')
            self.view()
        except Exception as e:
            messagebox.showerror('Error', str(e))
    def view(self):
        rows=self.manager.list_bills(); self.txt.delete('1.0','end')
        for r in rows: self.txt.insert('end', f"{r['Bill_ID']} | P:{r['Patient_ID']} | {r['Amount']} | {r['Status']}\n")
