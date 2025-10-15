import sys
import os
import configparser
import traceback
from cryptography.fernet import Fernet
from PySide6.QtWidgets import QMainWindow, QMessageBox, QLineEdit
from PySide6.QtCore import Signal

# ----- Base path & config -----
if getattr(sys, 'frozen', False):
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_path = os.path.join(BASE_PATH, "config.ini")

if not os.path.exists(config_path):
    raise FileNotFoundError(f"config.ini not found at {config_path}")

config = configparser.ConfigParser()
config.read(config_path)
secret_key = config.get("APP", "SECRET_KEY").encode()
fernet = Fernet(secret_key)

# ----- Add widgets folder to path -----
sys.path.insert(0, os.path.join(BASE_PATH, "widgits"))
import widgits.rec_rc  # Ensure your resources file is here

# ----- Login Window -----
class LoginWindow(QMainWindow):
    login_success = Signal(bool)

    def __init__(self, db, stack, admin_page, cashier_page, helpdesk_page,
                 admin_ui, cashier_ui, helpdesk_ui,
                 ADMIN_NAV, CASHIER_NAV, HELPDESK_NAV,
                 NORMAL_STYLE, ACTIVE_STYLE):
        super().__init__()
        self.db = db
        self.stack = stack

        # Pages & UIs
        self.admin_page = admin_page
        self.cashier_page = cashier_page
        self.helpdesk_page = helpdesk_page
        self.admin_ui = admin_ui
        self.cashier_ui = cashier_ui
        self.helpdesk_ui = helpdesk_ui

        # Navigation & styles
        self.ADMIN_NAV = ADMIN_NAV
        self.CASHIER_NAV = CASHIER_NAV
        self.HELPDESK_NAV = HELPDESK_NAV
        self.NORMAL_STYLE = NORMAL_STYLE
        self.ACTIVE_STYLE = ACTIVE_STYLE

        # Logged-in user info
        self.logged_system_user_id = None
        self.logged_employee_id = None

        # Load login UI
        from widgits.ui_Login import Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.pushButton.clicked.connect(self.handle_login)

        # Optional pre-fill

        # Use the global fernet
        self.fernet = fernet

    # ----- Password decryption -----
    def decrypt_password(self, encrypted_password: str) -> str:
        decrypted = self.fernet.decrypt(encrypted_password.encode())
        return decrypted.decode()

    # ----- Navigation helpers -----
    def reset_admin_nav(self):
        for btn in self.ADMIN_NAV:
            btn.setStyleSheet(self.NORMAL_STYLE)

    def reset_cashier_nav(self):
        for btn in self.CASHIER_NAV:
            btn.setStyleSheet(self.NORMAL_STYLE)

    def reset_helpdesk_nav(self):
        for btn in self.HELPDESK_NAV:
            btn.setStyleSheet(self.NORMAL_STYLE)

    def set_active_admin(self, btn=None):
        self.reset_admin_nav()
        if btn:
            btn.setStyleSheet(self.ACTIVE_STYLE)

    def set_active_cashier(self, btn=None):
        self.reset_cashier_nav()
        if btn:
            btn.setStyleSheet(self.ACTIVE_STYLE)

    def set_active_helpdesk(self, btn=None):
        self.reset_helpdesk_nav()
        if btn:
            btn.setStyleSheet(self.ACTIVE_STYLE)

    # ----- Handle login -----
    def handle_login(self):
        username_input = self.ui.lineEdit.text().strip()
        password_input = self.ui.lineEdit_2.text().strip()

        try:
            self.db.cursor.execute(
                "SELECT system_user_id, employee_id, username, hashed_password, role FROM SystemUsers"
            )
            users = self.db.cursor.fetchall()

            for user in users:
                system_user_id, employee_id, db_username, db_encrypted_password, role = user
                decrypted_password = self.decrypt_password(db_encrypted_password)

                if username_input == db_username and password_input == decrypted_password:
                    self.logged_system_user_id = system_user_id
                    self.logged_employee_id = employee_id

                    # Log login
                    try:
                        self.db.cursor.execute(
                            "INSERT INTO SystemUserLogins (system_user_id) VALUES (?)",
                            (system_user_id,)
                        )
                        self.db.connection.commit()
                    except Exception as e:
                        print("Failed to log user login:", e)

                    # Clear input
                    self.ui.lineEdit.clear()
                    self.ui.lineEdit_2.clear()

                    # Role-based navigation
                    if role.lower() == "admin":
                        self.stack.setCurrentWidget(self.admin_page)
                        self.admin_ui.stackedWidget.setCurrentWidget(self.admin_ui.sales)
                        self.set_active_admin(self.admin_ui.pushButton_2)
                    elif role.lower() == "cashier":
                        self.stack.setCurrentWidget(self.cashier_page)
                        self.cashier_ui.stackedWidget.setCurrentWidget(self.cashier_ui.cashierWork)
                        self.set_active_cashier(self.cashier_ui.pushButton_7)
                        self.cashier_ui.pushButton_4.hide()
                    elif role.lower() == "helpdesk":
                        self.stack.setCurrentWidget(self.helpdesk_page)
                        self.helpdesk_ui.stackedWidget.setCurrentWidget(self.helpdesk_ui.users)
                        self.set_active_helpdesk(self.helpdesk_ui.pushButton_3)
                        self.helpdesk_ui.pushButton_4.hide()

                    self.login_success.emit(True)
                    return

            # No matching user
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password.")
            self.login_success.emit(False)

        except Exception as e:
            print("Login error:", e)
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Login error: {str(e)}")
            self.login_success.emit(False)

    # ----- Getters -----
    def get_logged_system_user_id(self):
        return self.logged_system_user_id

    def get_logged_employee_id(self):
        return self.logged_employee_id
