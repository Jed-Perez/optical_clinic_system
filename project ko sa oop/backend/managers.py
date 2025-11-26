from database.db_connection import Database
from datetime import datetime, timedelta
from utils.constants import *
from utils.logger import setup_logging
from utils.password_manager import PasswordManager
from backend.base_manager import BaseManager

logger = setup_logging(__name__)

class PatientManager(BaseManager):
    def __init__(self, db: Database):
        super().__init__(db)
        self.table_name = "patients"
        self.archived_table_name = "archived_patients"
        self.id_column = "Patient_ID"
    
    def validate_input(self, **kwargs):
        """Validate patient input data"""
        if 'surname' in kwargs and (not kwargs['surname'] or not kwargs['surname'].strip()):
            raise ValueError('Surname is required')
        if 'firstname' in kwargs and (not kwargs['firstname'] or not kwargs['firstname'].strip()):
            raise ValueError('First Name is required')
        if 'gender' in kwargs and (not kwargs['gender'] or not kwargs['gender'].strip()):
            raise ValueError('Gender is required')
        if 'age_group' in kwargs and (not kwargs['age_group'] or not kwargs['age_group'].strip()):
            raise ValueError('Age Group is required')
        if 'contact' in kwargs and (not kwargs['contact'] or not kwargs['contact'].strip()):
            raise ValueError('Contact is required')
        return True

    def add_patient(self, surname, firstname, middleinitial, age, gender, age_group, address, contact, email, medical_history):
        self.validate_input(surname=surname, firstname=firstname, gender=gender, age_group=age_group, contact=contact)

        q = "INSERT INTO patients (Surname, FirstName, MiddleInitial, Age, Gender, Age_Group, Address, Contact, Email, Medical_History, Registration_Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE())"
        return self.db.execute(q, (surname.strip(), firstname.strip(), middleinitial.strip(), age or None, gender.strip(), age_group.strip(), address.strip(), contact.strip(), email.strip(), medical_history.strip()))

    def list_patients(self):
        # Combine name parts for display, handling NULL values
        query = "SELECT *, CONCAT(COALESCE(Surname, ''), ', ', COALESCE(FirstName, ''), ' ', COALESCE(MiddleInitial, '')) AS Name FROM patients ORDER BY Patient_ID DESC"
        return self.db.fetch(query)

    def get_patient(self, patient_id):
        """Fetches a single patient by their ID, combining name parts for display."""
        query = "SELECT *, CONCAT(COALESCE(Surname, ''), ', ', COALESCE(FirstName, ''), ' ', COALESCE(MiddleInitial, '')) AS Name FROM patients WHERE Patient_ID = %s"
        result = self.db.fetch(query, (patient_id,))
        return result[0] if result else None

    def count_patients_today(self):
        """Counts the number of patients registered today."""
        query = "SELECT COUNT(*) as count FROM patients WHERE Registration_Date = CURDATE()"
        result = self.db.fetch(query)
        return result[0]['count'] if result else 0

    def archive_patient(self, patient_id):
        return self.archive(patient_id)

    def delete_patient(self, patient_id):
        return self.archive_patient(patient_id)

class DoctorManager(BaseManager):
    def __init__(self, db: Database):
        super().__init__(db)
        self.table_name = "doctors"
        self.archived_table_name = "archived_doctors"
        self.id_column = "Doctor_ID"
    
    def validate_input(self, **kwargs):
        #Validate doctor input data
        if 'surname' in kwargs and (not kwargs['surname'] or not kwargs['surname'].strip()):
            raise ValueError('Doctor surname is required')
        if 'firstname' in kwargs and (not kwargs['firstname'] or not kwargs['firstname'].strip()):
            raise ValueError('Doctor first name is required')
        if 'license_no' in kwargs and (not kwargs['license_no'] or not kwargs['license_no'].strip()):
            raise ValueError('License number is required')
        if 'specialization' in kwargs and (not kwargs['specialization'] or not kwargs['specialization'].strip()):
            raise ValueError('Specialization is required')
        return True
    
    def add_doctor(self, surname, firstname, middle_initial, license_no, specialization, contact, schedule):
        self.validate_input(surname=surname, firstname=firstname, license_no=license_no, specialization=specialization)
        
        # Format full name: Surname, FirstName M.I.
        if middle_initial and middle_initial.strip():
            full_name = f"{surname.strip()}, {firstname.strip()} {middle_initial.strip()}."
        else:
            full_name = f"{surname.strip()}, {firstname.strip()}"
        
        q = 'INSERT INTO doctors (Surname, FirstName, MiddleInitial, Name, License_No, Specialization, Contact, Schedule) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        return self.db.execute(q, (surname.strip(), firstname.strip(), middle_initial.strip() if middle_initial else '', full_name, license_no.strip(), specialization.strip(), contact.strip() if contact else '', schedule.strip() if schedule else ''))
    def list_doctors(self):
        return self.db.fetch('SELECT * FROM doctors ORDER BY Doctor_ID DESC')
    
    def archive_doctor(self, doctor_id):
        """Polymorphic override - uses BaseManager's generic archive method"""
        return self.archive(doctor_id)
    
    def delete_doctor(self, doctor_id):
        """Alias for archive_doctor for UI convenience"""
        return self.archive_doctor(doctor_id)

