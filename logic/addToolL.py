from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.ui_addTool import Ui_Dialog
from PySide6.QtCore import QDate

class AddToolDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.add_tool)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)    # Cancel

    def validate_input(self):
        """Validate input fields before inserting into database"""
        name = self.ui.lineEdit.text().strip()
        cost = self.ui.lineEdit_2.text().strip()
        tag_name = self.ui.lineEdit_3.text().strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Tool name is required")
            self.ui.lineEdit.setFocus()
            return None

        if cost:
            try:
                cost_float = float(cost)
                if cost_float < 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Cost must be a valid positive number")
                self.ui.lineEdit_2.setFocus()
                return None
        else:
            cost_float = 0.0  # Default to 0 if no cost provided

        purchase_date = QDate.currentDate().toString("yyyy-MM-dd")

        return {
            'name': name,
            'tag_name': tag_name if tag_name else None,
            'purchase_date': purchase_date,
            'cost': cost_float
        }

    def verify_name_unique(self, name):
        """Check if a tool with the same name already exists"""
        try:
            query = "SELECT COUNT(*) FROM Tools WHERE name = ?"
            self.db.cursor.execute(query, (name,))
            return self.db.cursor.fetchone()[0] == 0
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to verify tool name: {str(e)}")
            return False

    def add_tool(self):
        """Insert a new tool into the database and record the expense"""
        data = self.validate_input()
        if not data:
            return

        if not self.verify_name_unique(data['name']):
            QMessageBox.warning(self, "Error", "Tool name already exists")
            self.ui.lineEdit.setFocus()
            return

        try:
            # Insert tool into Tools table
            tool_query = """
            INSERT INTO Tools (name, tag_name, purchase_date, cost)
            VALUES (?, ?, ?, ?)
            """
            self.db.cursor.execute(tool_query, (
                data['name'],
                data['tag_name'],
                data['purchase_date'],
                data['cost']
            ))

            # Insert expense into Expenses table
            expense_query = """
            INSERT INTO Expenses (description, amount, expense_date)
            VALUES (?, ?, ?)
            """
            description = f"Tool purchased: {data['name']}"
            self.db.cursor.execute(expense_query, (
                description,
                data['cost'],
                data['purchase_date']
            ))

            # Commit both inserts
            self.db.connection.commit()

            QMessageBox.information(self, "Success", "Tool added and expense recorded successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add tool or record expense: {str(e)}")
            print(f"Database error: {str(e)}")
