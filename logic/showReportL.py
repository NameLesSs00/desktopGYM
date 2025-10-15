from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Signal
from widgits.ui_reportCard import Ui_Dialog  # Replace with your actual UI file

def styled_message_box(title, text, icon=QMessageBox.Information, buttons=QMessageBox.Ok):
    """Create a styled message box with dark background and white text"""
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.setStandardButtons(buttons)
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #2e2e2e;
            color: white;
            font-size: 13px;
        }
        QPushButton {
            background-color: #444;
            color: white;
            border-radius: 5px;
            padding: 5px 15px;
        }
        QPushButton:hover {
            background-color: #555;
        }
    """)
    return msg

class ReportViewerDialog(QDialog):
    """
    Dialog to view a report in the Admin panel.
    Shows: Report ID, Employee Name, Date & Time, Title & Content.
    Supports deleting the report.
    Emits a signal when a report is deleted.
    """
    report_deleted = Signal()  # Signal to notify that a report was deleted

    def __init__(self, parent=None, db=None, report_id=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db
        self.report_id = report_id

        # Connect buttons
        self.ui.pushButton.clicked.connect(self.delete_report)  # Delete
        self.ui.pushButton_2.clicked.connect(self.close)        # Close

        # Load the report details
        self.load_report()

    def load_report(self):
        """Fetch report data from DB and populate labels"""
        if not self.report_id:
            msg = styled_message_box("Error", "No report ID provided", QMessageBox.Critical)
            msg.exec()
            self.reject()
            return

        try:
            query = """
            SELECT r.report_id, r.employee_id, e.name, r.title, r.content, r.report_date, r.report_time
            FROM Reports r
            JOIN Employees e ON r.employee_id = e.employee_id
            WHERE r.report_id = ?
            """
            self.db.cursor.execute(query, (self.report_id,))
            report = self.db.cursor.fetchone()

            if not report:
                msg = styled_message_box("Not Found", f"No report found with ID {self.report_id}", QMessageBox.Warning)
                msg.exec()
                self.reject()
                return

            report_id, employee_id, employee_name, title, content, report_date, report_time = report

            # Populate labels
            self.ui.label_2.setText(f"Report ID: {report_id}")
            self.ui.label_3.setText(f"From: {employee_name} (ID: {employee_id})")
            self.ui.label_4.setText(f"Date & Time: {report_date} {report_time}")
            self.ui.label_5.setText(f"Title: {title}\n\nContent:\n{content}")

        except Exception as e:
            msg = styled_message_box("Error", f"Failed to load report: {str(e)}", QMessageBox.Critical)
            msg.exec()
            print(f"Database error: {str(e)}")
            self.reject()

    def delete_report(self):
        """Delete the report from the database and emit a signal"""
        msg = styled_message_box(
            "Delete Report",
            "Are you sure you want to delete this report?",
            QMessageBox.Question,
            buttons=QMessageBox.Yes | QMessageBox.No
        )
        reply = msg.exec()

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.cursor.execute("DELETE FROM Reports WHERE report_id = ?", (self.report_id,))
                self.db.connection.commit()

                msg = styled_message_box("Deleted", "Report deleted successfully", QMessageBox.Information)
                msg.exec()

                # Emit signal to notify ReportsPage to refresh
                self.report_deleted.emit()

                self.accept()  # Close the dialog
            except Exception as e:
                msg = styled_message_box("Error", f"Failed to delete report: {str(e)}", QMessageBox.Critical)
                msg.exec()
                print(f"Database error: {str(e)}")
