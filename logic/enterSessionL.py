from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import QDate, Qt
from widgits.ui_enterSession import Ui_Dialog  # Replace with your actual UI
from datetime import datetime

class JoinSessionDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Load all sessions into the combo box
        self.load_sessions()

        # Connect combo box change
        self.ui.comboBox.currentIndexChanged.connect(self.update_session_info)

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.add_user_to_session)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)               # Cancel

    def load_sessions(self):
        """Load all available sessions into the combo box"""
        try:
            query = """
                SELECT session_id, title, start_time, end_time, entry_fee
                FROM WorkoutSessions
                ORDER BY session_date, start_time
            """
            self.db.cursor.execute(query)
            sessions = self.db.cursor.fetchall()

            self.sessions = {}  # Dictionary to store session info
            self.ui.comboBox.clear()
            for session in sessions:
                session_id, title, start_time, end_time, fee = session
                self.sessions[session_id] = {
                    "title": title,
                    "start_time": start_time,
                    "end_time": end_time,
                    "fee": fee
                }
                self.ui.comboBox.addItem(title, session_id)

            # Update info for the first session by default
            if sessions:
                self.update_session_info()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load sessions: {str(e)}")

    def update_session_info(self):
        """Update labels based on selected session"""
        session_id = self.ui.comboBox.currentData()
        if not session_id:
            return

        info = self.sessions.get(session_id)
        if not info:
            return

        self.ui.label_5.setText(info["title"])  # Session title
        self.ui.label_4.setText(f"Fee: ${info['fee']:.2f}")  # Fee
        self.ui.label_9.setText(info["start_time"].strftime("%I:%M %p"))  # Start time AM/PM
        self.ui.label_11.setText(info["end_time"].strftime("%I:%M %p"))   # End time AM/PM

    def validate_input(self):
        """Validate user input"""
        user_id_text = self.ui.lineEdit.text().strip()
        session_id = self.ui.comboBox.currentData()

        # Validate user_id
        if not user_id_text.isdigit():
            QMessageBox.warning(self, "Validation Error", "User ID must be a valid number")
            self.ui.lineEdit.setFocus()
            return None

        user_id = int(user_id_text)

        # Check if user exists
        self.db.cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id = ?", (user_id,))
        if self.db.cursor.fetchone()[0] == 0:
            QMessageBox.warning(self, "Validation Error", "User does not exist")
            self.ui.lineEdit.setFocus()
            return None

        # Check if session is selected
        if not session_id:
            QMessageBox.warning(self, "Validation Error", "Please select a session")
            return None

        return {"user_id": user_id, "session_id": session_id}

    def add_user_to_session(self):
        """Add user to the selected session and log income"""
        data = self.validate_input()
        if not data:
            return

        try:
            # Get session fee
            session_info = self.sessions.get(data["session_id"])
            fee = session_info["fee"] if session_info else 0.0

            # Insert into UserWorkoutSessions
            query = """
                INSERT INTO UserWorkoutSessions (user_id, session_id)
                VALUES (?, ?)
            """
            self.db.cursor.execute(query, (data["user_id"], data["session_id"]))
            self.db.connection.commit()

            # Insert into Income
            insert_income = """
                INSERT INTO Income (source, amount, income_date)
                VALUES (?, ?, ?)
            """
            self.db.cursor.execute(insert_income, ("joinedSession", fee, datetime.now()))
            self.db.connection.commit()

            QMessageBox.information(self, "Success", "User successfully joined the session!")
            self.accept()

        except Exception as e:
            if "UC_User_Session" in str(e):
                QMessageBox.warning(self, "Duplicate Entry", "User is already enrolled in this session.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to add user to session: {str(e)}")
