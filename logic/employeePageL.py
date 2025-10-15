from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
from PySide6.QtCore import Qt, QDate

class EmployeesPage:
    def __init__(self, ui, db, current_system_user_id):
        self.ui = ui
        self.db = db
        self.current_system_user_id = current_system_user_id

        self.ui.lineEdit_2.setPlaceholderText("Search by Employee ID")
        self.table = self.ui.employee.findChild(QTableWidget, "tableWidget_4")

        self.setup_table()
        self.load_employees()

        self.ui.pushButton_15.clicked.connect(self.search_employee_by_id)

    def setup_table(self):
        headers = ["ID", "Name", "Phone", "Salary", "Role", "Username", "Action", "Pay Employee"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_employees(self):
        try:
            query = """
                SELECT e.employee_id, e.name, e.phone, e.salary, su.role, su.username, su.system_user_id
                FROM Employees e
                LEFT JOIN SystemUsers su ON e.employee_id = su.employee_id
                ORDER BY e.employee_id DESC
            """
            self.db.cursor.execute(query)
            employees = self.db.cursor.fetchall()
            self.populate_table(employees)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load employees: {str(e)}")

    def populate_table(self, employees):
        self.table.setRowCount(0)
        for row_num, emp in enumerate(employees):
            self.table.insertRow(row_num)
            emp_id, name, phone, salary, role, username, system_user_id = emp

            # Basic info columns
            for col_num, value in enumerate([emp_id, name, phone, salary]):
                if col_num == 3 and value is not None:
                    value = f"${value:.2f}"
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)

            # Role
            role_item = QTableWidgetItem(role if role else "")
            role_item.setTextAlignment(Qt.AlignCenter)
            role_item.setFlags(role_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_num, 4, role_item)

            # Username
            username_item = QTableWidgetItem(username if username else "")
            username_item.setTextAlignment(Qt.AlignCenter)
            username_item.setFlags(username_item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_num, 5, username_item)

            # Delete button
            if system_user_id:
                btn_delete = QPushButton("Delete")
                btn_delete.clicked.connect(
                    lambda checked, su_id=system_user_id: self.delete_system_user(su_id)
                )
                self.table.setCellWidget(row_num, 6, btn_delete)
            else:
                self.table.setItem(row_num, 6, QTableWidgetItem(""))

            # Pay button
            btn_pay = QPushButton("Pay")
            btn_pay.clicked.connect(
                lambda checked, e_id=emp_id, e_name=name, btn=btn_pay: self.pay_employee(e_id, e_name, btn)
            )
            self.table.setCellWidget(row_num, 7, btn_pay)

    def pay_employee(self, employee_id, employee_name, btn_pay):
        try:
            self.db.cursor.execute(
                "SELECT salary FROM Employees WHERE employee_id = ?", (employee_id,)
            )
            result = self.db.cursor.fetchone()
            if not result:
                QMessageBox.warning(None, "Error", f"No salary found for {employee_name}.")
                return

            salary_amount = result[0]
            if salary_amount <= 0:
                QMessageBox.warning(None, "Error", f"Invalid salary amount for {employee_name}.")
                return

            self.db.cursor.execute(
                "INSERT INTO SalaryPayments (employee_id, amount, payment_date) VALUES (?, ?, ?)",
                (employee_id, salary_amount, QDate.currentDate().toString("yyyy-MM-dd"))
            )
            self.db.cursor.execute(
                "INSERT INTO Expenses (description, amount, expense_date) VALUES (?, ?, ?)",
                (f"Salary Payment: {employee_name}", salary_amount, QDate.currentDate().toString("yyyy-MM-dd"))
            )
            self.db.connection.commit()
            QMessageBox.information(None, "Success", f"Paid {employee_name} ${salary_amount:.2f} successfully!")
        except Exception as e:
            self.db.connection.rollback()
            QMessageBox.critical(None, "Error", f"Failed to pay employee: {str(e)}")

    def delete_system_user(self, system_user_id):
        if system_user_id == self.current_system_user_id:
            QMessageBox.warning(None, "Cannot Delete", "You cannot delete yourself!")
            return

        confirm = QMessageBox.question(
            None,
            "Confirm Delete",
            "Are you sure you want to delete this system user?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            # Delete dependent records in other tables if necessary
            # Example: SystemUserLogins
            self.db.cursor.execute(
                "DELETE FROM SystemUserLogins WHERE system_user_id = ?", (system_user_id,)
            )

            # Delete the system user only
            self.db.cursor.execute(
                "DELETE FROM SystemUsers WHERE system_user_id = ?", (system_user_id,)
            )
            self.db.connection.commit()
            QMessageBox.information(None, "Deleted", "System user deleted successfully.")
            self.load_employees()
        except Exception as e:
            self.db.connection.rollback()
            QMessageBox.critical(None, "Error", f"Failed to delete system user: {str(e)}")

    def refresh(self):
        self.load_employees()

    def search_employee_by_id(self):
        employee_id = self.ui.lineEdit_5.text().strip()
        if employee_id == "":
            self.refresh()
            return
        if not employee_id.isdigit():
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid numeric Employee ID.")
            return

        try:
            query = """
                SELECT e.employee_id, e.name, e.phone, e.salary, su.role, su.username, su.system_user_id
                FROM Employees e
                LEFT JOIN SystemUsers su ON e.employee_id = su.employee_id
                WHERE e.employee_id = ?
            """
            self.db.cursor.execute(query, (int(employee_id),))
            employees = self.db.cursor.fetchall()
            if employees:
                self.populate_table(employees)
            else:
                QMessageBox.information(None, "Not Found", f"No employee found with ID {employee_id}.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search employee: {str(e)}")
