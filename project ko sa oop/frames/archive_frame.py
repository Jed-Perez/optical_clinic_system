import customtkinter as ctk
from tkinter import messagebox
from utils.alert_system import AlertSystem

class ArchiveFrame(ctk.CTkFrame):
    def __init__(self, master, managers, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pm = managers['pm']; self.dm = managers['dm']; self.am = managers['am']; self.im = managers['im']
        self.build()
    def build(self):
        ctk.CTkLabel(self, text='🗑️ Archive / Recycle Bin', font=('Segoe UI', 26, 'bold')).pack(pady=8)
        frm=ctk.CTkFrame(self); frm.pack(padx=6, pady=6)

        ctk.CTkLabel(frm, text='Category', font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, padx=5, pady=5)
        self.category_combo = ctk.CTkComboBox(frm, values=['Patient', 'Doctor', 'Appointment', 'Inventory Item'], state='readonly', height=32, font=('Segoe UI', 11), command=self.on_category_changed)
        self.category_combo.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(frm, text='Select to Restore', font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, padx=5, pady=5)
        self.item_combo = ctk.CTkComboBox(frm, values=[], state='readonly', height=32, font=('Segoe UI', 11))
        self.item_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        
        restore = ctk.CTkButton(frm, text='🔄 Restore', command=self.restore, height=35, font=('Segoe UI', 11, 'bold'), fg_color=("#f39c12", "#d68910"))
        restore.grid(row=2, column=0, columnspan=2, pady=10)
        
        frm.columnconfigure(1, weight=1)
        
        self.txt=ctk.CTkTextbox(self, width=900, height=350, font=('Consolas', 11)); self.txt.pack(padx=6, pady=6)
        self.refresh()
        self.on_category_changed()
    def refresh(self):
        self.txt.delete('1.0','end')
        self.txt.insert('end','Archived Patients:\n')
        for r in self.pm.list_archived(): self.txt.insert('end', f"{r['Patient_ID']} | {r['Name']} | Deleted: {r['Deleted_On']}\n")
        self.txt.insert('end','\nArchived Doctors:\n')
        for r in self.dm.list_archived(): self.txt.insert('end', f"{r['Doctor_ID']} | {r['Name']} | Deleted: {r['Deleted_On']}\n")
        self.txt.insert('end','\nArchived Appointments:\n')
        for r in self.am.list_archived(): self.txt.insert('end', f"{r.get('Appointment_ID')} | P:{r.get('Patient_ID')} D:{r.get('Doctor_ID')} Deleted: {r.get('Deleted_On')}\n")
        self.txt.insert('end','\nArchived Inventory:\n')
        for r in self.im.list_archived(): self.txt.insert('end', f"{r['Item_ID']} | {r['Item_Name']} | Deleted: {r['Deleted_On']}\n")
    
    def on_category_changed(self, *args):
        category = self.category_combo.get()
        items = []
        
        try:
            if category == 'Patient':
                archived = self.pm.list_archived()
                items = [f"{r['Patient_ID']}: {r['Name']}" for r in archived]
            elif category == 'Doctor':
                archived = self.dm.list_archived()
                items = [f"{r['Doctor_ID']}: {r['Name']}" for r in archived]
            elif category == 'Appointment':
                archived = self.am.list_archived()
                items = [f"{r.get('Appointment_ID')}: Patient {r.get('Patient_ID')} - Doctor {r.get('Doctor_ID')} on {r.get('Appointment_Date', 'N/A')}" for r in archived]
            elif category == 'Inventory Item':
                archived = self.im.list_archived()
                items = [f"{r['Item_ID']}: {r['Item_Name']}" for r in archived]
        except:
            items = ['Error loading items']
        
        if not items:
            items = ['No archived items found']
        
        self.item_combo.configure(values=items)
        if items and 'No archived' not in items[0] and 'Error' not in items[0]:
            self.item_combo.set(items[0])
        else:
            self.item_combo.set(items[0])
    
    def restore(self):
        category = self.category_combo.get()
        selection = self.item_combo.get().strip()
        
        if not selection or 'No archived' in selection or 'Error' in selection:
            AlertSystem.error('Validation Error', 'Please select an item to restore')
            return
        
        item_id = selection.split(':')[0].strip()
        
        if not AlertSystem.confirm('Restore Record', f"Restore {category} with ID {item_id}?"):
            return
        
        try:
            if category == 'Patient':
                self.pm.restore(item_id)
                AlertSystem.success('Success', 'Patient restored')
            elif category == 'Doctor':
                self.dm.restore(item_id)
                AlertSystem.success('Success', 'Doctor restored')
            elif category == 'Appointment':
                self.am.restore(item_id)
                AlertSystem.success('Success', 'Appointment restored')
            elif category == 'Inventory Item':
                self.im.restore(item_id)
                AlertSystem.success('Success', 'Item restored')
            else:
                AlertSystem.error('Error', 'Please select a category')
                return
            
            self.refresh()
            self.on_category_changed()
        except Exception as e:
            AlertSystem.error('Error', str(e))
