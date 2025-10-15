from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import QDate, QTime, QDateTime
from widgits.ui_salesReport import Ui_Dialog

class SalesSummaryDialog(QDialog):
    def __init__(self, parent=None, db=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = db

        # Connect Cancel / Go Back button
        self.ui.pushButton_4.clicked.connect(self.reject)

        # Update summary when dialog opens
        self.update_last_30_days_summary()

    def update_last_30_days_summary(self):
        try:
            # Rolling last 30 days
            today = QDate.currentDate()
            start_date = today.addDays(-30)
            end_date = today

            start_datetime = QDateTime(start_date, QTime(0, 0, 0))
            end_datetime = QDateTime(end_date, QTime(23, 59, 59))
            start_str = start_datetime.toString("yyyy-MM-dd HH:mm:ss")
            end_str = end_datetime.toString("yyyy-MM-dd HH:mm:ss")

            # Define income sources and corresponding labels
            sources = {
                'membership': self.ui.label_7,
                'supplies': self.ui.label_8,
                'joinedSession': self.ui.label_9,
                'ToolRS': self.ui.label_10
            }

            # Fetch totals for each income source
            for source, label in sources.items():
                query = """
                    SELECT SUM(amount)
                    FROM Income
                    WHERE source = ? AND income_date >= ? AND income_date <= ?
                """
                self.db.cursor.execute(query, (source, start_str, end_str))
                total = self.db.cursor.fetchone()[0] or 0
                label.setText(f"${float(total):.2f}")

            # Fetch total expenses
            query_exp = """
                SELECT SUM(amount)
                FROM Expenses
                WHERE expense_date >= ? AND expense_date <= ?
            """
            self.db.cursor.execute(query_exp, (start_str, end_str))
            expenses_total = self.db.cursor.fetchone()[0] or 0
            self.ui.label_11.setText(f"${float(expenses_total):.2f}")

            # Calculate total profit: sum of all incomes - expenses
            income_total = sum(
                float(label.text().replace('$', ''))
                for label in [self.ui.label_7, self.ui.label_8, self.ui.label_9, self.ui.label_10]
            )
            total_profit = income_total - float(expenses_total)
            self.ui.label_13.setText(f"${total_profit:.2f}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to calculate last 30 days summary:\n{str(e)}")
