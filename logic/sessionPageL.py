from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Qt

class SessionsPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db

        # Placeholder for search input
        self.ui.lineEdit_4.setPlaceholderText("Search by Session ID")

        # Find the table in the sessions page
        self.table = self.ui.session.findChild(QTableWidget, "tableWidget_4")  # Replace with your table widget
        self.setup_table()
        self.load_sessions()

        # Connect search button
        self.ui.pushButton_18.clicked.connect(self.search_session_by_id)  # Replace with your search button

    def setup_table(self):
        headers = ["Session ID", "Title", "Trainer", "Date", "Start Time", "End Time", "Users", "Fee"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_sessions(self):
        """Load all sessions with trainer and enrolled users"""
        try:
            # Query to get session info, trainer info, fee, and enrolled users
            query = """
            SELECT ws.session_id, ws.title, t.trainer_id, t.name, ws.session_date, ws.start_time, ws.end_time, ws.entry_fee,
                   u.user_id, u.name
            FROM WorkoutSessions ws
            JOIN Trainers t ON ws.trainer_id = t.trainer_id
            LEFT JOIN UserWorkoutSessions uws ON ws.session_id = uws.session_id
            LEFT JOIN Users u ON uws.user_id = u.user_id
            ORDER BY ws.session_id DESC
            """
            self.db.cursor.execute(query)
            sessions = self.db.cursor.fetchall()
            self.populate_table(sessions)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load sessions: {str(e)}")

    def populate_table(self, sessions):
        """Fill the table with session data"""
        self.table.setRowCount(0)
        session_dict = {}

        # Group users per session
        for session in sessions:
            session_id, title, trainer_id, trainer_name, session_date, start_time, end_time, fee, user_id, user_name = session

            if session_id not in session_dict:
                session_dict[session_id] = {
                    "title": title,
                    "trainer": f"{trainer_name} (ID: {trainer_id})",
                    "date": session_date.strftime("%Y-%m-%d"),
                    "start_time": start_time.strftime("%I:%M %p"),
                    "end_time": end_time.strftime("%I:%M %p"),
                    "fee": f"${fee:.2f}" if fee else "$0.00",
                    "users": []
                }
            if user_id:
                session_dict[session_id]["users"].append(f"{user_name} (ID: {user_id})")

        # Populate table
        for row_num, (sid, data) in enumerate(session_dict.items()):
            self.table.insertRow(row_num)
            row_data = [
                sid,
                data["title"],
                data["trainer"],
                data["date"],
                data["start_time"],
                data["end_time"],
                ", ".join(data["users"]),
                data["fee"]
            ]

            for col_num, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value else "")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)

    def refresh(self):
        """Reload all sessions"""
        self.load_sessions()

    def search_session_by_id(self):
        """Search session by session_id from lineEdit_4"""
        session_id = self.ui.lineEdit_4.text().strip()

        if session_id == "":
            self.refresh()
            return

        if not session_id.isdigit():
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid numeric Session ID.")
            return

        try:
            query = """
            SELECT ws.session_id, ws.title, t.trainer_id, t.name, ws.session_date, ws.start_time, ws.end_time, ws.entry_fee,
                   u.user_id, u.name
            FROM WorkoutSessions ws
            JOIN Trainers t ON ws.trainer_id = t.trainer_id
            LEFT JOIN UserWorkoutSessions uws ON ws.session_id = uws.session_id
            LEFT JOIN Users u ON uws.user_id = u.user_id
            WHERE ws.session_id = ?
            """
            self.db.cursor.execute(query, (int(session_id),))
            sessions = self.db.cursor.fetchall()

            if sessions:
                self.populate_table(sessions)
            else:
                QMessageBox.information(None, "Not Found", f"No session found with ID {session_id}.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search sessions: {str(e)}")
