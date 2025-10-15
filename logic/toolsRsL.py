from PySide6.QtWidgets import QDialog, QMessageBox
from widgits.ui_toolsRS import Ui_Dialog  # Replace with your actual UI file
from PySide6.QtCore import QTime, QDate
from datetime import datetime

class AddToolReservationDialog(QDialog):
    HOUR_COST = 5  # $5 per hour

    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Load tools into combo box
        self.load_tools()

        # Connect buttons
        self.ui.pushButton_5.clicked.connect(self.add_reservation)  # Done
        self.ui.pushButton_4.clicked.connect(self.reject)           # Cancel

        # Connect time edits to recalc cost
        self.ui.timeEdit.timeChanged.connect(self.calculate_cost)
        self.ui.timeEdit_2.timeChanged.connect(self.calculate_cost)

        # Set default date
        self.ui.dateEdit.setDate(QDate.currentDate())

    def load_tools(self):
        """Load all tool names into the combo box"""
        try:
            query = "SELECT tool_id, name FROM Tools"
            self.db.cursor.execute(query)
            tools = self.db.cursor.fetchall()
            self.ui.comboBox.clear()
            for tool_id, name in tools:
                self.ui.comboBox.addItem(name, tool_id)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tools: {str(e)}")

    def calculate_cost(self):
        """Calculate reserved hours and cost"""
        start_time = self.ui.timeEdit.time()
        end_time = self.ui.timeEdit_2.time()

        start_seconds = start_time.hour() * 3600 + start_time.minute() * 60
        end_seconds = end_time.hour() * 3600 + end_time.minute() * 60

        if end_seconds <= start_seconds:
            self.ui.label_8.setText("Invalid time range")
            return

        hours = (end_seconds - start_seconds) / 3600
        total_cost = hours * self.HOUR_COST
        self.ui.label_8.setText(f"That will cost: ${total_cost:.2f}")

    def validate_input(self):
        """Validate the input fields"""
        user_id_text = self.ui.lineEdit.text().strip()
        tool_index = self.ui.comboBox.currentIndex()
        reservation_date = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        start_time = self.ui.timeEdit.time()
        end_time = self.ui.timeEdit_2.time()

        # Validate user_id
        if not user_id_text.isdigit():
            QMessageBox.warning(self, "Validation Error", "User ID must be a valid number")
            self.ui.lineEdit.setFocus()
            return None

        user_id = int(user_id_text)

        # Check user exists
        self.db.cursor.execute("SELECT COUNT(*) FROM Users WHERE user_id = ?", (user_id,))
        if self.db.cursor.fetchone()[0] == 0:
            QMessageBox.warning(self, "Validation Error", "User does not exist")
            self.ui.lineEdit.setFocus()
            return None

        # Check tool selected
        if tool_index < 0:
            QMessageBox.warning(self, "Validation Error", "Please select a tool")
            return None

        tool_id = self.ui.comboBox.currentData()

        # Check time validity
        start_seconds = start_time.hour() * 3600 + start_time.minute() * 60
        end_seconds = end_time.hour() * 3600 + end_time.minute() * 60
        if end_seconds <= start_seconds:
            QMessageBox.warning(self, "Validation Error", "End time must be after start time")
            return None

        hours = (end_seconds - start_seconds) / 3600
        total_cost = hours * self.HOUR_COST

        return {
            'user_id': user_id,
            'tool_id': tool_id,
            'reservation_date': reservation_date,
            'start_time': start_time.toString("HH:mm:ss"),
            'end_time': end_time.toString("HH:mm:ss"),
            'hours': hours,
            'total_cost': total_cost
        }

    def add_reservation(self):
        """Insert reservation into database with overlap check and log income"""
        data = self.validate_input()
        if not data:
            return

        try:
            # Check for overlapping reservations
            overlap_query = """
            SELECT COUNT(*)
            FROM ToolReservations
            WHERE tool_id = ?
              AND reservation_date = ?
              AND (
                    (start_time < ? AND end_time > ?)  -- overlaps start
                 OR (start_time < ? AND end_time > ?)  -- overlaps end
                 OR (start_time >= ? AND end_time <= ?) -- fully inside
              )
            """
            self.db.cursor.execute(overlap_query, (
                data['tool_id'],
                data['reservation_date'],
                data['end_time'], data['start_time'],
                data['end_time'], data['start_time'],
                data['start_time'], data['end_time']
            ))
            if self.db.cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Conflict", "This tool is already reserved during the selected time.")
                return

            # Insert reservation
            insert_query = """
            INSERT INTO ToolReservations (user_id, tool_id, reservation_date, start_time, end_time)
            VALUES (?, ?, ?, ?, ?)
            """
            self.db.cursor.execute(insert_query, (
                data['user_id'],
                data['tool_id'],
                data['reservation_date'],
                data['start_time'],
                data['end_time']
            ))
            self.db.connection.commit()

            # Log income
            income_query = """
                INSERT INTO Income (source, amount, income_date)
                VALUES (?, ?, ?)
            """
            self.db.cursor.execute(income_query, ("toolRS", data['total_cost'], datetime.now()))
            self.db.connection.commit()

            QMessageBox.information(self, "Success", f"Reservation added! Total cost: ${data['total_cost']:.2f}")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add reservation: {str(e)}")
