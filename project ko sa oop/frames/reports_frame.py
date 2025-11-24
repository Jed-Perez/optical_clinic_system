import customtkinter as ctk
from tkinter import messagebox

class ReportsFrame(ctk.CTkFrame):
    def __init__(self, master, managers, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.managers = managers
        self.build()

    def build(self):
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='📊 Reports', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)

        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)

        main = ctk.CTkFrame(self)
        main.pack(fill='both', expand=True, padx=15, pady=15)
        
        report_selection_frame = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        report_selection_frame.pack(fill='x', pady=(0, 15), padx=0)

        ctk.CTkLabel(report_selection_frame, text="📈 Select Report:", font=('Segoe UI', 14, 'bold')).pack(side='left', padx=15, pady=15)

        self.report_combo = ctk.CTkComboBox(report_selection_frame, values=["Sales Report", "Patient Demographics"], command=self.generate_report, height=38, font=('Segoe UI', 12))
        self.report_combo.set("Select a report to generate")
        self.report_combo.pack(side='left', fill='x', expand=True, padx=15, pady=15)

        ctk.CTkButton(report_selection_frame, text="🔄 Refresh", command=lambda: self.generate_report(self.report_combo.get()), height=38, font=('Segoe UI', 12, 'bold')).pack(side='left', padx=(0, 15), pady=15)

        display_frame = ctk.CTkFrame(main, fg_color=("white", "#0f0f0f"))
        display_frame.pack(fill='both', expand=True, padx=0, pady=0)

        ctk.CTkLabel(display_frame, text="📋 Report Output", font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=15, pady=(15, 10))

        self.txt = ctk.CTkTextbox(display_frame, font=('Consolas', 11), fg_color=("#f5f5f5", "#1a1a1a"), text_color=("black", "white"))
        self.txt.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def generate_report(self, report_name):
        self.txt.delete('1.0', 'end')
        try:
            if report_name == "Sales Report":
                report_data = self.managers['sm'].get_sales_report()
                self.txt.insert('end', "--- Sales Report by Category ---\n\n")
                header = f"{'Category':<20} {'Items Sold':<15} {'Total Quantity':<15} {'Avg Price (₱)':<15}\n"
                self.txt.insert('end', header)
                self.txt.insert('end', "="*70 + "\n")
                if not report_data:
                    self.txt.insert('end', "No sales data available.")
                    return
                for row in report_data:
                    self.txt.insert('end', f"{row['category']:<20} {row['count']:<15} {row['total_qty']:<15} {row['avg_price']:<15.2f}\n")

            elif report_name == "Patient Demographics":
                patients = self.managers['pm'].list_patients()
                self.txt.insert('end', "--- Patient Demographics Report ---\n\n")
                self.txt.insert('end', f"Total Patients: {len(patients)}\n\n")

            else:
                self.txt.insert('end', "Please select a valid report.")

        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to generate report: {e}")
            self.txt.insert('end', f"Error: {e}")