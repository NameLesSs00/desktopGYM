from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.ui_addTrainer import Ui_Dialog

class AddTrainerDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.add_trainer)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)       # Cancel

    def validate_input(self):
        """Validate input fields before inserting into database"""
        name = self.ui.lineEdit.text().strip()
        phone = self.ui.lineEdit_2.text().strip()
        specialization = self.ui.lineEdit_4.text().strip()

        # Get gender from radio buttons
        gender = None
        if self.ui.radioButton.isChecked():
            gender = "Female"
        elif self.ui.radioButton_3.isChecked():
            gender = "Male"

        # --- Validation ---
        if not name:
            QMessageBox.warning(self, "Validation Error", "Trainer name is required")
            self.ui.lineEdit.setFocus()
            return None

        if not gender:
            QMessageBox.warning(self, "Validation Error", "Please select a gender")
            return None

        if not phone or not phone.isdigit() or len(phone) != 11:
            QMessageBox.warning(self, "Validation Error", "Phone number must be 11 digits")
            self.ui.lineEdit_2.setFocus()
            return None

        return {
            'name': name,
            'gender': gender,
            'phone': phone,
            'specialization': specialization if specialization else None
        }

    def add_trainer(self):
        """Insert a new trainer into the database"""
        data = self.validate_input()
        if not data:
            return

        try:
            query = """
            INSERT INTO Trainers (name, gender, phone, specialization)
            VALUES (?, ?, ?, ?)
            """
            self.db.cursor.execute(query, (
                data['name'],
                data['gender'],
                data['phone'],
                data['specialization']
            ))
            self.db.connection.commit()

            QMessageBox.information(self, "Success", "Trainer added successfully!")
            self.accept()  # Close the dialog

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add trainer: {str(e)}")
            print(f"Database error: {str(e)}")
