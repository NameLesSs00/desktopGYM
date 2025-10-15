import sys
import os
import configparser

# Determine the correct path for config.ini
if getattr(sys, 'frozen', False):
    # Running as .exe
    base_path = sys._MEIPASS
else:
    # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(base_path, "config.ini")

if not os.path.exists(config_path):
    raise FileNotFoundError(f"config.ini not found at {config_path}")

config = configparser.ConfigParser()
config.read(config_path)

secret_key = config.get("APP", "SECRET_KEY")



from PySide6.QtWidgets import QApplication, QStackedWidget, QMainWindow, QMessageBox , QLabel 
from PySide6.QtGui import QPixmap, Qt

from logic.LoginL import LoginWindow
from logic.expensesPageL import ExpensesPage
from widgits.ui_adminMain import Ui_MainWindow1 as Ui_Admin
from widgits.ui_helpDeskMain import Ui_MainWindow as Ui_HelpDesk
from widgits.ui_cashierMain import Ui_MainWindow as Ui_CashierMain

from db import DatabaseConnection
from PySide6.QtGui import QIcon

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(BASE_PATH, "iconImage.ico") 
app = QApplication([])
app.setWindowIcon(QIcon(icon_path))
app.setApplicationName("Gym System")
stack = QStackedWidget()

# ---------- Database Connection ----------

db = DatabaseConnection()
if not db.connection or not db.cursor:
    QMessageBox.critical(None, "Error", "Failed to connect to database!")
    sys.exit(1)



# ---------- Styles ----------

NORMAL_STYLE = """
QPushButton {
    background-color: black;
    color: white;
    border-radius: 20px;
    border: none;
    padding: 5px 12px;
}
QPushButton:hover {
    background-color: #333333;
}
QPushButton:pressed {
    background-color: #555555;
}
"""

ACTIVE_STYLE = """
QPushButton {
    background-color: #007ACC;
    color: white;
    border-radius: 20px;
    border: none;
    padding: 5px 12px;
}
"""

# ---------- Pages ----------
admin_page = QMainWindow()
admin_ui = Ui_Admin()
admin_ui.setupUi(admin_page)

helpdesk_page = QMainWindow()
helpdesk_ui = Ui_HelpDesk()
helpdesk_ui.setupUi(helpdesk_page)

cashier_page = QMainWindow()
cashier_ui = Ui_CashierMain()
cashier_ui.setupUi(cashier_page)

ADMIN_NAV = [
    admin_ui.pushButton_2,  # Sales
    admin_ui.pushButton_3,  # Employee
    admin_ui.pushButton_10, # Expenses
    admin_ui.pushButton_5,  # Reports
    admin_ui.pushButton_6,  # HelpDesk
    admin_ui.pushButton_4,  # Cashier
]
HELPDESK_NAV = [
    helpdesk_ui.pushButton_3,  # Users
    helpdesk_ui.pushButton_5,  # Trainers
    helpdesk_ui.pushButton_11, # Session
    helpdesk_ui.pushButton_6   # Tools
]
CASHIER_NAV = [
    cashier_ui.pushButton_7,  # Main (Cashier work)
    cashier_ui.pushButton_3,  # Goods
    cashier_ui.pushButton_5,  # Suppliers
]

login_page = LoginWindow(
    db=db,
    stack=stack,
    admin_page=admin_page,
    cashier_page=cashier_page,
    helpdesk_page=helpdesk_page,
    admin_ui=admin_ui,
    cashier_ui=cashier_ui,
    helpdesk_ui=helpdesk_ui,
    ADMIN_NAV=ADMIN_NAV,
    CASHIER_NAV=CASHIER_NAV,
    HELPDESK_NAV=HELPDESK_NAV,
    NORMAL_STYLE=NORMAL_STYLE,
    ACTIVE_STYLE=ACTIVE_STYLE
)

#Instance

from logic.employeePageL import EmployeesPage
employees_page = EmployeesPage(admin_ui, db, current_system_user_id=None)

from logic.goodsPageL import GoodsPage
goods_page = GoodsPage(cashier_ui, db)       

from logic.salePointL import SalePointPage
sale_point_page = SalePointPage(cashier_ui, db)

from logic.suppliersPageL import SuppliersPage
suppliers_page = SuppliersPage(cashier_ui, db)

from logic.addSameGoodL import AddSameGoodDialog
add_same_good_dialog = AddSameGoodDialog(db=db)


from logic.expensesPageL import ExpensesPage
expenses_page = ExpensesPage(admin_ui, db)  

from logic.reportsPageL import ReportsPage
reports_page = ReportsPage(admin_ui, db)

from logic.salesPageL import SalesPage
sales_page = SalesPage(admin_ui, db)


from logic.trainerPageL import TrainersPage
trainers_page = TrainersPage(helpdesk_ui, db)