class AppointmentManager(BaseManager):
    def __init__(self, db: Database):
        super().__init__(db)
        self.table_name = "appointments"
        self.archived_table_name = "archived_appointments"
        self.id_column = "Appointment_ID"
    
    def validate_input(self, **kwargs):
        """Validate appointment input data"""
        if 'patient_id' in kwargs and (not kwargs['patient_id'] or not str(kwargs['patient_id']).strip()):
            raise ValueError('Patient ID is required')
        if 'doctor_id' in kwargs and (not kwargs['doctor_id'] or not str(kwargs['doctor_id']).strip()):
            raise ValueError('Doctor ID is required')
        if 'date' in kwargs and (not kwargs['date'] or not str(kwargs['date']).strip()):
            raise ValueError('Date is required (YYYY-MM-DD format)')
        if 'time' in kwargs and (not kwargs['time'] or not str(kwargs['time']).strip()):
            raise ValueError('Time is required (HH:MM format)')
        return True
    
    def schedule(self, patient_id, doctor_id, date, time):
        self.validate_input(patient_id=patient_id, doctor_id=doctor_id, date=date, time=time)
        
        try:
            existing = self.db.fetch('SELECT * FROM appointments WHERE Doctor_ID=%s AND Appointment_Date=%s AND Appointment_Time=%s AND Status=%s',
                                     (doctor_id, date, time, 'Scheduled'))
            if existing:
                raise ValueError(ERROR_DUPLICATE_BOOKING)
            
            result = self.db.execute('INSERT INTO appointments (Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time, Status) VALUES (%s,%s,%s,%s,%s)',
                                   (patient_id, doctor_id, date, time, 'Scheduled'))
            logger.info(f"Appointment scheduled: Patient {patient_id}, Doctor {doctor_id}, Date {date} {time}")
            return result
        except Exception as e:
            logger.error(f"Failed to schedule appointment: {str(e)}")
            raise
    def list_appointments(self):
        return self.db.fetch('SELECT * FROM appointments ORDER BY Appointment_Date DESC, Appointment_Time DESC')

    def mark_as_done(self, appointment_id):
        """Marks an appointment as 'Done' and then archives it."""
        try:
            self.db.execute("UPDATE appointments SET Status='Done' WHERE Appointment_ID=%s", (appointment_id,))
            self.archive(appointment_id)
            logger.info(f"Appointment {appointment_id} marked as done and archived")
            return True
        except Exception as e:
            logger.error(f"Failed to mark appointment as done: {str(e)}")
            raise

class InventoryManager(BaseManager):
    def __init__(self, db: Database):
        super().__init__(db)
        self.table_name = "inventory"
        self.archived_table_name = "archived_inventory"
        self.id_column = "Inventory_ID"
    
    def validate_input(self, **kwargs):
        """Validate inventory input data"""
        if 'name' in kwargs and (not kwargs['name'] or not kwargs['name'].strip()):
            raise ValueError('Item name is required')
        if 'category' in kwargs and (not kwargs['category'] or not kwargs['category'].strip()):
            raise ValueError('Category is required')
        if 'quantity' in kwargs and (kwargs['quantity'] is None or kwargs['quantity'] == ''):
            raise ValueError('Quantity is required')
        return True
    
    def add_item(self, name, category, quantity, unit_price, supplier):
        self.validate_input(name=name, category=category, quantity=quantity)
        
        return self.db.execute('INSERT INTO inventory (Item_Name, Category, Quantity_On_Hand, Unit_Price, Supplier) VALUES (%s,%s,%s,%s,%s)',
                               (name.strip(), category.strip(), quantity, unit_price, supplier.strip()))
    def list_items(self):
        return self.db.fetch('SELECT * FROM inventory ORDER BY Inventory_ID DESC')

    def view_all_products(self):
        return self.list_items()

