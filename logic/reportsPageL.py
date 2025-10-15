from PySide6.QtWidgets import QTableWidgetItem, QPushButton, QHeaderView, QMessageBox, QTableWidget
from PySide6.QtCore import Qt
from logic.showReportL import ReportViewerDialog  # Make sure this is your dialog

class ReportsPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db

        # Placeholder for search input (adjust lineEdit name)
        self.ui.lineEdit_2.setPlaceholderText("Search by Report ID")

        # Find the table
        self.table = self.ui.reports.findChild(QTableWidget, "tableWidget_2")
        self.setup_table()
        self.load_reports()

        # Connect search button (adjust pushButton name)
        self.ui.pushButton_9.clicked.connect(self.search_report_by_id)

    def setup_table(self):
        """Setup table headers and behavior"""
        headers = ["Report ID", "Employee Name & ID", "Title", "Content", "Date & Time", "Action"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_reports(self):
        """Load all reports from the database"""
        try:
            query = """
            SELECT r.report_id, e.name, e.employee_id, r.title, r.content, r.report_date, r.report_time
            FROM Reports r
            JOIN Employees e ON r.employee_id = e.employee_id
            ORDER BY r.report_id DESC
            """
            self.db.cursor.execute(query)
            reports = self.db.cursor.fetchall()
            self.populate_table(reports)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load reports: {str(e)}")

    def populate_table(self, reports):
        """Fill the table with report data"""
        self.table.setRowCount(0)
        for row_num, report in enumerate(reports):
            self.table.insertRow(row_num)
            report_id, employee_name, employee_id, title, content, report_date, report_time = report

            # Fill table items
            for col_num, value in enumerate([
                report_id,
                f"{employee_name} (ID: {employee_id})",
                title,
                content,
                f"{report_date} {report_time}"
            ]):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)

            # Action column: Show button
            btn_show = QPushButton("Show")
            btn_show.clicked.connect(self.make_show_handler(report_id))
            self.table.setCellWidget(row_num, 5, btn_show)

    def make_show_handler(self, report_id):
        """Return a function that opens the report dialog with the correct report_id"""
        def handler():
            self.show_report(report_id)
        return handler

    def show_report(self, report_id):
        """Open the report viewer dialog and refresh table if deleted"""
        dialog = ReportViewerDialog(self.ui.reports, self.db, report_id)
        dialog.report_deleted.connect(self.refresh)  # Refresh table on deletion
        dialog.exec()

    def refresh(self):
        """Reload table"""
        self.load_reports()

    def search_report_by_id(self):
        """Search report by report_id from lineEdit_2"""
        report_id = self.ui.lineEdit_2.text().strip()

        if report_id == "":
            self.refresh()
            return

        if not report_id.isdigit():
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid numeric Report ID.")
            return

        try:
            query = """
            SELECT r.report_id, e.name, e.employee_id, r.title, r.content, r.report_date, r.report_time
            FROM Reports r
            JOIN Employees e ON r.employee_id = e.employee_id
            WHERE r.report_id = ?
            """
            self.db.cursor.execute(query, (int(report_id),))
            reports = self.db.cursor.fetchall()

            if reports:
                self.populate_table(reports)
            else:
                QMessageBox.information(None, "Not Found", f"No report found with ID {report_id}.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search report: {str(e)}")
