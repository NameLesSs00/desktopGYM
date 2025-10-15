from PySide6.QtWidgets import QDialog, QMessageBox
from datetime import date, datetime
from widgits.ui_addReport import Ui_Dialog  # Replace with your actual UI file

class AddReportDialog(QDialog):
    def __init__(self, parent=None, db=None, employee_id=None):
        """
        :param parent: Parent QWidget (e.g., helpdesk_ui)
        :param db: Database connection object
        :param employee_id: Currently logged-in employee's ID (foreign key)
        """
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db
        self.employee_id = employee_id

        # Connect buttons
        self.ui.pushButton_3.clicked.connect(self.add_report)  # Done
        self.ui.pushButton_2.clicked.connect(self.reject)      # Cancel

    def validate_input(self):
        """Check title and content fields"""
        title = self.ui.lineEdit.text().strip()
        content = self.ui.textEdit.toPlainText().strip()

        if not title:
            QMessageBox.warning(self, "Validation Error", "Title is required")
            self.ui.lineEdit.setFocus()
            return None

        if not content:
            QMessageBox.warning(self, "Validation Error", "Content cannot be empty")
            self.ui.textEdit.setFocus()
            return None

        return {
            "title": title,
            "content": content
        }

    def add_report(self):
        """Insert a new report into the Reports table"""
        data = self.validate_input()
        if not data:
            return

        try:
            # Ensure we have a valid employee_id
            if not self.employee_id:
                QMessageBox.critical(self, "Error", "No employee ID provided")
                return

            # Prepare SQL insert
            insert_query = """
            INSERT INTO Reports (employee_id, title, content, report_date, report_time)
            VALUES (?, ?, ?, ?, ?)
            """
            today_date = date.today()
            current_time = datetime.now().time()

            self.db.cursor.execute(insert_query, (
                self.employee_id,
                data["title"],
                data["content"],
                today_date,
                current_time
            ))
            self.db.connection.commit()

            QMessageBox.information(self, "Success", "Report added successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add report: {str(e)}")
            print(f"Database error: {str(e)}")
