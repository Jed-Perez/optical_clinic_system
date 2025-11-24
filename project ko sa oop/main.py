import customtkinter as ctk
from database.db_connection import Database
from backend.managers import PatientManager, DoctorManager, AppointmentManager, InventoryManager, BillingManager, UserManager, ProcedureManager, SalesManager, PrescriptionManager, MedicalRecordsManager, ReminderManager, InvoiceManager
from frames.dashboard_frame import DashboardFrame
from frames.doctors_frame import DoctorsFrame
from frames.medical_records_frame import MedicalRecordsFrame
from frames.reports_frame import ReportsFrame
from frames.archive_frame import ArchiveFrame
from frames.sales_frame import SalesFrame
from frames.inventory_frame import InventoryFrame
from frames.followup_frame import FollowUpFrame
from frames.workflow_frame import WorkflowFrame
from frames.appointments_frame import AppointmentsFrame
from utils.alert_system import AlertSystem
from utils.password_manager import PasswordManager
from utils.logger import setup_logging
from utils.constants import *
from tkinter import messagebox

logger = setup_logging(__name__)

ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(COLOR_THEME)

class LoginWindow(ctk.CTk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.user_manager = UserManager(db)
        self.title(LOGIN_WINDOW_TITLE)
        self.geometry(LOGIN_GEOMETRY)
        self.user_data = None
        self.build()

    def build(self):
        ctk.CTkLabel(self, text='Optical Clinic', font=('Segoe UI', 24, 'bold')).pack(pady=12)
        frm = ctk.CTkFrame(self); frm.pack(pady=10, padx=10)
        ctk.CTkLabel(frm, text='Username', font=('Segoe UI', 12)).grid(row=0, column=0, padx=10, pady=8)
        self.user_entry = ctk.CTkEntry(frm, font=('Segoe UI', 12)); self.user_entry.grid(row=0, column=1, padx=10, pady=8)
        ctk.CTkLabel(frm, text='Password', font=('Segoe UI', 12)).grid(row=1, column=0, padx=10, pady=8)
        self.pw_entry = ctk.CTkEntry(frm, font=('Segoe UI', 12), show='*'); self.pw_entry.grid(row=1, column=1, padx=10, pady=8)
        ctk.CTkButton(self, text='Login', command=self.try_login, font=('Segoe UI', 12, 'bold')).pack(pady=12)

    def try_login(self):
        u = self.user_manager.verify_user(self.user_entry.get().strip(), self.pw_entry.get())
        if not u:
            logger.warning(f"Failed login attempt with username: {self.user_entry.get().strip()}")
            messagebox.showerror('Login failed', ERROR_INVALID_CREDENTIALS)
            return
        
        self.user_data = u
        self.destroy() 

def ensure_sample_data(db):
    """
    Ensures that all necessary tables and some sample data exist in the database.
    This function is idempotent and can be run safely multiple times.
    """
    
    tables = {
        'patients': """
            CREATE TABLE `patients` (
              `Patient_ID` int NOT NULL AUTO_INCREMENT,
              `Surname` varchar(100) NOT NULL,
              `FirstName` varchar(100) NOT NULL,
              `MiddleInitial` varchar(10) DEFAULT NULL,
              `Age` int DEFAULT NULL,
              `Gender` varchar(10) NOT NULL,
              `Age_Group` varchar(20) NOT NULL,
              `Address` text,
              `Contact` varchar(20) NOT NULL,
              `Email` varchar(100) DEFAULT NULL,
              `Medical_History` text,
              `Registration_Date` date DEFAULT (curdate()),
              PRIMARY KEY (`Patient_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'archived_patients': """
            CREATE TABLE `archived_patients` (
              `Patient_ID` int NOT NULL,
              `Surname` varchar(100) NOT NULL,
              `FirstName` varchar(100) NOT NULL,
              `MiddleInitial` varchar(10) DEFAULT NULL,
              `Age` int DEFAULT NULL,
              `Gender` varchar(10) NOT NULL,
              `Age_Group` varchar(20) NOT NULL,
              `Address` text,
              `Contact` varchar(20) NOT NULL,
              `Email` varchar(100) DEFAULT NULL,
              `Medical_History` text,
              `Deleted_On` datetime NOT NULL,
              PRIMARY KEY (`Patient_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'doctors': """
            CREATE TABLE `doctors` (
              `Doctor_ID` int NOT NULL AUTO_INCREMENT,
              `Surname` varchar(100) NOT NULL,
              `FirstName` varchar(100) NOT NULL,
              `MiddleInitial` varchar(10) DEFAULT NULL,
              `Name` varchar(255) NOT NULL,
              `License_No` varchar(50) NOT NULL,
              `Specialization` varchar(100) NOT NULL,
              `Contact` varchar(20) DEFAULT NULL,
              `Schedule` varchar(255) DEFAULT NULL,
              PRIMARY KEY (`Doctor_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'archived_doctors': """
            CREATE TABLE `archived_doctors` (
              `Doctor_ID` int NOT NULL,
              `Surname` varchar(100) NOT NULL,
              `FirstName` varchar(100) NOT NULL,
              `MiddleInitial` varchar(10) DEFAULT NULL,
              `Name` varchar(255) NOT NULL,
              `License_No` varchar(50) NOT NULL,
              `Specialization` varchar(100) NOT NULL,
              `Contact` varchar(20) DEFAULT NULL,
              `Schedule` varchar(255) DEFAULT NULL,
              `Deleted_On` datetime NOT NULL,
              PRIMARY KEY (`Doctor_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'appointments': """
            CREATE TABLE `appointments` (
              `Appointment_ID` int NOT NULL AUTO_INCREMENT,
              `Patient_ID` int NOT NULL,
              `Doctor_ID` int NOT NULL,
              `Appointment_Date` date NOT NULL,
              `Appointment_Time` time NOT NULL,
              `Status` varchar(20) NOT NULL,
              PRIMARY KEY (`Appointment_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'archived_appointments': """
            CREATE TABLE `archived_appointments` (
              `Appointment_ID` int NOT NULL,
              `Patient_ID` int NOT NULL,
              `Doctor_ID` int NOT NULL,
              `Appointment_Date` date NOT NULL,
              `Appointment_Time` time NOT NULL,
              `Status` varchar(20) NOT NULL,
              `Deleted_On` datetime NOT NULL,
              PRIMARY KEY (`Appointment_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'inventory': """
            CREATE TABLE `inventory` (
              `Inventory_ID` int NOT NULL AUTO_INCREMENT,
              `Item_Name` varchar(100) NOT NULL,
              `Category` varchar(50) NOT NULL,
              `Quantity_On_Hand` int NOT NULL,
              `Unit_Price` decimal(10,2) DEFAULT NULL,
              `Supplier` varchar(100) DEFAULT NULL,
              PRIMARY KEY (`Inventory_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'archived_inventory': """
            CREATE TABLE `archived_inventory` (
              `Inventory_ID` int NOT NULL,
              `Item_Name` varchar(100) NOT NULL,
              `Category` varchar(50) NOT NULL,
              `Quantity_On_Hand` int NOT NULL,
              `Unit_Price` decimal(10,2) DEFAULT NULL,
              `Supplier` varchar(100) DEFAULT NULL,
              `Deleted_On` datetime NOT NULL,
              PRIMARY KEY (`Inventory_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'billing': """
            CREATE TABLE `billing` (
              `Bill_ID` int NOT NULL AUTO_INCREMENT,
              `Patient_ID` int NOT NULL,
              `Amount` decimal(10,2) NOT NULL,
              `Billing_Date` date DEFAULT (curdate()),
              `Payment_Method` varchar(50) DEFAULT NULL,
              `Status` varchar(20) NOT NULL,
              PRIMARY KEY (`Bill_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'users': """
            CREATE TABLE `users` (
              `User_ID` int NOT NULL AUTO_INCREMENT,
              `Username` varchar(50) NOT NULL,
              `Password` varchar(255) NOT NULL,
              `Role` varchar(20) NOT NULL,
              PRIMARY KEY (`User_ID`),
              UNIQUE KEY `Username` (`Username`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'procedures': """
            CREATE TABLE `procedures` (
              `Procedure_ID` int NOT NULL AUTO_INCREMENT,
              `Name` varchar(100) NOT NULL,
              `Description` text,
              `Cost` decimal(10,2) NOT NULL,
              PRIMARY KEY (`Procedure_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'sales_products': """
            CREATE TABLE `sales_products` (
              `id` int NOT NULL AUTO_INCREMENT,
              `name` varchar(100) NOT NULL,
              `category` varchar(50) NOT NULL,
              `description` text,
              `price` decimal(10,2) NOT NULL,
              `quantity` int NOT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'sales': """
            CREATE TABLE `sales` (
              `id` int NOT NULL AUTO_INCREMENT,
              `customer_name` varchar(100) NOT NULL,
              `total` decimal(10,2) NOT NULL,
              `sale_date` datetime NOT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'sale_items': """
            CREATE TABLE `sale_items` (
              `id` int NOT NULL AUTO_INCREMENT,
              `sale_id` int NOT NULL,
              `product_id` int NOT NULL,
              `quantity` int NOT NULL,
              `price` decimal(10,2) NOT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'prescriptions': """
            CREATE TABLE `prescriptions` (
              `Prescription_ID` int NOT NULL AUTO_INCREMENT,
              `Patient_ID` int NOT NULL,
              `Doctor_ID` int NOT NULL,
              `Appointment_ID` int DEFAULT NULL,
              `Issued_Date` date NOT NULL,
              `Expiry_Date` date NOT NULL,
              `OD_Sphere` varchar(10) DEFAULT NULL,
              `OD_Cylinder` varchar(10) DEFAULT NULL,
              `OD_Axis` varchar(10) DEFAULT NULL,
              `OD_Add` varchar(10) DEFAULT NULL,
              `OS_Sphere` varchar(10) DEFAULT NULL,
              `OS_Cylinder` varchar(10) DEFAULT NULL,
              `OS_Axis` varchar(10) DEFAULT NULL,
              `OS_Add` varchar(10) DEFAULT NULL,
              `Notes` text,
              PRIMARY KEY (`Prescription_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'medical_records': """
            CREATE TABLE `medical_records` (
              `Record_ID` int NOT NULL AUTO_INCREMENT,
              `Patient_ID` int NOT NULL,
              `Doctor_ID` int NOT NULL,
              `Appointment_ID` int DEFAULT NULL,
              `Recorded_Date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
              `Diagnosis` varchar(255) DEFAULT NULL,
              `Severity` varchar(50) DEFAULT NULL,
              `Clinical_Notes` text,
              `Recommendations` text,
              `Follow_up_Days` int DEFAULT '90',
              PRIMARY KEY (`Record_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'appointment_reminders': """
            CREATE TABLE `appointment_reminders` (
              `Reminder_ID` int NOT NULL AUTO_INCREMENT,
              `Appointment_ID` int NOT NULL,
              `Patient_ID` int NOT NULL,
              `Reminder_Date` date NOT NULL,
              `Reminder_Time` time DEFAULT NULL,
              `Contact_Method` varchar(20) DEFAULT 'SMS',
              `Status` varchar(20) DEFAULT 'Pending',
              `Sent_Date` datetime DEFAULT NULL,
              PRIMARY KEY (`Reminder_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """,
        'invoices': """
            CREATE TABLE `invoices` (
              `Invoice_ID` int NOT NULL AUTO_INCREMENT,
              `Sale_ID` int DEFAULT NULL,
              `Patient_ID` int DEFAULT NULL,
              `Invoice_Number` varchar(50) NOT NULL,
              `Invoice_Date` date NOT NULL,
              `Total_Amount` decimal(10,2) NOT NULL,
              `Tax` decimal(10,2) NOT NULL,
              `Grand_Total` decimal(10,2) NOT NULL,
              `Status` varchar(20) DEFAULT 'Unpaid',
              `Generated_By` varchar(50) DEFAULT NULL,
              PRIMARY KEY (`Invoice_ID`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
        """
    }

    try:
        # Get existing tables
        existing_tables = {row['Tables_in_optical_clinic_db'] for row in db.fetch('SHOW TABLES')}
        
        # Create tables that don't exist
        for table_name, create_sql in tables.items():
            if table_name not in existing_tables:
                logger.info(f"Creating table: {table_name}...")
                db.execute(create_sql)
                logger.info(f"Table {table_name} created successfully.")

        # Check and add missing columns for existing tables
        # For patients table
        if 'patients' in existing_tables:
            columns = db.fetch("SHOW COLUMNS FROM patients")
            column_names = [col['Field'] for col in columns]
            if 'Surname' not in column_names:
                logger.info("Adding 'Surname' column to patients table...")
                db.execute("ALTER TABLE patients ADD COLUMN `Surname` varchar(100) NOT NULL DEFAULT ''")
                logger.info("'Surname' column added to patients table.")
            if 'FirstName' not in column_names:
                logger.info("Adding 'FirstName' column to patients table...")
                db.execute("ALTER TABLE patients ADD COLUMN `FirstName` varchar(100) NOT NULL DEFAULT ''")
                logger.info("'FirstName' column added to patients table.")
            if 'MiddleInitial' not in column_names:
                logger.info("Adding 'MiddleInitial' column to patients table...")
                db.execute("ALTER TABLE patients ADD COLUMN `MiddleInitial` varchar(10) DEFAULT NULL")
                logger.info("'MiddleInitial' column added to patients table.")
            if 'Registration_Date' not in column_names:
                logger.info("Adding 'Registration_Date' column to patients table...")
                db.execute("ALTER TABLE patients ADD COLUMN `Registration_Date` date DEFAULT (curdate())")
                logger.info("'Registration_Date' column added to patients table.")

            # Migrate data from old 'Name' column if it exists
            if 'Name' in column_names:
                logger.info("Migrating data from 'Name' column to new name fields...")
                patients = db.fetch("SELECT Patient_ID, Name FROM patients WHERE Name IS NOT NULL AND Name != ''")
                for patient in patients:
                    name = patient['Name'].strip()
                    # Assume format: "Surname, FirstName MiddleInitial" or "Surname, FirstName"
                    if ', ' in name:
                        surname_part, rest = name.split(', ', 1)
                        surname = surname_part.strip()
                        if ' ' in rest:
                            firstname, middleinitial = rest.split(' ', 1)
                            firstname = firstname.strip()
                            middleinitial = middleinitial.strip()
                        else:
                            firstname = rest.strip()
                            middleinitial = ''
                    else:
                        # Fallback: treat whole as surname if no comma
                        surname = name
                        firstname = ''
                        middleinitial = ''
                    db.execute("UPDATE patients SET Surname=%s, FirstName=%s, MiddleInitial=%s WHERE Patient_ID=%s",
                               (surname, firstname, middleinitial, patient['Patient_ID']))
                logger.info("Data migration completed. Dropping old 'Name' column...")
                db.execute("ALTER TABLE patients DROP COLUMN `Name`")
                logger.info("'Name' column dropped from patients table.")

        # For archived_patients table
        if 'archived_patients' in existing_tables:
            columns = db.fetch("SHOW COLUMNS FROM archived_patients")
            column_names = [col['Field'] for col in columns]
            if 'Surname' not in column_names:
                logger.info("Adding 'Surname' column to archived_patients table...")
                db.execute("ALTER TABLE archived_patients ADD COLUMN `Surname` varchar(100) NOT NULL DEFAULT ''")
                logger.info("'Surname' column added to archived_patients table.")
            if 'FirstName' not in column_names:
                logger.info("Adding 'FirstName' column to archived_patients table...")
                db.execute("ALTER TABLE archived_patients ADD COLUMN `FirstName` varchar(100) NOT NULL DEFAULT ''")
                logger.info("'FirstName' column added to archived_patients table.")
            if 'MiddleInitial' not in column_names:
                logger.info("Adding 'MiddleInitial' column to archived_patients table...")
                db.execute("ALTER TABLE archived_patients ADD COLUMN `MiddleInitial` varchar(10) DEFAULT NULL")
                logger.info("'MiddleInitial' column added to archived_patients table.")

        # Ensure a default user exists
        if 'users' in existing_tables:
            users = db.fetch("SELECT COUNT(*) as count FROM users")
            if users and users[0]['count'] == 0:
                logger.info("Creating default admin user...")
                # Use hashed password instead of plaintext
                hashed_password = PasswordManager.hash_password('admin')
                db.execute("INSERT INTO users (Username, Password, Role) VALUES (%s, %s, %s)", 
                          ('admin', hashed_password, 'Admin'))
                logger.info("Default admin user created (username: admin, password: admin)")

    except Exception as e:
        logger.error(f"Error during sample data setup: {str(e)}")

class MainApp(ctk.CTk):
    def __init__(self, db, user, **kwargs):
        super().__init__()
        self.db = db
        self.user = user
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.build()

    def build(self):
        # Top header 
        top = ctk.CTkFrame(self, fg_color=("#f0f0f0", "#1a1a1a"), height=70)
        top.pack(side='top', fill='x', padx=0, pady=0)
        top.pack_propagate(False)
        
        left_top = ctk.CTkFrame(top, fg_color="transparent")
        left_top.pack(side='left', fill='y', padx=20, pady=15)
        ctk.CTkLabel(left_top, text="👤", font=('Segoe UI', 22)).pack(side='left', padx=5) # This emoji is generally safe
        ctk.CTkLabel(left_top, text=f"{self.user['Username']}", font=('Segoe UI', 16, 'bold')).pack(side='left', padx=5)
        ctk.CTkLabel(left_top, text=f"({self.user['Role']})", font=('Segoe UI', 12), text_color=("gray50", "gray70")).pack(side='left', padx=5)
        
        right_top = ctk.CTkFrame(top, fg_color="transparent")
        right_top.pack(side='right', fill='y', padx=20, pady=15)
        ctk.CTkLabel(right_top, text="Theme:", font=('Segoe UI', 12)).pack(side='left', padx=5)
        self.mode_var = ctk.StringVar(value='dark')
        seg = ctk.CTkSegmentedButton(right_top, values=['🌙 Dark','☀️ Light'], variable=self.mode_var, command=self.switch_mode, width=120, font=('Segoe UI', 11))
        seg.pack(side='left', padx=5)

        main_container = ctk.CTkFrame(self)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        sidebar = ctk.CTkFrame(main_container, width=SIDEBAR_WIDTH, fg_color=("#a19494", "#212121"))
        sidebar.pack(side='left', fill='y', padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        ctk.CTkLabel(sidebar, text="NAVIGATION", font=('Segoe UI', 11, 'bold'), text_color=("gray50", "gray70")).pack(pady=12, padx=12)
        
        ctk.CTkLabel(sidebar, text="", fg_color=("gray70", "gray40"), height=1).pack(fill='x', padx=8, pady=0)
        
        # Navigation buttons - use scrollable frame for many buttons
        self.left = ctk.CTkScrollableFrame(sidebar, fg_color="transparent")
        self.left.pack(fill='both', expand=True, padx=8, pady=12)
        
        btns = [
            ('🏠 Dashboard', self.show_dashboard),
            ('👥 Patients', self.show_workflow),
            ('👨‍⚕️ Doctors', self.show_doctors),
            ('📅 Appointments', self.show_appointments),
            ('📋 Medical Records', self.show_medical_records),
            ('🛒 Sales', self.show_sales),
            ('📦 Inventory', self.show_inventory),
            ('📅 Schedule Follow-up', self.show_followup),
            ('📊 Reports', self.show_reports),
            ('📑 Archive', self.show_archive),
        ]
        for t, cmd in btns:
            b = ctk.CTkButton(self.left, text=t, command=cmd, font=('Segoe UI', 11), height=35, anchor='w', fg_color=("#3498db", "#1f6aa5"), hover_color=("#2980b9", "#164d7a"))
            b.pack(fill='x', pady=3, padx=0)
        
        logout_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logout_frame.pack(fill='x', padx=8, pady=12, side='bottom')
        ctk.CTkButton(logout_frame, text='Logout', command=self.logout, font=('Segoe UI', 12), height=40, fg_color=("#e74c3c", "#c0392b"), hover_color=("#c0392b", "#a93226")).pack(fill='x', pady=0)
        
        self.content = ctk.CTkFrame(main_container, fg_color=("white", "#0a0a0a"))
        self.content.pack(side='left', fill='both', expand=True, padx=10, pady=0)

        # managers
        managers = {
            'pm': PatientManager(self.db),
            'dm': DoctorManager(self.db),
            'am': AppointmentManager(self.db),
            'im': InventoryManager(self.db),
            'bm': BillingManager(self.db),
            'proc_m': ProcedureManager(self.db),
            'sm': SalesManager(self.db),
            'pres_m': PrescriptionManager(self.db),
            'mr_m': MedicalRecordsManager(self.db),
            'rem_m': ReminderManager(self.db),
            'inv_m': InvoiceManager(self.db)
        }

        # frames - Only essential optical clinic frames
        self.frames = {}
        self.frames['dashboard'] = DashboardFrame(self.content, managers)
        self.frames['workflow'] = WorkflowFrame(self.content, managers)
        self.frames['doctors'] = DoctorsFrame(self.content, managers['dm'])
        self.frames['appointments'] = AppointmentsFrame(self.content, managers['am'], managers['pm'], managers['dm'])
        self.frames['medical_records'] = MedicalRecordsFrame(self.content, managers)
        self.frames['sales'] = SalesFrame(self.content, managers['sm'], managers['bm'], managers['pm'], managers['im'], managers['inv_m'])
        self.frames['inventory'] = InventoryFrame(self.content, managers['im'])
        self.frames['followup'] = FollowUpFrame(self.content, managers)
        self.frames['reports'] = ReportsFrame(self.content, managers)
        self.frames['archive'] = ArchiveFrame(self.content, managers)

        self.show_dashboard()

    def switch_mode(self, mode):
        actual_mode = mode.split()[-1]  
        ctk.set_appearance_mode(actual_mode)

    def hide_all(self):
        for f in self.frames.values():
            f.pack_forget()

    def show_dashboard(self):
        self.hide_all()
        self.frames['dashboard'].pack(fill='both', expand=True)
    def show_workflow(self):
        self.hide_all()
        self.frames['workflow'].pack(fill='both', expand=True)
    def show_doctors(self):
        self.hide_all()
        self.frames['doctors'].pack(fill='both', expand=True)
    def show_appointments(self):
        self.hide_all()
        self.frames['appointments'].pack(fill='both', expand=True)
    def show_medical_records(self):
        self.hide_all()
        self.frames['medical_records'].pack(fill='both', expand=True)
    def show_sales(self):
        self.hide_all()
        self.frames['sales'].pack(fill='both', expand=True)
    def show_inventory(self):
        self.hide_all()
        self.frames['inventory'].pack(fill='both', expand=True)
    def show_followup(self):
        self.hide_all()
        self.frames['followup'].pack(fill='both', expand=True)
    def show_reports(self):
        self.hide_all()
        self.frames['reports'].pack(fill='both',expand=True)
    def show_archive(self):
        self.hide_all()
        self.frames['archive'].pack(fill='both',expand=True)
    def logout(self):
        self.destroy()
        main()

def main():
    try:
        db = Database(raise_on_error=True)
        if not db.is_connected():
            error_msg = ERROR_DB_CONNECTION.format(DATABASE_NAME)
            logger.error(error_msg)
            messagebox.showerror('Database Error', error_msg + f'\n\nError: {db.last_error}')
            return
        
        ensure_sample_data(db)
        login = LoginWindow(db)
        login.mainloop()

        if login.user_data:
            app = MainApp(db, login.user_data)
            app.mainloop()
    except RuntimeError as e:
        error_msg = f'Failed to connect to database:\n\n{str(e)}'
        logger.error(error_msg)
        messagebox.showerror('Database Error', error_msg)
    except Exception as e:
        error_msg = f'An unexpected error occurred:\n\n{str(e)}'
        logger.error(error_msg)
        messagebox.showerror('Application Error', error_msg)

if __name__ == '__main__':
    main()