from logic.usersPageL import UsersPage
users_page = UsersPage(helpdesk_ui, db)

from logic.toolsPageL import ToolsPage
tools_page = ToolsPage(helpdesk_ui, db)

from logic.sessionPageL import SessionsPage  
sessions_page = SessionsPage(helpdesk_ui, db)

current_system_user_id = None
current_employee_id = None

def on_login_success(success):
    global current_system_user_id, current_employee_id
    if success:
        current_system_user_id = login_page.get_logged_system_user_id()
        current_employee_id = login_page.get_logged_employee_id()

        employees_page.current_system_user_id = current_system_user_id
        employees_page.refresh()  

login_page.login_success.connect(on_login_success)

stack.addWidget(login_page)
stack.addWidget(admin_page)
stack.addWidget(helpdesk_page)
stack.addWidget(cashier_page)

# ---------- Nav groups ----------
def set_active_admin(active_btn=None):
    for b in ADMIN_NAV:
        b.setStyleSheet(NORMAL_STYLE)
    if active_btn is not None:
        active_btn.setStyleSheet(ACTIVE_STYLE)

def set_active_helpdesk(active_btn=None):
    for b in HELPDESK_NAV:
        b.setStyleSheet(NORMAL_STYLE)
    if active_btn is not None:
        active_btn.setStyleSheet(ACTIVE_STYLE)

def set_active_cashier(active_btn=None):
    for b in CASHIER_NAV:
        b.setStyleSheet(NORMAL_STYLE)
    if active_btn is not None:
        active_btn.setStyleSheet(ACTIVE_STYLE)

# ---------- Navigation ----------
def logout():
    # Create a custom message box
    msg_box = QMessageBox(admin_page)
    msg_box.setWindowTitle("Logout")
    msg_box.setText("Are you sure you want to logout?")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg_box.setDefaultButton(QMessageBox.StandardButton.No)

    # Load the image
    pixmap = QPixmap(r"C:\Users\b\Pictures\Screenshots\Screenshot 2025-08-29 195904.png")

    # Create a label for the pixmap
    label = QLabel()
    label.setPixmap(pixmap)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setScaledContents(True)

    # Add the label to the QMessageBox layout
    layout = msg_box.layout()
    layout.addWidget(label, 0, 1)  # add it to the second column, top row

    reply = msg_box.exec()

    if reply == QMessageBox.StandardButton.Yes:
        stack.setCurrentWidget(login_page)
        set_active_admin(None)
        set_active_helpdesk(None)
        set_active_cashier(None)

def open_helpdesk():
    stack.setCurrentWidget(helpdesk_page)
    helpdesk_ui.stackedWidget.setCurrentWidget(helpdesk_ui.users)
    set_active_admin(admin_ui.pushButton_6)
    set_active_helpdesk(helpdesk_ui.pushButton_3)
    set_active_cashier(None)

def open_cashier():
    stack.setCurrentWidget(cashier_page)
    cashier_ui.stackedWidget.setCurrentWidget(cashier_ui.cashierWork)  # Main cashier work area
    set_active_admin(admin_ui.pushButton_4)
    set_active_cashier(cashier_ui.pushButton_7)  # Main cashier work button
    set_active_helpdesk(None)

def go_admin_sales():
    admin_ui.stackedWidget.setCurrentWidget(admin_ui.sales)
    set_active_admin(admin_ui.pushButton_2)
    set_active_helpdesk(None)
    set_active_cashier(None)
    # This will reload all income records properly
    sales_page.refresh()



def go_admin_employee():
    admin_ui.stackedWidget.setCurrentWidget(admin_ui.employee)
    set_active_admin(admin_ui.pushButton_3)
    set_active_helpdesk(None)
    set_active_cashier(None)
    employees_page.refresh()  


def go_admin_expenses():
    admin_ui.stackedWidget.setCurrentWidget(admin_ui.expenses)
    set_active_admin(admin_ui.pushButton_10)
    set_active_helpdesk(None)
    set_active_cashier(None)
    expenses_page.refresh() 

def go_admin_reports():
    admin_ui.stackedWidget.setCurrentWidget(admin_ui.reports)
    set_active_admin(admin_ui.pushButton_5)
    set_active_helpdesk(None)
    set_active_cashier(None)
    # Refresh the reports table
    reports_page.refresh()


def go_admin_from_helpdesk():
    stack.setCurrentWidget(admin_page)
    admin_ui.stackedWidget.setCurrentWidget(admin_ui.sales)
    set_active_admin(admin_ui.pushButton_2)
    set_active_helpdesk(None)
    set_active_cashier(None)
    sales_page.refresh()

