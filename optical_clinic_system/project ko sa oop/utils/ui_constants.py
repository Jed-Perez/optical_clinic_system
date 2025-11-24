# ===== FONTS =====
FONT_TITLE_LARGE = ('Segoe UI', 28, 'bold')
FONT_TITLE_MEDIUM = ('Segoe UI', 18, 'bold')
FONT_TITLE_SMALL = ('Segoe UI', 16, 'bold')
FONT_LABEL_BOLD = ('Segoe UI', 14, 'bold')
FONT_LABEL_NORMAL = ('Segoe UI', 14)
FONT_LABEL_SMALL = ('Segoe UI', 13)
FONT_LABEL_SMALL_BOLD = ('Segoe UI', 13, 'bold')
FONT_BUTTON = ('Segoe UI', 14, 'bold')
FONT_BUTTON_SMALL = ('Segoe UI', 13, 'bold')
FONT_MONO = ('Consolas', 13)
FONT_MONO_SMALL = ('Consolas', 12)
FONT_EMOJI = ('Segoe UI Emoji', 40)
FONT_EMOJI_SMALL = ('Segoe UI Emoji', 22)

# ===== COLORS - BUTTONS =====
BTN_SUCCESS = ("#27ae60", "#1e8449")  # (light, dark)
BTN_WARNING = ("#f39c12", "#d68910")
BTN_DANGER = ("#e74c3c", "#c0392b")
BTN_INFO = ("#3498db", "#2980b9")
BTN_DEFAULT = ("#3498db", "#2980b9")

# ===== COLORS - FRAMES =====
COLOR_HEADER_BG = ("white", "#1a1a1a")
COLOR_SEPARATOR = ("gray80", "gray30")
COLOR_PANEL_BG = ("white", "#0f0f0f")
COLOR_PANEL_LIGHT = ("#f0f0f0", "#1a1a1a")
COLOR_TEXT_BG = ("#f5f5f5", "#1a1a1a")

# ===== SIZES =====
HEADER_HEIGHT = 70
SIDEBAR_WIDTH = 200
LEFT_PANEL_WIDTH = 350
LEFT_PANEL_WIDTH_SMALL = 300
BUTTON_HEIGHT = 40
BUTTON_HEIGHT_SMALL = 35
BUTTON_HEIGHT_TINY = 32
ENTRY_HEIGHT = 35
ENTRY_HEIGHT_SMALL = 32

# ===== PADDING & MARGINS =====
PADDING_LARGE = 20
PADDING_NORMAL = 15
PADDING_SMALL = 10
PADDING_TINY = 5

# ===== ICON EMOJIS =====
ICON_ADD = "➕"
ICON_DELETE = "🗑️"
ICON_EDIT = "✏️"
ICON_VIEW = "👁️"
ICON_ARCHIVE = "📑"
ICON_PATIENT = "👥"
ICON_DOCTOR = "👨‍⚕️"
ICON_APPOINTMENT = "📅"
ICON_PRESCRIPTION = "👓"
ICON_MEDICAL = "📋"
ICON_BILLING = "💳"
ICON_INVENTORY = "📦"
ICON_SALES = "🛒"
ICON_REPORTS = "📊"
ICON_DASHBOARD = "🏠"
ICON_SEARCH = "🔍"
ICON_REFRESH = "🔄"
ICON_CHECK = "✅"
ICON_ALERT = "⚠️"
ICON_HOME = "🏠"
ICON_REMINDER = "🔔"
ICON_SETTINGS = "⚙️"
ICON_LOGOUT = "🚪"
ICON_RIGHT_EYE = "🔴"
ICON_LEFT_EYE = "🔵"

# ===== VALIDATION MESSAGES =====
MSG_REQUIRED = "{field} is required"
MSG_INVALID_FORMAT = "{field} format is invalid"
MSG_INVALID_NUMBER = "{field} must be numeric"
MSG_INVALID_INTEGER = "{field} must be a whole number"
MSG_SUCCESS = "{action} completed successfully"
MSG_ERROR = "An error occurred: {error}"
MSG_CONFIRM_DELETE = "Are you sure you want to delete this record?"
MSG_CONFIRM_ARCHIVE = "Are you sure you want to archive this record?"

