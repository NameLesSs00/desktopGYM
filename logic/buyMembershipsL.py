from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.ui_buyMembership import Ui_Dialog
from datetime import timedelta, date, datetime

class BuyMembershipDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Load memberships into combo box
        self.load_memberships()

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.buy_membership)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)          # Cancel
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
        user_id_text = self.ui.lineEdit.text().strip()
        if not user_id_text or not user_id_text.isdigit():
            QMessageBox.warning(self, "Validation Error", "Please enter a valid User ID")
            self.ui.lineEdit.setFocus()
            return None
        user_id = int(user_id_text)

        # Check if user exists
        self.db.cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id = ?", (user_id,))
        if self.db.cursor.fetchone()[0] == 0:
            QMessageBox.warning(self, "Validation Error", f"No user found with ID {user_id}")
            self.ui.lineEdit.setFocus()
            return None

        index = self.ui.comboBox.currentIndex()
        if index < 0 or not self.memberships:
            QMessageBox.warning(self, "Validation Error", "Please select a membership")
            return None

        membership = self.memberships[index]

        return {
            'user_id': user_id,
            'membership_id': membership[0],
            'duration_days': membership[2],
            'price': membership[3]
        }

    def buy_membership(self):
        """Insert membership for an existing user and log income"""
        data = self.validate_input()
        if not data:
            return

        try:
            start_date = date.today()
            end_date = start_date + timedelta(days=data['duration_days'])

            # Insert membership
            insert_membership = """
            INSERT INTO UserMemberships (user_id, membership_id, start_date, end_date)
            VALUES (?, ?, ?, ?)
            """
            self.db.cursor.execute(insert_membership, (
                data['user_id'],
                data['membership_id'],
                start_date,
                end_date
            ))
            self.db.connection.commit()

            # Insert income record
            insert_income = """
            INSERT INTO Income (source, amount, income_date)
            VALUES (?, ?, ?)
            """
            self.db.cursor.execute(insert_income, ("membership", data['price'], datetime.now()))
            self.db.connection.commit()

            QMessageBox.information(
                self,
                "Success",
                f"Membership purchased successfully!\nAvailable till: {end_date.strftime('%d:%m:%Y')}"
            )
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to purchase membership: {str(e)}")
            print(f"Database error: {str(e)}")