def go_admin_from_cashier():
    stack.setCurrentWidget(admin_page)
    admin_ui.stackedWidget.setCurrentWidget(admin_ui.sales)
    set_active_admin(admin_ui.pushButton_2)
    set_active_helpdesk(None)
    set_active_cashier(None)
    sales_page.refresh()

def go_cashier_main():
    cashier_ui.stackedWidget.setCurrentWidget(cashier_ui.cashierWork)
    set_active_cashier(cashier_ui.pushButton_7)

def go_cashier_goods():
    cashier_ui.stackedWidget.setCurrentWidget(cashier_ui.goods)
    set_active_cashier(cashier_ui.pushButton_3)
    goods_page.refresh()  # Refresh the goods table when switching to the page

def go_cashier_suppliers():
    cashier_ui.stackedWidget.setCurrentWidget(cashier_ui.suppliers)
    set_active_cashier(cashier_ui.pushButton_5)
    suppliers_page.refresh()

def go_helpdesk_users():
    helpdesk_ui.stackedWidget.setCurrentWidget(helpdesk_ui.users)
    set_active_helpdesk(helpdesk_ui.pushButton_3)

def go_helpdesk_trainers():
    helpdesk_ui.stackedWidget.setCurrentWidget(helpdesk_ui.trainers)
    set_active_helpdesk(helpdesk_ui.pushButton_5)

def go_helpdesk_session():
    helpdesk_ui.stackedWidget.setCurrentWidget(helpdesk_ui.session)
    set_active_helpdesk(helpdesk_ui.pushButton_11)

def go_helpdesk_tools():
    helpdesk_ui.stackedWidget.setCurrentWidget(helpdesk_ui.toolRs)
    set_active_helpdesk(helpdesk_ui.pushButton_6)

# ---------- Dialog Functions ----------
def show_add_supplier_dialog():
    from logic.addSupplierL import AddSupplierDialog
    dialog = AddSupplierDialog(cashier_page, db)
    if dialog.exec():  
        suppliers_page.refresh()

def show_add_good_dialog():
    from logic.addGoodL import AddGoodDialog
    dialog = AddGoodDialog(cashier_page, db)
    if dialog.exec():
        goods_page.refresh()  

def open_add_same_good():
    from logic.addSameGoodL import AddSameGoodDialog
    dialog = AddSameGoodDialog(None, db)  
    if dialog.exec():
        goods_page.refresh() 

def show_add_expense_dialog():
    from logic.addExpensesL import AddExpensesDialog
    dialog = AddExpensesDialog(cashier_page, db)
    if dialog.exec():
        expenses_page.refresh()  

def show_add_employee_dialog():
    from logic.addEmployeeL import AddEmployeeDialog
    dialog = AddEmployeeDialog(admin_page, db)
    if dialog.exec():  
        employees_page.refresh()  

def show_add_system_user_dialog():
    from logic.addSystemUserL import AddSystemUserDialog
    dialog = AddSystemUserDialog(admin_page, db) 
    if dialog.exec():
        employees_page.refresh()

def show_add_tool_dialog():
    from logic.addToolL import AddToolDialog
    dialog = AddToolDialog(admin_page, db)  
    dialog.exec()  
    
def show_add_trainer_dialog():
    from logic.addTrainerL import AddTrainerDialog
    dialog = AddTrainerDialog(admin_page, db)
    if dialog.exec():  
        trainers_page.refresh()  

def show_sales_report_dialog():
    from logic.getSalesL import SalesSummaryDialog
    dialog = SalesSummaryDialog(admin_page, db)
    dialog.exec()

def show_add_report_dialog():
    from logic.addReportL import AddReportDialog
    dialog = AddReportDialog(helpdesk_page, db, current_employee_id)  
    if dialog.exec():  
        reports_page.refresh()  

def show_add_tool_reservation_dialog():
    from logic.toolsRsL import AddToolReservationDialog
    dialog = AddToolReservationDialog(helpdesk_page, db) 
    if dialog.exec():  
        tools_page.refresh()  

# --- Show Add User Dialog ---
def show_add_user_dialog():
    from logic.addUserL import AddUserDialog
    dialog = AddUserDialog(helpdesk_page, db)
    if dialog.exec():  
        users_page.refresh() 

def show_buy_membership_dialog():
    from logic.buyMembershipsL import BuyMembershipDialog
    dialog = BuyMembershipDialog(helpdesk_page, db)
    if dialog.exec():  
        users_page.refresh()  
        
def show_add_report_dialog(current_employee_id): 
    from logic.addReportL import AddReportDialog
    dialog = AddReportDialog(helpdesk_page, db, current_employee_id)
    dialog.exec()

def show_add_tool_dialog():
    from logic.addToolL import AddToolDialog  # Adjust to your actual dialog
    dialog = AddToolDialog(helpdesk_page, db)
    if dialog.exec():  # Only refresh if user clicked "Done"
        tools_page.refresh()  # Refresh the table to show new/updated tool

