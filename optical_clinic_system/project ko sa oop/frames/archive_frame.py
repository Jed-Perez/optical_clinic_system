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
        # simple restore inputs
        ctk.CTkLabel(frm, text='Type', font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, padx=5, pady=5)
        self.type_entry = ctk.CTkEntry(frm, placeholder_text='patient/doctor/appointment/item', height=32, font=('Segoe UI', 11)); self.type_entry.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(frm, text='ID', font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, padx=5, pady=5)
        self.id_entry = ctk.CTkEntry(frm, placeholder_text='ID', height=32, font=('Segoe UI', 11)); self.id_entry.grid(row=1, column=1, padx=5, pady=5)
        restore = ctk.CTkButton(frm, text='🔄 Restore', command=self.restore, height=35, font=('Segoe UI', 11, 'bold'), fg_color=("#f39c12", "#d68910")); restore.grid(row=2, column=0, columnspan=2, pady=10)
        self.txt=ctk.CTkTextbox(self, width=900, height=350, font=('Consolas', 11)); self.txt.pack(padx=6, pady=6)
        self.refresh()
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
    def restore(self):
        t = self.type_entry.get().strip().lower(); idv = self.id_entry.get().strip()
        if not t or not idv:
            AlertSystem.error('Validation Error', 'Please enter both type and ID')
            return
        
        # Confirmation
        if not AlertSystem.confirm('Restore Record', f"Restore {t} with ID {idv}?"):
            return
        
        try:
            if t=='patient':
                self.pm.restore(idv); AlertSystem.success('Success', 'Patient restored')
            elif t=='doctor':
                self.dm.restore(idv); AlertSystem.success('Success', 'Doctor restored')
            elif t in ('appointment','appt'):
                self.am.restore(idv); AlertSystem.success('Success', 'Appointment restored')
            elif t in ('item','inventory'):
                self.im.restore(idv); AlertSystem.success('Success', 'Item restored')
            else:
                AlertSystem.error('Error', 'Unknown type. Use: patient, doctor, appointment, or item')
                return
            self.type_entry.delete(0, 'end')
            self.id_entry.delete(0, 'end')
            self.refresh()
        except Exception as e:
            AlertSystem.error('Error', str(e))
