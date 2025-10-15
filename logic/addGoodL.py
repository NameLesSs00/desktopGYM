from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.ui_addGood import Ui_Dialog

class AddGoodDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db
        
        self.ui.pushButton_5.clicked.connect(self.add_good)
        self.ui.pushButton_4.clicked.connect(self.reject)
        
        self.load_suppliers()
        
    def load_suppliers(self):
        try:
            query = "SELECT supplier_id FROM Suppliers"
            self.db.cursor.execute(query)
            suppliers = self.db.cursor.fetchall()
            if not suppliers:
                QMessageBox.warning(self, "Warning", "No suppliers found. Please add suppliers first.")
                self.reject()
                return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load suppliers: {str(e)}")
            self.reject()

    def validate_input(self):
        supplier_id = self.ui.lineEdit.text().strip()
        name = self.ui.lineEdit_2.text().strip()
        quantity = self.ui.lineEdit_3.text().strip()
        price = self.ui.lineEdit_4.text().strip()

        if not supplier_id:
            QMessageBox.warning(self, "Validation Error", "Supplier ID is required")
            self.ui.lineEdit.setFocus()
            return None

        if not name:
            QMessageBox.warning(self, "Validation Error", "Good name is required")
            self.ui.lineEdit_2.setFocus()
            return None

        if not quantity or not quantity.isdigit():
            QMessageBox.warning(self, "Validation Error", "Quantity must be a valid number")
            self.ui.lineEdit_3.setFocus()
            return None

        try:
            price_float = float(price)
            if price_float <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Price must be a valid positive number")
            self.ui.lineEdit_4.setFocus()
            return None

        return {
            'supplier_id': int(supplier_id),
            'name': name,
            'quantity': int(quantity),
            'price': price_float
        }

    def verify_supplier_exists(self, supplier_id):
        try:
            query = "SELECT COUNT(*) FROM Suppliers WHERE supplier_id = ?"
            self.db.cursor.execute(query, (supplier_id,))
            return self.db.cursor.fetchone()[0] > 0
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to verify supplier: {str(e)}")
            return False

    def add_good(self):
        data = self.validate_input()
        if not data:
            return

        if not self.verify_supplier_exists(data['supplier_id']):
            QMessageBox.warning(self, "Error", "Invalid supplier ID")
            self.ui.lineEdit.setFocus()
            return

        try:
            query = """
            INSERT INTO Supplies (supplier_id, item_name, quantity, price)
            VALUES (?, ?, ?, ?)
            """
            self.db.cursor.execute(query, (
                data['supplier_id'],
                data['name'],
                data['quantity'],
                data['price']
            ))
            self.db.connection.commit()
            
            QMessageBox.information(self, "Success", "Good added successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add good: {str(e)}")
            print(f"Database error: {str(e)}")
