from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Qt

class GoodsPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db

        # Set placeholder for search input
        self.ui.lineEdit_2.setPlaceholderText("Search by Goods ID")

        # Find the table in the goods page
        self.table = self.ui.goods.findChild(QTableWidget, "tableWidget_2")
        self.setup_table()
        self.load_goods()

        # Connect search button
        self.ui.pushButton_9.clicked.connect(self.search_goods_by_id)

    def setup_table(self):
        headers = ["ID", "Supplier Name", "Item Name", "Quantity", "Price"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_goods(self):
        """Load all goods from the database"""
        try:
            query = """
            SELECT s.supply_id, sup.name as supplier_name, s.item_name, s.quantity, s.price 
            FROM Supplies s
            JOIN Suppliers sup ON s.supplier_id = sup.supplier_id
            ORDER BY s.supply_id DESC
            """
            self.db.cursor.execute(query)
            goods = self.db.cursor.fetchall()
            self.populate_table(goods)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load goods: {str(e)}")

    def populate_table(self, goods):
        """Fill the table with the given data"""
        self.table.setRowCount(0)
        for row_num, good in enumerate(goods):
            self.table.insertRow(row_num)
            for col_num, value in enumerate(good):
                if col_num == 4 and value is not None:  # Price formatting
                    value = f"${value:.2f}"
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Read-only
                self.table.setItem(row_num, col_num, item)

    def refresh(self):
        """Reload all goods"""
        self.load_goods()

    def search_goods_by_id(self):
        """Search goods by supply ID from lineEdit_2"""
        supply_id = self.ui.lineEdit_2.text().strip()

        if supply_id == "":
            self.refresh()
            return

        if not supply_id.isdigit():
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid numeric Goods ID.")
            return

        try:
            query = """
            SELECT s.supply_id, sup.name as supplier_name, s.item_name, s.quantity, s.price 
            FROM Supplies s
            JOIN Suppliers sup ON s.supplier_id = sup.supplier_id
            WHERE s.supply_id = ?
            """
            self.db.cursor.execute(query, (int(supply_id),))
            goods = self.db.cursor.fetchall()

            if goods:
                self.populate_table(goods)
            else:
                QMessageBox.information(None, "Not Found", f"No goods found with ID {supply_id}.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search goods: {str(e)}")
