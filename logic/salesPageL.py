from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QMessageBox, QTableWidget
from PySide6.QtCore import Qt

class SalesPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db

        # Set placeholder for search input
        self.ui.lineEdit.setPlaceholderText("Search by Income ID")

        # Get the table widget correctly
        self.table = self.ui.sales.findChild(QTableWidget, "tableWidget")
        if self.table is None:
            QMessageBox.critical(None, "Error", "Sales table not found!")
            return

        self.setup_table()
        self.load_income()

        # Connect search button
        self.ui.pushButton_7.clicked.connect(self.search_income_by_id)

    def setup_table(self):
        headers = ["Income ID", "Source", "Amount", "Date & Time"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_income(self):
        """Load all income records from the database without summing"""
        try:
            query = """
            SELECT income_id, source, amount, income_date
            FROM Income
            ORDER BY income_id DESC
            """
            self.db.cursor.execute(query)
            incomes = self.db.cursor.fetchall()
            self.populate_table(incomes)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load income records: {str(e)}")

    def populate_table(self, incomes):
        """Fill the QTableWidget with raw income records"""
        self.table.setRowCount(0)
        for row_num, income in enumerate(incomes):
            self.table.insertRow(row_num)
            income_id, source, amount, income_date = income

            # Show amount as currency
            row_values = [income_id, source, f"${amount:.2f}", str(income_date)]
            for col_num, value in enumerate(row_values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # make cells read-only
                self.table.setItem(row_num, col_num, item)

    def search_income_by_id(self):
        """Search for a specific income record by its ID"""
        income_id = self.ui.lineEdit.text().strip()
        if income_id == "":
            self.refresh()  # call refresh here instead of load_income
            return

        if not income_id.isdigit():
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid numeric Income ID.")
            return

        try:
            query = """
            SELECT income_id, source, amount, income_date 
            FROM Income 
            WHERE income_id = ?
            """
            self.db.cursor.execute(query, (int(income_id),))
            incomes = self.db.cursor.fetchall()

            if incomes:
                self.populate_table(incomes)
            else:
                QMessageBox.information(None, "Not Found", f"No income record found with ID {income_id}.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search income record: {str(e)}")

    def refresh(self):
        """Reload all income records, like SessionsPage refresh"""
        self.load_income()
