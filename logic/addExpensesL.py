from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.ui_addExpenses import Ui_Dialog
from PySide6.QtCore import QDate

class AddExpensesDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.add_expense)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)       # Cancel

        # Optional: default date to today if there's a dateEdit
        if hasattr(self.ui, "dateEdit"):
            self.ui.dateEdit.setDate(QDate.currentDate())

    def validate_input(self):
        """Validate the input fields before inserting into database"""
        description = self.ui.lineEdit.text().strip()
        amount = self.ui.lineEdit_2.text().strip()

        if not description:
            QMessageBox.warning(self, "Validation Error", "Description is required")
            self.ui.lineEdit.setFocus()
            return None

        try:
            amount_float = float(amount)
            if amount_float <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Amount must be a valid positive number")
            self.ui.lineEdit_2.setFocus()
            return None

        return {
            'description': description,
            'amount': amount_float
        }

    def add_expense(self):
        """Insert a new expense into the database"""
        data = self.validate_input()
        if not data:
            return

        try:
            query = """
            INSERT INTO Expenses (description, amount, expense_date)
            VALUES (?, ?, CONVERT(date, GETDATE()))
            """
            self.db.cursor.execute(query, (
                data['description'],
                data['amount']
            ))
            self.db.connection.commit()

            QMessageBox.information(self, "Success", "Expense added successfully!")
            self.accept()  # Close the dialog

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add expense: {str(e)}")
            print(f"Database error: {str(e)}")
