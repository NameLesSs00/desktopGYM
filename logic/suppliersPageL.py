from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Qt

class SuppliersPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db

        # Set placeholder text for lineEdit_3
        self.ui.lineEdit_3.setPlaceholderText("Search by Supplier ID")

        # Find the table widget in the suppliers page
        self.table = self.ui.suppliers.findChild(QTableWidget, "tableWidget_3")
        self.setup_table()
        self.load_suppliers()

        # Connect search button
        self.ui.pushButton_12.clicked.connect(self.search_supplier_by_id)

    def setup_table(self):
        headers = ["ID", "Name", "Email", "Phone"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_suppliers(self):
        """Load all suppliers"""
        try:
            query = """
            SELECT supplier_id, name, email, phone
            FROM Suppliers
            ORDER BY supplier_id DESC
            """
            self.db.cursor.execute(query)
            suppliers = self.db.cursor.fetchall()
            self.populate_table(suppliers)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load suppliers: {str(e)}")

    def populate_table(self, suppliers):
        """Fill the table with given supplier data"""
        self.table.setRowCount(0)
        for row_num, supplier in enumerate(suppliers):
            self.table.insertRow(row_num)
            for col_num, value in enumerate(supplier):
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Read-only
                self.table.setItem(row_num, col_num, item)

    def refresh(self):
        """Reload all suppliers"""
        self.load_suppliers()

    def search_supplier_by_id(self):
        supplier_id = self.ui.lineEdit_3.text().strip()

        if supplier_id == "":
            # Empty input -> reload all suppliers
            self.refresh()
            return

        if not supplier_id.isdigit():
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid numeric supplier ID.")
            return

        try:
            query = "SELECT supplier_id, name, email, phone FROM Suppliers WHERE supplier_id = ?"
            self.db.cursor.execute(query, (int(supplier_id),))
            supplier = self.db.cursor.fetchall()

            if supplier:
                self.populate_table(supplier)
            else:
                QMessageBox.information(None, "Not Found", f"No supplier found with ID {supplier_id}.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search supplier: {str(e)}")
