from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.ui_addUser import Ui_Dialog
from datetime import timedelta, date, datetime

class AddUserDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Load memberships into combo box
        self.load_memberships()

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.add_user)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)    # Cancel
        self.ui.comboBox.currentIndexChanged.connect(self.update_membership_info)

        # Set default membership info (Weekly)
        self.set_default_membership_info()

    def load_memberships(self):
        """Load membership types from DB into combo box"""
        try:
            query = "SELECT membership_id, type, duration_days, price FROM Memberships ORDER BY membership_id"
            self.db.cursor.execute(query)
            self.memberships = self.db.cursor.fetchall()

            self.ui.comboBox.clear()
            for m in self.memberships:
                self.ui.comboBox.addItem(m[1], userData=m)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load memberships: {str(e)}")
            self.memberships = []

    def set_default_membership_info(self):
        """Set default values for the first membership (Weekly)"""
        if not self.memberships:
            return

        weekly = next((m for m in self.memberships if m[1].lower() == 'weekly'), self.memberships[0])
        index = self.memberships.index(weekly)
        self.ui.comboBox.setCurrentIndex(index)

        duration_days = weekly[2]
        price = weekly[3]
        start_date = date.today()
        end_date = start_date + timedelta(days=duration_days)

        self.ui.label_9.setText(f"Available till: {end_date.strftime('%d:%m:%Y')} | {duration_days} days")
        self.ui.label_4.setText(f"That will cost: ${price:.2f}")

    def update_membership_info(self):
        """Update labels when a different membership is selected"""
        index = self.ui.comboBox.currentIndex()
        if index < 0 or not self.memberships:
            return
        membership = self.memberships[index]

        duration_days = membership[2]
        price = membership[3]
        start_date = date.today()
        end_date = start_date + timedelta(days=duration_days)

        self.ui.label_9.setText(f"Available till: {end_date.strftime('%d:%m:%Y')} | {duration_days} days")
        self.ui.label_4.setText(f"That will cost: ${price:.2f}")

    def validate_input(self):
        """Validate user inputs"""
        name = self.ui.lineEdit.text().strip()
        dob = self.ui.dateEdit.date().toPython()

        gender = None
        if self.ui.radioButton.isChecked():
            gender = "Female"
        elif self.ui.radioButton_3.isChecked():
            gender = "Male"

        index = self.ui.comboBox.currentIndex()
        if index < 0 or not self.memberships:
            QMessageBox.warning(self, "Validation Error", "Please select a membership")
            return None

        membership = self.memberships[index]

        if not name:
            QMessageBox.warning(self, "Validation Error", "User name is required")
            self.ui.lineEdit.setFocus()
            return None

        if not gender:
            QMessageBox.warning(self, "Validation Error", "Please select gender")
            return None

        return {
            'name': name,
            'dob': dob,
            'gender': gender,
            'membership_id': membership[0],
            'duration_days': membership[2],
            'price': membership[3]
        }

    def add_user(self):
        """Insert user, assign membership, and then log income"""
        data = self.validate_input()
        if not data:
            return

        try:
            # Step 1: Insert user
            insert_user = """
            INSERT INTO Users (name, date_of_birth, gender, registration_date)
            VALUES (?, ?, ?, GETDATE())
            """
            self.db.cursor.execute(insert_user, (data['name'], data['dob'], data['gender']))
            self.db.connection.commit()

            # Step 2: Get the new user_id
            self.db.cursor.execute("SELECT TOP 1 user_id FROM Users ORDER BY user_id DESC")
            user_id = self.db.cursor.fetchone()[0]

            # Step 3: Insert into UserMemberships
            start_date = date.today()
            end_date = start_date + timedelta(days=data['duration_days'])
            insert_membership = """
            INSERT INTO UserMemberships (user_id, membership_id, start_date, end_date)
            VALUES (?, ?, ?, ?)
            """
            self.db.cursor.execute(insert_membership, (user_id, data['membership_id'], start_date, end_date))
            self.db.connection.commit()

            # Step 4: Insert into Income after membership is added
            insert_income = """
            INSERT INTO Income (source, amount, income_date)
            VALUES (?, ?, ?)
            """
            source_label = "membership"
            self.db.cursor.execute(insert_income, (source_label, data['price'], datetime.now()))
            self.db.connection.commit()

            # Success message
            QMessageBox.information(
                self,
                "Success",
                f"User added successfully!\nMembership available till: {end_date.strftime('%d:%m:%Y')}"
            )
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add user: {str(e)}")
            print(f"Database error: {str(e)}")
