from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.ui_addEmployee import Ui_Dialog  # Make sure you have this UI file

class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.add_employee)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)        # Cancel

    def validate_input(self):
        """Validate input fields before inserting into database"""
        name = self.ui.lineEdit.text().strip()
        phone = self.ui.lineEdit_2.text().strip()
        salary = self.ui.lineEdit_3.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Employee name is required")
            self.ui.lineEdit.setFocus()
            return None

        if not salary:
            QMessageBox.warning(self, "Validation Error", "Salary is required")
            self.ui.lineEdit_3.setFocus()
            return None

        try:
            salary_float = float(salary)
            if salary_float <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Salary must be a valid positive number")
            self.ui.lineEdit_3.setFocus()
            return None

        return {
            'name': name,
            'phone': phone,
            'salary': salary_float
        }

    def add_employee(self):
        """Insert a new employee into the database"""
        data = self.validate_input()
        if not data:
            return

        try:
            query = """
            INSERT INTO Employees (name, phone, salary)
            VALUES (?, ?, ?)
            """
            self.db.cursor.execute(query, (
                data['name'],
                data['phone'],
                data['salary']
            ))
            self.db.connection.commit()

            QMessageBox.information(self, "Success", "Employee added successfully!")
            self.accept()  # Close the dialog

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add employee: {str(e)}")
            print(f"Database error: {str(e)}")
