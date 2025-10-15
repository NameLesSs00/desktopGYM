from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Qt
from datetime import datetime

class ToolsPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db

        # Placeholder for search input
        self.ui.lineEdit_3.setPlaceholderText("Search by Tool ID or Name")

        # Find the table in the tools page (correct parent widget name)
        self.table = self.ui.toolRs.findChild(QTableWidget, "tableWidget_3")
        self.setup_table()
        self.load_tools()

        # Connect search button
        self.ui.pushButton_15.clicked.connect(self.search_tool)

    def setup_table(self):
        headers = ["Tool ID", "Name", "Tag Name", "Reserved By", "Reservation Date", "From - Till"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_tools(self):
        """Load all tools with reservation info"""
        try:
            query = """
            SELECT t.tool_id, t.name, t.tag_name,
                   u.user_id, u.name, tr.reservation_date, tr.start_time, tr.end_time
            FROM Tools t
            LEFT JOIN ToolReservations tr ON t.tool_id = tr.tool_id
            LEFT JOIN Users u ON tr.user_id = u.user_id
            ORDER BY t.tool_id DESC
            """
            self.db.cursor.execute(query)
            tools = self.db.cursor.fetchall()
            self.populate_table(tools)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load tools: {str(e)}")

    def populate_table(self, tools):
        """Fill the table with the given data (12-hour AM/PM format for times)"""
        self.table.setRowCount(0)
        for row_num, tool in enumerate(tools):
            self.table.insertRow(row_num)
            tool_id, name, tag_name, user_id, user_name, res_date, start_time, end_time = tool

            reserved_by = f"{user_name} (ID: {user_id})" if user_id else ""
            reservation_date = res_date.strftime("%Y-%m-%d") if res_date else ""
            from_till = ""
            if start_time and end_time:
                from_till = f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}"  # 12-hour format

            row_data = [tool_id, name, tag_name, reserved_by, reservation_date, from_till]
            for col_num, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)

    def refresh(self):
        """Reload all tools"""
        self.load_tools()

    def search_tool(self):
        """Search tool by tool_id or name"""
        keyword = self.ui.lineEdit_3.text().strip()
        if keyword == "":
            self.refresh()
            return

        try:
            if keyword.isdigit():
                query = """
                SELECT t.tool_id, t.name, t.tag_name,
                       u.user_id, u.name, tr.reservation_date, tr.start_time, tr.end_time
                FROM Tools t
                LEFT JOIN ToolReservations tr ON t.tool_id = tr.tool_id
                LEFT JOIN Users u ON tr.user_id = u.user_id
                WHERE t.tool_id = ?
                ORDER BY t.tool_id DESC
                """
                self.db.cursor.execute(query, (int(keyword),))
            else:
                query = """
                SELECT t.tool_id, t.name, t.tag_name,
                       u.user_id, u.name, tr.reservation_date, tr.start_time, tr.end_time
                FROM Tools t
                LEFT JOIN ToolReservations tr ON t.tool_id = tr.tool_id
                LEFT JOIN Users u ON tr.user_id = u.user_id
                WHERE t.name LIKE ?
                ORDER BY t.tool_id DESC
                """
                self.db.cursor.execute(query, (f"%{keyword}%",))

            tools = self.db.cursor.fetchall()

            if tools:
                self.populate_table(tools)
            else:
                QMessageBox.information(None, "Not Found", f"No tools found for '{keyword}'.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search tools: {str(e)}")
