from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.ui_addSameGood import Ui_Dialog  # Your .ui file for the dialog
from datetime import datetime

class AddSameGoodDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)  # parent can be None or a QWidget, not Ui_MainWindow
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Buttons
        self.ui.pushButton_5.clicked.connect(self.add_same_good)  # OK button
        self.ui.pushButton_4.clicked.connect(self.reject)         # Cancel button

    def validate_input(self):
        good_id = self.ui.lineEdit_3.text().strip()
        amount_to_add = self.ui.lineEdit.text().strip()
        total_cost = self.ui.lineEdit_2.text().strip()

        if not good_id.isdigit():
            QMessageBox.warning(self, "Validation Error", "Good ID must be a number.")
            return None
        if not amount_to_add.isdigit():
            QMessageBox.warning(self, "Validation Error", "Amount to add must be a number.")
            return None
        try:
            cost_float = float(total_cost)
            if cost_float <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Total cost must be a positive number.")
            return None

        return {
            "good_id": int(good_id),
            "amount_to_add": int(amount_to_add),
            "total_cost": cost_float
        }

    def add_same_good(self):
        data = self.validate_input()
        if not data:
            return

        try:
            # 1. Update the quantity in Supplies
            update_query = "UPDATE Supplies SET quantity = quantity + ? WHERE supply_id = ?"
            self.db.cursor.execute(update_query, (data["amount_to_add"], data["good_id"]))

            # 2. Add an expense record
            expense_query = """
                INSERT INTO Expenses (description, amount, expense_date)
                VALUES (?, ?, ?)
            """
            desc = f"Added {data['amount_to_add']} units to Good ID {data['good_id']}"
            self.db.cursor.execute(expense_query, (desc, data["total_cost"], datetime.now()))

            # Commit the changes
            self.db.connection.commit()

            QMessageBox.information(self, "Success", "Stock updated and expense recorded!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update stock: {str(e)}")
