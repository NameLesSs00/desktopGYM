from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import QDate, QTime
from widgits.ui_addSession import Ui_Dialog  # Replace with your actual .ui file

class AddSessionDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.add_session)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)       # Cancel

        # Set default date to today
        self.ui.dateEdit.setDate(QDate.currentDate())

    def validate_input(self):
        """Validate all input fields"""
        # Trainer ID
        trainer_id_text = self.ui.lineEdit.text().strip()
        if not trainer_id_text.isdigit():
            QMessageBox.warning(self, "Validation Error", "Trainer ID must be a valid number")
            self.ui.lineEdit.setFocus()
            return None
        trainer_id = int(trainer_id_text)

        # Check trainer exists
        self.db.cursor.execute("SELECT COUNT(*) FROM Trainers WHERE trainer_id = ?", (trainer_id,))
        if self.db.cursor.fetchone()[0] == 0:
            QMessageBox.warning(self, "Validation Error", "Trainer does not exist")
            self.ui.lineEdit.setFocus()
            return None

        # Session title
        title = self.ui.lineEdit_2.text().strip()
        if not title:
            QMessageBox.warning(self, "Validation Error", "Session title cannot be empty")
            self.ui.lineEdit_2.setFocus()
            return None

        # Session date
        session_date_qdate = self.ui.dateEdit.date()
        today = QDate.currentDate()
        if session_date_qdate < today:
            QMessageBox.warning(self, "Validation Error", "Session date cannot be in the past")
            self.ui.dateEdit.setFocus()
            return None

        session_date = session_date_qdate.toString("yyyy-MM-dd")

        # Start and end times
        start_time = self.ui.timeEdit.time()
        end_time = self.ui.timeEdit_2.time()
        if end_time <= start_time:
            QMessageBox.warning(self, "Validation Error", "End time must be after start time")
            self.ui.timeEdit_2.setFocus()
            return None

        # Prevent adding a session for today if end time already passed
        if session_date_qdate == today:
            current_time = QTime.currentTime()
            if end_time <= current_time:
                QMessageBox.warning(self, "Validation Error", "Cannot add a session that already ended today")
                self.ui.timeEdit_2.setFocus()
                return None

        # Entry fee
        fee_text = self.ui.lineEdit_3.text().strip()
        try:
            fee = float(fee_text) if fee_text else 0.0
            if fee < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Entry fee must be a positive number")
            self.ui.lineEdit_3.setFocus()
            return None

        return {
            "trainer_id": trainer_id,
            "title": title,
            "session_date": session_date,
            "start_time": start_time.toString("HH:mm:ss"),
            "end_time": end_time.toString("HH:mm:ss"),
            "entry_fee": fee
        }

    def add_session(self):
        """Insert the session into the database"""
        data = self.validate_input()
        if not data:
            return

        try:
            query = """
            INSERT INTO WorkoutSessions (trainer_id, title, session_date, start_time, end_time, entry_fee)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            self.db.cursor.execute(query, (
                data["trainer_id"],
                data["title"],
                data["session_date"],
                data["start_time"],
                data["end_time"],
                data["entry_fee"]
            ))
            self.db.connection.commit()
            QMessageBox.information(self, "Success", "Workout session added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add session: {str(e)}")