class BillingManager:
    def __init__(self, db: Database):
        self.db = db
    
    def create_bill(self, patient_id, amount, method):
        # Validate required fields
        if not patient_id or not str(patient_id).strip():
            raise ValueError('Patient ID is required')
        if amount is None or amount == '':
            raise ValueError('Amount is required')
        
        return self.db.execute('INSERT INTO billing (Patient_ID, Amount, Payment_Method, Status) VALUES (%s,%s,%s,%s)', (patient_id, amount, method, 'Pending'))
    
    def add_billing(self, patient_id, amount, service='General', method='Cash', status='Pending'):
        """Add billing charge - alias for create_bill with additional parameters"""
        if not patient_id or not str(patient_id).strip():
            raise ValueError('Patient ID is required')
        if amount is None or amount == '':
            raise ValueError('Amount is required')
        
        return self.db.execute('INSERT INTO billing (Patient_ID, Amount, Payment_Method, Status) VALUES (%s,%s,%s,%s)', (patient_id, amount, method, status))
    
    def list_bills(self):
        return self.db.fetch('SELECT * FROM billing ORDER BY Billing_Date DESC')
    
    def mark_paid(self, bill_id):
        self.db.execute('UPDATE billing SET Status=%s WHERE Bill_ID=%s', ('Paid', bill_id))

class UserManager:
    def __init__(self, db: Database):
        self.db = db
    
    def find_user(self, username):
        """Find user by username"""
        try:
            rows = self.db.fetch('SELECT * FROM users WHERE Username=%s', (username,))
            return rows[0] if rows else None
        except Exception as e:
            logger.error(f"Failed to find user {username}: {str(e)}")
            raise
    
    def create_user(self, username, password, role='Staff'):
        """Create new user with hashed password"""
        if not username or not username.strip():
            raise ValueError('Username is required')
        if not password or len(password) < MIN_PASSWORD_LENGTH:
            raise ValueError(f'Password must be at least {MIN_PASSWORD_LENGTH} characters')
        
        try:
            # Hash password before storing
            hashed_password = PasswordManager.hash_password(password)
            result = self.db.execute('INSERT INTO users (Username, Password, Role) VALUES (%s,%s,%s)', 
                                   (username.strip(), hashed_password, role))
            logger.info(f"User '{username}' created with role '{role}'")
            return result
        except Exception as e:
            logger.error(f"Failed to create user: {str(e)}")
            raise
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            user = self.find_user(username)
            if not user:
                logger.warning(f"Login attempt with non-existent user: {username}")
                return None
            
            if PasswordManager.verify_password(password, user['Password']):
                logger.info(f"User '{username}' authenticated successfully")
                return user
            else:
                logger.warning(f"Failed login attempt for user: {username}")
                return None
        except Exception as e:
            logger.error(f"Error verifying user: {str(e)}")
            return None


class ProcedureManager:
    def __init__(self, db: Database):
        self.db = db

    def add_procedure(self, name, description, price):
        # Validate required fields
        if not name or not name.strip():
            raise ValueError('Procedure name is required')
        if price is None or price == '':
            raise ValueError('Price is required')
        
        query = "INSERT INTO procedures (Name, Description, Cost) VALUES (%s, %s, %s)"
        return self.db.execute(query, (name.strip(), description.strip(), price))

    def get_all_procedures(self):
        return self.db.fetch("SELECT * FROM procedures")

    def update_procedure(self, proc_id, name, description, price):
        query = "UPDATE procedures SET Name=%s, Description=%s, Cost=%s WHERE Procedure_ID=%s"
        return self.db.execute(query, (name, description, price, proc_id))

    def delete_procedure(self, proc_id):
        query = "DELETE FROM procedures WHERE Procedure_ID=%s"
        return self.db.execute(query, (proc_id,))


