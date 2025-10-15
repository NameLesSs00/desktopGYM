from PySide6.QtWidgets import QTableWidgetItem, QHeaderView, QPushButton, QMessageBox, QAbstractItemView
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import Qt
from datetime import datetime
from functools import partial

class SalePointPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db
        self.cart = []

        # Tables
        self.items_table = self.ui.cashierWork.findChild(type(self.ui.tableWidget_4), "tableWidget_4")
        self.cart_table = self.ui.cashierWork.findChild(type(self.ui.tableWidget), "tableWidget")

        # Inputs and labels
        self.search_input = self.ui.lineEdit_4
        self.discount_input = self.ui.lineEdit_5
        self.amount_tendered_input = self.ui.lineEdit      # Amount Tendered
        self.balance_due_input = self.ui.lineEdit_6        # Balance Due
        self.total_label = self.ui.label_6                 # Total: $0.00
        self.change_label = self.ui.label_3                # Change: $0.00

        # Buttons
        self.search_button = self.ui.pushButton_13
        self.sell_button = self.ui.pushButton_6
        self.cancel_button = self.ui.pushButton_14

        # Setup tables
        self.setup_items_table()
        self.setup_cart_table()

        # Load items
        self.load_items()

        # Connect buttons
        self.search_button.clicked.connect(self.search_items)
        self.sell_button.clicked.connect(self.sell_cart)
        self.cancel_button.clicked.connect(self.clear_cart)

        # Connect amount tendered input change
        self.amount_tendered_input.textChanged.connect(self.update_change_balance)

        # To prevent recursive itemChanged calls
        self._updating_cart = False

    # ---------------- Table Setup ----------------
    def setup_items_table(self):
        headers = ["ID", "Name", "Price per Unit", "Stock", "Quantity", "Add to Cart"]
        self.items_table.setColumnCount(len(headers))
        self.items_table.setHorizontalHeaderLabels(headers)
        for i in range(len(headers)):
            self.items_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        self.items_table.setEditTriggers(QAbstractItemView.DoubleClicked)

    def setup_cart_table(self):
        headers = ["Name", "Quantity", "Price per Unit", "Discount", "Total"]
        self.cart_table.setColumnCount(len(headers))
        self.cart_table.setHorizontalHeaderLabels(headers)
        for i in range(len(headers)):
            self.cart_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    # ---------------- Load Items ----------------
    def load_items(self):
        try:
            query = "SELECT supply_id, item_name, price, quantity FROM Supplies ORDER BY item_name"
            self.db.cursor.execute(query)
            items = self.db.cursor.fetchall()
            self.populate_items_table(items)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load items: {str(e)}")

    def populate_items_table(self, items):
        self.items_table.setRowCount(0)
        for row_num, item in enumerate(items):
            supply_id, name, price, stock = item
            self.items_table.insertRow(row_num)

            # Fill all cells
            values = [supply_id, name, float(price), stock, 1]
            for col_num, value in enumerate(values):
                cell = QTableWidgetItem(str(value))
                cell.setForeground(QBrush(QColor(0, 0, 0)))
                cell.setTextAlignment(Qt.AlignCenter)
                if col_num == 4:
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                else:
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.items_table.setItem(row_num, col_num, cell)

            # Add-to-cart button
            add_btn = QPushButton("Add")
            add_btn.clicked.connect(partial(self.add_to_cart_from_table, supply_id, row_num))
            self.items_table.setCellWidget(row_num, 5, add_btn)

    # ---------------- Search Items ----------------
    def search_items(self):
        search_term = self.search_input.text().strip()
        try:
            if search_term:
                query = "SELECT supply_id, item_name, price, quantity FROM Supplies WHERE item_name LIKE ?"
                self.db.cursor.execute(query, (f"%{search_term}%",))
            else:
                query = "SELECT supply_id, item_name, price, quantity FROM Supplies ORDER BY item_name"
                self.db.cursor.execute(query)
            items = self.db.cursor.fetchall()
            self.populate_items_table(items)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search items: {str(e)}")

    # ---------------- Cart ----------------
    def add_to_cart(self, supply_id, quantity=1, discount=0.0):
        self.db.cursor.execute("SELECT item_name, price, quantity FROM Supplies WHERE supply_id = ?", (supply_id,))
        result = self.db.cursor.fetchone()
        if not result:
            QMessageBox.warning(None, "Error", "Item not found")
            return
        name, price, stock = result
        price = float(price)
        if stock < quantity:
            QMessageBox.warning(None, "Stock Error", f"Not enough stock for '{name}'")
            return

        # Update cart if item exists
        for item in self.cart:
            if item["id"] == supply_id:
                item["quantity"] += quantity
                item["discount"] = discount
                self.refresh_cart_table()
                return

        # Add new entry
        self.cart.append({
            "id": supply_id,
            "name": name,
            "price": price,
            "quantity": quantity,
            "discount": discount
        })
        self.refresh_cart_table()

    def add_to_cart_from_table(self, supply_id, row):
        # Read Quantity from tableWidget_4 (editable)
        try:
            quantity = int(self.items_table.item(row, 4).text())
            if quantity < 1:
                raise ValueError
        except ValueError:
            QMessageBox.warning(None, "Invalid Quantity", "Quantity must be a positive integer")
            return

        # Read discount from input
        discount_text = self.discount_input.text().strip()
        discount = 0.0
        if discount_text:
            try:
                discount = float(discount_text)
                if not (0 <= discount <= 100):
                    raise ValueError
            except ValueError:
                QMessageBox.warning(None, "Invalid Discount", "Discount must be 0-100%")
                return

        # Add to cart with stock check
        self.db.cursor.execute("SELECT item_name, quantity FROM Supplies WHERE supply_id = ?", (supply_id,))
        result = self.db.cursor.fetchone()
        if not result:
            QMessageBox.warning(None, "Error", "Item not found")
            return
        name, stock = result
        if stock < quantity:
            QMessageBox.warning(None, "Stock Error", f"Not enough stock for '{name}'")
            return

        self.add_to_cart(supply_id, quantity=quantity, discount=discount)
        self.discount_input.setText("0")  # reset discount

        # Confirmation message
        QMessageBox.information(None, "Added to Cart", f"Added '{name}' x{quantity} with discount {discount:.2f}%")
        self.update_total_balance()

    def refresh_cart_table(self):
        self._updating_cart = True
        if self.cart_table.signalsBlocked() == False:
          try:
           self.cart_table.itemChanged.disconnect(self.on_quantity_changed)
          except Exception:
            pass
        self.cart_table.setRowCount(0)

        for row_num, item in enumerate(self.cart):
            self.cart_table.insertRow(row_num)
            discount = float(item["discount"])
            total_price = item["price"] * item["quantity"] * (1 - discount / 100)

            values = [
                item["name"],
                item["quantity"],
                f"${item['price']:.2f}",
                f"{discount:.2f}%" if discount > 0 else "-",
                f"${total_price:.2f}"
            ]

            for col_num, value in enumerate(values):
                cell = QTableWidgetItem(str(value))
                cell.setForeground(QBrush(QColor(0, 0, 0)))
                cell.setTextAlignment(Qt.AlignCenter)
                if col_num == 1:  # Quantity editable in cart
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                else:
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.cart_table.setItem(row_num, col_num, cell)

        self.cart_table.itemChanged.connect(self.on_quantity_changed)
        self._updating_cart = False
        self.update_total_balance()

    def on_quantity_changed(self, item):
        if self._updating_cart:
            return
        row = item.row()
        col = item.column()
        if col == 1:
            try:
                new_qty = int(item.text())
                if new_qty < 1:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(None, "Invalid Quantity", "Quantity must be a positive integer")
                item.setText(str(self.cart[row]["quantity"]))
                return
            # Stock check
            self.db.cursor.execute("SELECT quantity FROM Supplies WHERE supply_id = ?", (self.cart[row]["id"],))
            stock = self.db.cursor.fetchone()[0]
            if new_qty > stock:
                QMessageBox.warning(None, "Stock Error", f"Not enough stock. Max available: {stock}")
                item.setText(str(self.cart[row]["quantity"]))
                return

            self.cart[row]["quantity"] = new_qty
            self.refresh_cart_table()

    # ---------------- Total / Balance ----------------
    def update_total_balance(self):
        total = sum(item["price"] * item["quantity"] * (1 - float(item["discount"]) / 100) for item in self.cart)
        self.total_label.setText(f"Total: ${total:.2f}")

        # Update change/balance
        self.update_change_balance()

    def update_change_balance(self):
        try:
            tendered = float(self.amount_tendered_input.text())
        except:
            tendered = 0.0
        total = sum(item["price"] * item["quantity"] * (1 - float(item["discount"]) / 100) for item in self.cart)
        change = tendered - total
        self.change_label.setText(f"Change: ${max(change,0):.2f}")
        self.balance_due_input.setText(f"{max(total - tendered,0):.2f}")

    # ---------------- Sell / Clear ----------------
    def sell_cart(self):
        if not self.cart:
            QMessageBox.warning(None, "Empty Cart", "Cart is empty")
            return
        try:
            for item in self.cart:
                self.db.cursor.execute(
                    "UPDATE Supplies SET quantity = quantity - ? WHERE supply_id = ?",
                    (item["quantity"], item["id"])
                )
                total_price = item["price"] * item["quantity"] * (1 - float(item["discount"]) / 100)
                self.db.cursor.execute(
                    "INSERT INTO Income (source, amount, income_date) VALUES (?, ?, ?)",
                    ("supplies", total_price, datetime.now())
                )
            self.db.connection.commit()
            QMessageBox.information(None, "Success", "Sale completed")
            self.clear_cart()
            self.load_items()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to complete sale: {str(e)}")

    def clear_cart(self):
        self.cart = []
        self.refresh_cart_table()
        self.amount_tendered_input.setText("")
        self.balance_due_input.setText("")
        self.total_label.setText("Total: $0.00")
        self.change_label.setText("Change: $0.00")
