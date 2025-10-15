from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Qt

class ExpensesPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db

        # Set placeholder for search input
        self.ui.lineEdit_2.setPlaceholderText("Search by Expense ID")

        # Find the table in the expenses page
        self.table = self.ui.expenses.findChild(QTableWidget, "tableWidget_3")
        self.setup_table()
        self.load_expenses()

        # Connect search button
        self.ui.pushButton_13.clicked.connect(self.search_expense_by_id)  # Adjust to your search button

    def setup_table(self):
        headers = ["ID", "Description", "Amount", "Date"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_expenses(self):
        """Load all expenses from the database"""
        try:
            query = """
            SELECT expense_id, description, amount, expense_date
            FROM Expenses
            ORDER BY expense_id DESC
            """
            self.db.cursor.execute(query)
            expenses = self.db.cursor.fetchall()
            self.populate_table(expenses)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load expenses: {str(e)}")

    def populate_table(self, expenses):
        """Fill the table with the given data"""
        self.table.setRowCount(0)
        for row_num, expense in enumerate(expenses):
            self.table.insertRow(row_num)
            for col_num, value in enumerate(expense):
                if col_num == 2 and value is not None:  # Amount formatting
                    value = f"${value:.2f}"
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Read-only
                self.table.setItem(row_num, col_num, item)

    def refresh(self):
        """Reload all expenses"""
        self.load_expenses()

    def search_expense_by_id(self):
        """Search expense by expense_id from lineEdit_2"""
        expense_id = self.ui.lineEdit_4.text().strip()

        if expense_id == "":
            self.refresh()
            return

        if not expense_id.isdigit():
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid numeric Expense ID.")
            return

        try:
            query = """
            SELECT expense_id, description, amount, expense_date
            FROM Expenses
            WHERE expense_id = ?
            """
            self.db.cursor.execute(query, (int(expense_id),))
            expenses = self.db.cursor.fetchall()

            if expenses:
                self.populate_table(expenses)
            else:
                QMessageBox.information(None, "Not Found", f"No expense found with ID {expense_id}.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search expense: {str(e)}")