class SalesManager:
    def __init__(self, db: Database):
        self.db = db

    def add_product(self, name, category, description, price, quantity):
        if not name or not name.strip():
            raise ValueError('Product name is required')
        if not category or not category.strip():
            raise ValueError('Category is required')
        if price is None or price == '':
            raise ValueError('Price is required')
        if quantity is None or quantity == '':
            raise ValueError('Quantity is required')
        
        query = "INSERT INTO sales_products (name, category, description, price, quantity) VALUES (%s, %s, %s, %s, %s)"
        return self.db.execute(query, (name.strip(), category.strip(), description.strip(), float(price), int(quantity)))

    def get_all_products(self):
        return self.db.fetch("SELECT * FROM sales_products ORDER BY category, name")
    
    def list_products(self):
        """Alias for get_all_products"""
        return self.get_all_products()

    def get_products_by_category(self, category):
        return self.db.fetch("SELECT * FROM sales_products WHERE category = %s", (category,))

    def update_product(self, product_id, name, category, description, price, quantity):
        if not name or not name.strip():
            raise ValueError('Product name is required')
        if not category or not category.strip():
            raise ValueError('Category is required')
        
        query = "UPDATE sales_products SET name=%s, category=%s, description=%s, price=%s, quantity=%s WHERE id=%s"
        return self.db.execute(query, (name.strip(), category.strip(), description.strip(), float(price), int(quantity), product_id))

    def delete_product(self, product_id):
        query = "DELETE FROM sales_products WHERE id=%s"
        return self.db.execute(query, (product_id,))

    def create_sale(self, customer_name, items):
        if not customer_name or not customer_name.strip():
            raise ValueError('Customer name is required')
        if not items:
            raise ValueError('Sale must have at least one item')
        
        total = sum(item['quantity'] * item['price'] for item in items)
        
        query = "INSERT INTO sales (customer_name, total, sale_date) VALUES (%s, %s, NOW())"
        sale_id = self.db.execute(query, (customer_name.strip(), total))
        

        for item in items:
            item_query = "INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
            self.db.execute(item_query, (sale_id, item['product_id'], item['quantity'], item['price']))
            
            self.db.execute("UPDATE sales_products SET quantity = quantity - %s WHERE id = %s", 
                          (item['quantity'], item['product_id']))
        
        return sale_id

    def get_all_sales(self):
        return self.db.fetch("SELECT * FROM sales ORDER BY sale_date DESC")

    def get_sale_details(self, sale_id):
        return self.db.fetch("SELECT si.*, sp.name FROM sale_items si JOIN sales_products sp ON si.product_id = sp.id WHERE si.sale_id = %s", (sale_id,))

    def get_sales_report(self):
        return self.db.fetch("SELECT category, COUNT(*) as count, SUM(quantity) as total_qty, AVG(price) as avg_price FROM sales_products GROUP BY category")


