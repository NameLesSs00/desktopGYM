from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
from PySide6.QtCore import Qt

class TrainersPage:
    def __init__(self, ui, db):
        self.ui = ui
        self.db = db

        # Placeholder for search input
        self.ui.lineEdit_2.setPlaceholderText("Search by Trainer ID")

        # Find the table in the trainers page
        self.table = self.ui.trainers.findChild(QTableWidget, "tableWidget_2")
  # Adjust to your table name
        self.setup_table()
        self.load_trainers()

        # Connect search button
        self.ui.pushButton_9.clicked.connect(self.search_trainer_by_id)  # Adjust to your search button

    def setup_table(self):
        headers = ["ID", "Name", "Gender", "Phone", "Specialization"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def load_trainers(self):
        """Load all trainers"""
        try:
            query = """
            SELECT trainer_id, name, gender, phone, specialization
            FROM Trainers
            ORDER BY trainer_id DESC
            """
            self.db.cursor.execute(query)
            trainers = self.db.cursor.fetchall()
            self.populate_table(trainers)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load trainers: {str(e)}")

    def populate_table(self, trainers):
        """Fill the table with the given data"""
        self.table.setRowCount(0)
        for row_num, trainer in enumerate(trainers):
            self.table.insertRow(row_num)
            trainer_id, name, gender, phone, specialization = trainer

            for col_num, value in enumerate([trainer_id, name, gender, phone, specialization]):
                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_num, col_num, item)

    def refresh(self):
        """Reload all trainers"""
        self.load_trainers()

    def search_trainer_by_id(self):
        """Search trainer by trainer_id from lineEdit_2"""
        trainer_id = self.ui.lineEdit_2.text().strip()
        if trainer_id == "":
            self.refresh()
            return

        if not trainer_id.isdigit():
            QMessageBox.warning(None, "Invalid Input", "Please enter a valid numeric Trainer ID.")
            return

        try:
            query = """
            SELECT trainer_id, name, gender, phone, specialization
            FROM Trainers
            WHERE trainer_id = ?
            """
            self.db.cursor.execute(query, (int(trainer_id),))
            trainers = self.db.cursor.fetchall()

            if trainers:
                self.populate_table(trainers)
            else:
                QMessageBox.information(None, "Not Found", f"No trainer found with ID {trainer_id}.")
                self.table.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to search trainer: {str(e)}")
