from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
from PySide6.QtCore import Qt
from datetime import date

class UsersPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db

        # Placeholder for search input
        self.ui.lineEdit.setPlaceholderText("Search by User ID")

        # Find the table in the users page
        self.table = self.ui.users.findChild(QTableWidget, "tableWidget")  # Replace with your actual table name
        self.setup_table()
        self.load_users()

        # Connect search button
        self.ui.pushButton_7.clicked.connect(self.search_user_by_id)  # Search button

    def setup_table(self):
        headers = ["ID", "Name", "Age", "Gender", "Membership Type", "Available Till", "Registration Date"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_users(self):
        """Load all users and their latest membership info"""
        try:
            # Query to get user info along with newest membership (if exists)
            query = """
            SELECT u.user_id, u.name, u.date_of_birth, u.gender, u.registration_date,
                   m.type, um.end_date
            FROM Users u
            LEFT JOIN (
                SELECT um1.user_id, um1.membership_id, um1.start_date, um1.end_date
                FROM UserMemberships um1
                WHERE um1.end_date = (
                    SELECT MAX(end_date) FROM UserMemberships um2
                    WHERE um2.user_id = um1.user_id
                )
            ) um ON u.user_id = um.user_id
            LEFT JOIN Memberships m ON um.membership_id = m.membership_id
            ORDER BY u.user_id DESC
            """
            self.db.cursor.execute(query)
            users = self.db.cursor.fetchall()
            self.populate_table(users)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load users: {str(e)}")

    def calculate_age(self, dob):
        """Calculate age in years from date of birth"""
        if not dob:
            return ""
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age

    def populate_table(self, users):
        """Fill the table with the given data"""
        self.table.setRowCount(0)
        for row_num, user in enumerate(users):
            self.table.insertRow(row_num)
            user_id, name, dob, gender, reg_date, membership_type, available_till = user

            age = self.calculate_age(dob) if dob else ""
            membership_type = membership_type if membership_type else ""
            available_till_str = available_till.strftime("%Y-%m-%d") if available_till else ""

            row_data = [user_id, name, age, gender, membership_type, available_till_str, reg_date.strftime("%Y-%m-%d")]

            for col_num, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)

    def refresh(self):
        """Reload all users"""
        self.load_users()

    def search_user_by_id(self):
        """Search user by user_id from lineEdit"""
        user_id = self.ui.lineEdit.text().strip()
        if user_id == "":
            self.refresh()
            return

        if not user_id.isdigit():
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid numeric User ID.")
            return

        try:
            query = """
            SELECT u.user_id, u.name, u.date_of_birth, u.gender, u.registration_date,
                   m.type, um.end_date
            FROM Users u
            LEFT JOIN (
                SELECT um1.user_id, um1.membership_id, um1.start_date, um1.end_date
                FROM UserMemberships um1
                WHERE um1.end_date = (
                    SELECT MAX(end_date) FROM UserMemberships um2
                    WHERE um2.user_id = um1.user_id
                )
            ) um ON u.user_id = um.user_id
            LEFT JOIN Memberships m ON um.membership_id = m.membership_id
            WHERE u.user_id = ?
            """
            self.db.cursor.execute(query, (int(user_id),))
            users = self.db.cursor.fetchall()

            if users:
                self.populate_table(users)
            else:
                QMessageBox.information(None, "Not Found", f"No user found with ID {user_id}.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search user: {str(e)}")