class PrescriptionManager:
    def __init__(self, db: Database):
        self.db = db

    def create_prescription(self, patient_id, doctor_id, appointment_id, 
                           od_sph, od_cyl, od_axis, od_add,
                           os_sph, os_cyl, os_axis, os_add, notes):
        if not patient_id or not doctor_id:
            raise ValueError('Patient ID and Doctor ID are required')
        
        try:
            issued_date = datetime.now().date()
            expiry_date = issued_date + timedelta(days=PRESCRIPTION_VALIDITY_DAYS)  
            
            query = """INSERT INTO prescriptions 
                       (Patient_ID, Doctor_ID, Appointment_ID, Issued_Date, Expiry_Date,
                        OD_Sphere, OD_Cylinder, OD_Axis, OD_Add,
                        OS_Sphere, OS_Cylinder, OS_Axis, OS_Add, Notes)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            result = self.db.execute(query, (patient_id, doctor_id, appointment_id, issued_date, expiry_date,
                                           od_sph, od_cyl, od_axis, od_add,
                                           os_sph, os_cyl, os_axis, os_add, notes))
            logger.info(f"Prescription created for patient {patient_id} by doctor {doctor_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to create prescription: {str(e)}")
            raise

    def get_patient_prescriptions(self, patient_id):
        query = """SELECT p.*, d.Name as Doctor_Name 
                   FROM prescriptions p 
                   JOIN doctors d ON p.Doctor_ID = d.Doctor_ID 
                   WHERE p.Patient_ID = %s 
                   ORDER BY p.Issued_Date DESC"""
        return self.db.fetch(query, (patient_id,))

    def get_latest_prescription(self, patient_id):
        query = """SELECT * FROM prescriptions 
                   WHERE Patient_ID = %s AND Expiry_Date >= CURDATE()
                   ORDER BY Issued_Date DESC LIMIT 1"""
        result = self.db.fetch(query, (patient_id,))
        return result[0] if result else None

    def get_all_prescriptions(self):
        query = """SELECT p.*, CONCAT(pa.Surname, ', ', pa.FirstName) as Patient_Name, d.Name as Doctor_Name
                   FROM prescriptions p
                   JOIN patients pa ON p.Patient_ID = pa.Patient_ID
                   JOIN doctors d ON p.Doctor_ID = d.Doctor_ID
                   ORDER BY p.Issued_Date DESC"""
        return self.db.fetch(query)

    def update_prescription(self, prescription_id, od_sph, od_cyl, od_axis, od_add,
                           os_sph, os_cyl, os_axis, os_add, notes):
        query = """UPDATE prescriptions 
                   SET OD_Sphere=%s, OD_Cylinder=%s, OD_Axis=%s, OD_Add=%s,
                       OS_Sphere=%s, OS_Cylinder=%s, OS_Axis=%s, OS_Add=%s, Notes=%s
                   WHERE Prescription_ID = %s"""
        return self.db.execute(query, (od_sph, od_cyl, od_axis, od_add,
                                       os_sph, os_cyl, os_axis, os_add, notes, prescription_id))

    def delete_prescription(self, prescription_id):
        return self.db.execute("DELETE FROM prescriptions WHERE Prescription_ID = %s", (prescription_id,))

    def check_expiring_prescriptions(self):
        query = """SELECT * FROM prescriptions 
                   WHERE Expiry_Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 30 DAY)
                   ORDER BY Expiry_Date ASC"""
        return self.db.fetch(query)


class MedicalRecordsManager:
    def __init__(self, db: Database):
        self.db = db

    def add_record(self, patient_id, doctor_id, appointment_id, diagnosis, severity, 
                   clinical_notes, recommendations, followup_days=90):
        """Create medical record"""
        if not patient_id or not doctor_id:
            raise ValueError('Patient ID and Doctor ID are required')
        
        query = """INSERT INTO medical_records 
                   (Patient_ID, Doctor_ID, Appointment_ID, Diagnosis, Severity,
                    Clinical_Notes, Recommendations, Follow_up_Days)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        return self.db.execute(query, (patient_id, doctor_id, appointment_id, diagnosis, severity,
                                       clinical_notes, recommendations, followup_days))

    def get_patient_records(self, patient_id):
        """Get all medical records for patient"""
        query = """SELECT mr.*, d.Name as Doctor_Name 
                   FROM medical_records mr 
                   JOIN doctors d ON mr.Doctor_ID = d.Doctor_ID 
                   WHERE mr.Patient_ID = %s 
                   ORDER BY mr.Recorded_Date DESC"""
        return self.db.fetch(query, (patient_id,))

    def get_all_records(self):
        """List all medical records"""
        query = """SELECT mr.*, CONCAT(pa.Surname, ', ', pa.FirstName) as Patient_Name, d.Name as Doctor_Name
                   FROM medical_records mr
                   JOIN patients pa ON mr.Patient_ID = pa.Patient_ID
                   JOIN doctors d ON mr.Doctor_ID = d.Doctor_ID
                   ORDER BY mr.Recorded_Date DESC"""
        return self.db.fetch(query)

    def update_record(self, record_id, diagnosis, severity, clinical_notes, recommendations):
        """Update medical record"""
        query = """UPDATE medical_records 
                   SET Diagnosis=%s, Severity=%s, Clinical_Notes=%s, Recommendations=%s
                   WHERE Record_ID = %s"""
        return self.db.execute(query, (diagnosis, severity, clinical_notes, recommendations, record_id))

    def delete_record(self, record_id):
        """Delete medical record"""
        return self.db.execute("DELETE FROM medical_records WHERE Record_ID = %s", (record_id,))

    def check_due_followups(self):
        """Get patients due for follow-up"""
        query = """SELECT mr.*, pa.Contact, pa.Email, CONCAT(pa.Surname, ', ', pa.FirstName) as Name
                   FROM medical_records mr
                   JOIN patients pa ON mr.Patient_ID = pa.Patient_ID
                   WHERE DATE_ADD(mr.Recorded_Date, INTERVAL mr.Follow_up_Days DAY) <= CURDATE()
                   ORDER BY mr.Recorded_Date ASC"""
        return self.db.fetch(query)


