import customtkinter as ctk

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, managers, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.managers = managers
        self.build()
        self.refresh_stats()

    def build(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=("white", "#1a1a1a"))
        header.pack(fill='x', padx=0, pady=0)
        ctk.CTkLabel(header, text='🏠 Dashboard', font=('Segoe UI', 26, 'bold')).pack(side='left', padx=20, pady=15)
        
        refresh_btn = ctk.CTkButton(header, text='🔄 Refresh', command=self.refresh_stats, height=32, font=('Segoe UI', 11, 'bold'))
        refresh_btn.pack(side='right', padx=20, pady=15)

        # Separator
        ctk.CTkLabel(self, text="", fg_color=("gray80", "gray30"), height=1).pack(fill='x', padx=0, pady=0)

        # Stats container
        stats_container = ctk.CTkFrame(self, fg_color=("transparent"))
        stats_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Grid layout for stats
        stats_container.grid_columnconfigure((0, 1, 2), weight=1)
        stats_container.grid_rowconfigure((0, 1), weight=1)

        # Stat cards
        self.patient_card = self.create_stat_card(stats_container, "Today's Patients", "0", "👥")
        self.patient_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.doctor_card = self.create_stat_card(stats_container, "Total Doctors", "0", "🩺")
        self.doctor_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.appointment_card = self.create_stat_card(stats_container, "Total Appointments", "0", "📅")
        self.appointment_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.sales_card = self.create_stat_card(stats_container, "Total Sales", "0", "🛒")
        self.sales_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.inventory_card = self.create_stat_card(stats_container, "Inventory Items", "0", "📦")
        self.inventory_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.reminders_card = self.create_stat_card(stats_container, "Pending Reminders", "0", "🔔")
        self.reminders_card.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")


    def create_stat_card(self, parent, title, initial_value, icon):
        card = ctk.CTkFrame(parent, fg_color=("#f0f0f0", "#1a1a1a"), corner_radius=10)
        
        icon_label = ctk.CTkLabel(card, text=icon, font=('Segoe UI Emoji', 40))
        icon_label.pack(pady=(20, 10))
        
        title_label = ctk.CTkLabel(card, text=title, font=('Segoe UI', 14, 'bold'))
        title_label.pack(pady=(0, 5))
        
        value_label = ctk.CTkLabel(card, text=initial_value, font=('Segoe UI', 32, 'bold'))
        value_label.pack(pady=(0, 20))
        
        card.value_label = value_label 
        return card

    def refresh_stats(self):
        try:
            # Patients registered today
            patients_today = self.managers['pm'].count_patients_today()
            self.patient_card.value_label.configure(text=str(patients_today))

            # Total doctors
            doctors_count = len(self.managers['dm'].list_doctors())
            self.doctor_card.value_label.configure(text=str(doctors_count))

            # Total appointments
            appointments_count = len(self.managers['am'].list_appointments())
            self.appointment_card.value_label.configure(text=str(appointments_count))

            # Total sales
            sales = self.managers['sm'].get_all_sales()
            sales_count = len(sales) if sales else 0
            self.sales_card.value_label.configure(text=str(sales_count))

            # Total inventory items
            inventory_count = len(self.managers['im'].list_items())
            self.inventory_card.value_label.configure(text=str(inventory_count))

            # Pending reminders
            reminders_count = len(self.managers['rem_m'].get_pending_reminders())
            self.reminders_card.value_label.configure(text=str(reminders_count))

        except Exception as e:
            print(f"Error refreshing dashboard stats: {e}")
            # Optionally show an error on the dashboard itself
            error_label = ctk.CTkLabel(self, text=f"Failed to load stats: {e}", text_color="red")
            error_label.pack()

    def pack(self, *args, **kwargs):
        self.refresh_stats()
        super().pack(*args, **kwargs)