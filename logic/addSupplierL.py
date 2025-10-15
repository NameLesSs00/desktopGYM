from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.addSupplier import Ui_Dialog
import re

class AddSupplierDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db
        
        self.ui.pushButton_5.clicked.connect(self.add_supplier)
        self.ui.pushButton_4.clicked.connect(self.reject)

    def validate_email(self, email):
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_phone(self, phone):
        if not phone:
            return True
        digits_only = ''.join(filter(str.isdigit, phone))
        return len(digits_only) == 11

    def validate_name(self, name):
        if not name:
            return False, "Name is required"
        if len(name) > 100:
            return False, "Name must be less than 100 characters"
        return True, ""

    def add_supplier(self):
        name = self.ui.lineEdit_2.text().strip()
        phone = self.ui.lineEdit_3.text().strip()
        email = self.ui.lineEdit_4.text().strip()
        
        name_valid, name_error = self.validate_name(name)
        if not name_valid:
            QMessageBox.warning(self, "Validation Error", name_error)
            self.ui.lineEdit_2.setFocus()
            return

        if email and not self.validate_email(email):
            QMessageBox.warning(self, "Validation Error", "Invalid email format")
            self.ui.lineEdit_4.setFocus()
            return

        if phone and not self.validate_phone(phone):
            QMessageBox.warning(self, "Validation Error", "Phone number must be 11 digits")
            self.ui.lineEdit_3.setFocus()
            return

        try:
            check_query = "SELECT COUNT(*) FROM Suppliers WHERE name = ?"
            self.db.cursor.execute(check_query, (name,))
            if self.db.cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Error", "A supplier with this name already exists!")
                self.ui.lineEdit_2.setFocus()
                return

            query = "INSERT INTO Suppliers (name, email, phone) VALUES (?, ?, ?)"
            self.db.cursor.execute(query, (name, email, phone))
            self.db.connection.commit()
            
            QMessageBox.information(self, "Success", "Supplier added successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add supplier: {str(e)}")
            print(f"Database error: {str(e)}")
            return