class ReminderManager:
    def __init__(self, db: Database):
        self.db = db

    def create_reminder(self, appointment_id, patient_id, reminder_date, reminder_time, contact_method='SMS'):
        if not appointment_id or not patient_id:
            raise ValueError('Appointment ID and Patient ID are required')
        
        query = """INSERT INTO appointment_reminders 
                   (Appointment_ID, Patient_ID, Reminder_Date, Reminder_Time, Contact_Method)
                   VALUES (%s, %s, %s, %s, %s)"""
        return self.db.execute(query, (appointment_id, patient_id, reminder_date, reminder_time, contact_method))

    def get_pending_reminders(self):
        query = """SELECT ar.*, pa.Contact, pa.Email, CONCAT(pa.Surname, ', ', pa.FirstName) as Name, ap.Appointment_Time
                   FROM appointment_reminders ar
                   JOIN patients pa ON ar.Patient_ID = pa.Patient_ID
                   JOIN appointments ap ON ar.Appointment_ID = ap.Appointment_ID
                   WHERE ar.Status = 'Pending' AND ar.Reminder_Date <= CURDATE()
                   ORDER BY ar.Reminder_Date ASC"""
        return self.db.fetch(query)

    def mark_sent(self, reminder_id):
        query = """UPDATE appointment_reminders 
                   SET Status = 'Sent', Sent_Date = NOW()
                   WHERE Reminder_ID = %s"""
        return self.db.execute(query, (reminder_id,))

    def get_appointment_reminders(self, appointment_id):
        query = """SELECT * FROM appointment_reminders 
                   WHERE Appointment_ID = %s 
                   ORDER BY Reminder_Date ASC"""
        return self.db.fetch(query, (appointment_id,))

    def delete_reminder(self, reminder_id):
        return self.db.execute("DELETE FROM appointment_reminders WHERE Reminder_ID = %s", (reminder_id,))


class InvoiceManager:
    def __init__(self, db: Database):
        self.db = db

    def create_invoice(self, sale_id, patient_id, generated_by):
        from datetime import date
        
        try:
            sale = self.db.fetch("SELECT * FROM sales WHERE id = %s", (sale_id,))[0]
            invoice_number = f"INV-{date.today().strftime('%Y%m%d')}-{sale_id}"
            tax = round(sale['total'] * INVOICE_TAX_RATE, 2)
            grand_total = round(sale['total'] + tax, 2)
            
            query = """INSERT INTO invoices 
                       (Sale_ID, Patient_ID, Invoice_Number, Invoice_Date, Total_Amount, Tax, Grand_Total, Generated_By)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            result = self.db.execute(query, (sale_id, patient_id, invoice_number, date.today(), 
                                           sale['total'], tax, grand_total, generated_by))
            logger.info(f"Invoice {invoice_number} created for sale {sale_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to create invoice: {str(e)}")
            raise

    def get_all_invoices(self):
        query = """SELECT i.*, CONCAT(pa.Surname, ', ', pa.FirstName) as Patient_Name
                   FROM invoices i
                   LEFT JOIN patients pa ON i.Patient_ID = pa.Patient_ID
                   ORDER BY i.Invoice_Date DESC"""
        return self.db.fetch(query)

    def get_invoice_details(self, invoice_id):
        query = """SELECT i.*, CONCAT(pa.Surname, ', ', pa.FirstName) as Patient_Name, pa.Contact, pa.Email, s.customer_name
                   FROM invoices i 
                   LEFT JOIN patients pa ON i.Patient_ID = pa.Patient_ID
                   LEFT JOIN sales s ON i.Sale_ID = s.id
                   WHERE i.Invoice_ID = %s"""
        return self.db.fetch(query, (invoice_id,))[0] if self.db.fetch(query, (invoice_id,)) else None

    def get_invoice_items(self, sale_id):
        query = """SELECT si.*, sp.name 
                   FROM sale_items si 
                   JOIN sales_products sp ON si.product_id = sp.id 
                   WHERE si.sale_id = %s"""
        return self.db.fetch(query, (sale_id,))

    def mark_invoice_paid(self, invoice_id):
        return self.db.execute("UPDATE invoices SET Status = 'Paid' WHERE Invoice_ID = %s", (invoice_id,))

    def get_invoices_by_patient(self, patient_id):
        query = """SELECT * FROM invoices 
                   WHERE Patient_ID = %s 
                   ORDER BY Invoice_Date DESC"""
        return self.db.fetch(query, (patient_id,))
