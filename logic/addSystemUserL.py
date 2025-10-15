from PySide6.QtWidgets import QDialog, QMessageBox, QLineEdit
from widgits.ui_addSystemUser import Ui_Dialog
from cryptography.fernet import Fernet
import configparser

class AddSystemUserDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Hide password input
        self.ui.lineEdit_3.setEchoMode(QLineEdit.Password)

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.add_system_user)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)           # Cancel

        # Load secret key from config
        config = configparser.ConfigParser()
        config.read("config.ini")
        secret_key = config.get("APP", "SECRET_KEY").encode()
        self.fernet = Fernet(secret_key)

        # Initialize role comboBox
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(["cashier", "admin", "helpdesk"])
        self.ui.comboBox.setCurrentText("cashier")  # default to cashier

    def encrypt_password(self, password: str) -> str:
        """Encrypt the password using the app secret key"""
        encrypted = self.fernet.encrypt(password.encode())
        return encrypted.decode()

    def validate_input(self):
        """Validate input fields before inserting into database"""
        employee_id_text = self.ui.lineEdit.text().strip()
        username = self.ui.lineEdit_2.text().strip()
        password = self.ui.lineEdit_3.text().strip()

        # Employee ID validation
        if not employee_id_text or not employee_id_text.isdigit():
            QMessageBox.warning(self, "Validation Error", "Employee ID must be a valid number")
            self.ui.lineEdit.setFocus()
            return None

        employee_id = int(employee_id_text)

        # Check if employee exists
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM Employees WHERE employee_id = ?", (employee_id,)
            )
            if self.db.cursor.fetchone()[0] == 0:
                QMessageBox.warning(
                    self, "Validation Error", f"No employee found with ID {employee_id}"
                )
                self.ui.lineEdit.setFocus()
                return None
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to verify employee ID: {str(e)}")
            return None

        if not username:
            QMessageBox.warning(self, "Validation Error", "Username is required")
            self.ui.lineEdit_2.setFocus()
            return None

        if not password:
            QMessageBox.warning(self, "Validation Error", "Password is required")
            self.ui.lineEdit_3.setFocus()
            return None

        # Encrypt the password using the secret key
        encrypted_password = self.encrypt_password(password)

        return {
            'employee_id': employee_id,
            'username': username,
            'hashed_password': encrypted_password
        }

    def add_system_user(self):
        """Insert a new system user into the database"""
        data = self.validate_input()
        if not data:
            return

        try:
            # Get role from comboBox
            role = self.ui.comboBox.currentText().strip().lower()

            query = """
            INSERT INTO SystemUsers (employee_id, role, username, hashed_password, created_at)
            VALUES (?, ?, ?, ?, GETDATE())
            """
            self.db.cursor.execute(query, (
                data['employee_id'],
                role,
                data['username'],
                data['hashed_password']
            ))
            self.db.connection.commit()

            QMessageBox.information(self, "Success", f"System user added successfully as {role}!")
            self.accept()  # Close the dialog

        except Exception as e:
            if "UNIQUE" in str(e):
                QMessageBox.warning(self, "Error", "Username already exists")
            else:
                QMessageBox.critical(self, "Error", f"Failed to add system user: {str(e)}")
            print(f"Database error: {str(e)}")