# ===== UI LABELS =====
LBL_ADD_NEW = "Add New {entity}"
LBL_PATIENT = "Patient"
LBL_DOCTOR = "Doctor"
LBL_APPOINTMENT = "Appointment"
LBL_PRESCRIPTION = "Prescription"
LBL_MEDICAL_RECORD = "Medical Record"
LBL_BILL = "Bill"
LBL_INVENTORY = "Inventory"
LBL_PRODUCT = "Product"
LBL_SALE = "Sale"
LBL_INVOICE = "Invoice"
LBL_REMINDER = "Reminder"

# ===== BUTTON LABELS =====
BTN_ADD = f"{ICON_ADD} Add"
BTN_DELETE = f"{ICON_DELETE} Delete"
BTN_EDIT = f"{ICON_EDIT} Edit"
BTN_VIEW = f"{ICON_VIEW} View"
BTN_REFRESH = f"{ICON_REFRESH} Refresh"
BTN_SAVE = "Save"
BTN_CANCEL = "Cancel"
BTN_CLOSE = "Close"
BTN_SEARCH = "Search"
BTN_CLEAR = "Clear"
BTN_CREATE = f"{ICON_CHECK} Create"
BTN_SUBMIT = "Submit"
BTN_BACK = "Back"

# ===== SEARCH & DISPLAY =====
SEARCH_PLACEHOLDER = "Search..."
SEARCH_PLACEHOLDER_NAME = "Search by name..."
SEARCH_PLACEHOLDER_ID = "Enter ID..."
COMBOBOX_SELECT = "Select {entity}"
COMBOBOX_SELECT_PATIENT = "Select Patient"
COMBOBOX_SELECT_DOCTOR = "Select Doctor"

# ===== TABLE/TEXT DISPLAY =====
TEXTBOX_FONT = FONT_MONO
TEXTBOX_FONT_SMALL = FONT_MONO_SMALL
TEXT_COLUMN_WIDTH = 15

# ===== WINDOW TITLES =====
TITLE_PATIENT_MGMT = f"{ICON_PATIENT} Patient Management"
TITLE_DOCTOR_MGMT = f"{ICON_DOCTOR} Doctor Management"
TITLE_APPOINTMENT_MGMT = f"{ICON_APPOINTMENT} Appointment Management"
TITLE_PRESCRIPTION_MGMT = f"{ICON_PRESCRIPTION} Prescription Management"
TITLE_MEDICAL_RECORDS = f"{ICON_MEDICAL} Medical Records"
TITLE_BILLING_MGMT = f"{ICON_BILLING} Billing Management"
TITLE_INVENTORY_MGMT = f"{ICON_INVENTORY} Inventory Management"
TITLE_SALES_MGMT = f"{ICON_SALES} Sales Management"
TITLE_REPORTS = f"{ICON_REPORTS} Reports"
TITLE_ARCHIVE = "Archive"
TITLE_DASHBOARD = f"{ICON_DASHBOARD} Dashboard"
TITLE_REMINDERS = f"{ICON_REMINDER} Reminders"

# ===== DIALOG TITLES =====
DIALOG_SUCCESS = "Success"
DIALOG_ERROR = "Error"
DIALOG_WARNING = "Warning"
DIALOG_INFO = "Information"
DIALOG_VALIDATION_ERROR = "Validation Error"

# ===== AGE GROUPS & OPTIONS =====
AGE_GROUPS = ['Kids', 'Adult']
GENDERS = ['Male', 'Female', 'Other']
PAYMENT_METHODS = ['Cash', 'Card', 'Check']
SALES_CATEGORIES = ['Lenses', 'Frames', 'Glasses', 'Contact Lenses', 'Eye Care Products', 'Cleaning Solutions', 'Cases & Accessories', 'Reading Glasses', 'Sunglasses', 'Blue Light Glasses']
APPOINTMENT_STATUS = ['Scheduled', 'Done', 'Cancelled']
REMINDER_METHODS = ['SMS', 'Email', 'Call']