def show_add_session_dialog():
    from logic.addSessionL import AddSessionDialog
    dialog = AddSessionDialog(helpdesk_page, db)
    if dialog.exec():  # Only refresh if a session was added
        sessions_page.refresh()

def show_join_session_dialog():
    from logic.enterSessionL import JoinSessionDialog
    dialog = JoinSessionDialog(helpdesk_page, db)
    if dialog.exec():  # Only refresh if a user joined a session
        sessions_page.refresh()

# ---------- Connect Buttons ----------
# Admin Page
# Navigation
admin_ui.pushButton_2.clicked.connect(go_admin_sales)     # Sales
admin_ui.pushButton_3.clicked.connect(go_admin_employee)  # Employee
admin_ui.pushButton_10.clicked.connect(go_admin_expenses) # Expenses
admin_ui.pushButton_5.clicked.connect(go_admin_reports)   # Reports
admin_ui.pushButton_6.clicked.connect(open_helpdesk)      # Help Desk
admin_ui.pushButton_4.clicked.connect(open_cashier)       # Cashier
admin_ui.pushButton.clicked.connect(logout)               # Logout
admin_ui.pushButton_14.clicked.connect(show_add_expense_dialog) #add expandes
admin_ui.pushButton_16.clicked.connect(show_add_employee_dialog) #add employee
admin_ui.pushButton_17.clicked.connect(show_add_system_user_dialog) #add system user
admin_ui.pushButton_8.clicked.connect(show_sales_report_dialog) #add employee

show_sales_report_dialog

# HelpDesk Page
# Navigation
helpdesk_ui.pushButton_3.clicked.connect(go_helpdesk_users)      # Users
helpdesk_ui.pushButton_5.clicked.connect(go_helpdesk_trainers)   # Trainers
helpdesk_ui.pushButton_11.clicked.connect(go_helpdesk_session)   # Session
helpdesk_ui.pushButton_4.clicked.connect(go_admin_from_helpdesk) # Main/Admin
helpdesk_ui.pushButton.clicked.connect(logout)                    # Logout
helpdesk_ui.pushButton_13.clicked.connect(show_add_tool_dialog) # add tool
helpdesk_ui.pushButton_14.clicked.connect(show_add_tool_reservation_dialog) # add toolrs 
helpdesk_ui.pushButton_6.clicked.connect(go_helpdesk_tools)      # Tools
helpdesk_ui.pushButton_8.clicked.connect(show_add_user_dialog)      # add user
helpdesk_ui.pushButton_12.clicked.connect(show_buy_membership_dialog)      # buy membershipe

# Button connection for adding report (HelpDesk)
helpdesk_ui.pushButton_2.clicked.connect(
    lambda: show_add_report_dialog(current_employee_id)
)
helpdesk_ui.pushButton_16.clicked.connect(show_add_session_dialog)      # add user

helpdesk_ui.pushButton_17.clicked.connect(show_join_session_dialog) # enter session



# Cashier Page
cashier_ui.pushButton.clicked.connect(logout)                       # Logout
cashier_ui.pushButton_4.clicked.connect(go_admin_from_cashier)     # Admin main
cashier_ui.pushButton_3.clicked.connect(go_cashier_goods)          # Goods
cashier_ui.pushButton_5.clicked.connect(go_cashier_suppliers)      # Suppliers
cashier_ui.pushButton_7.clicked.connect(go_cashier_main)           # Main (Cashier work)
cashier_ui.pushButton_10.clicked.connect(show_add_good_dialog)     # Add new good
cashier_ui.pushButton_11.clicked.connect(show_add_supplier_dialog) # Add new supplier
cashier_ui.pushButton_2.clicked.connect(
    lambda: show_add_report_dialog(current_employee_id)
)
cashier_ui.pushButton_8.clicked.connect(open_add_same_good)#  add same good


def show_add_supplier_dialog():
    from logic.addSupplierL import AddSupplierDialog
    dialog = AddSupplierDialog(cashier_page, db)
    if dialog.exec():
        suppliers_page.refresh() 

# ---------- Initialize Nav groups ----------

# Initialize all buttons with normal style

for btn in ADMIN_NAV + HELPDESK_NAV + CASHIER_NAV:
    btn.setStyleSheet(NORMAL_STYLE)

# ---------- Show App ----------
stack.showMaximized()  # This will make the window take up the full screen
#app.exec()


main_window = QMainWindow()
main_window.setWindowTitle("Gym System")  # Title for the taskbar
main_window.setWindowIcon(QIcon(icon_path))  # Icon for the taskbar
main_window.setCentralWidget(stack)  # Put your stacked widget inside
main_window.showMaximized()  # Show maximized

# ---------- Run the application ----------
app.exec()