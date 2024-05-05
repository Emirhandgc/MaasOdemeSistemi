import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QInputDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime, timedelta

class SalaryPaymentSystem(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maaş Ödeme Sistemi")
        self.setGeometry(100, 100, 800, 400)

        self.connection = sqlite3.connect("salary_system.db")
        self.cursor = self.connection.cursor()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Şirket bakiyesi görüntüleme
        company_balance_layout = QHBoxLayout()
        company_balance_layout.addWidget(QLabel("<b>Şirket Bakiyesi:</b>"))
        self.company_balance_label = QLabel()
        self.company_balance_label.setAlignment(Qt.AlignCenter)
        self.update_company_balance_label()
        company_balance_layout.addWidget(self.company_balance_label)
        layout.addLayout(company_balance_layout)

        # Şirket bakiyesi güncelleme
        update_balance_layout = QHBoxLayout()
        self.new_balance_input = QLineEdit()
        update_balance_layout.addWidget(self.new_balance_input)
        update_button = QPushButton("Bakiyeyi Güncelle")
        update_button.clicked.connect(self.update_company_balance)
        update_balance_layout.addWidget(update_button)
        layout.addLayout(update_balance_layout)

        # Departman seçimi
        department_layout = QHBoxLayout()
        department_layout.addWidget(QLabel("Departman:"))
        self.department_combobox = QComboBox()
        self.populate_departments()
        self.department_combobox.currentIndexChanged.connect(self.populate_employees)
        department_layout.addWidget(self.department_combobox)

        # 'Bütün Departmanlar' seçeneği ekleme
        self.department_combobox.addItem("Bütün Departmanlar")

        layout.addLayout(department_layout)

        # Çalışan tablosu
        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(4)
        self.employee_table.setHorizontalHeaderLabels(["Çalışan", "Departman", "Maaş Ödeme Günü", "IBAN"])
        layout.addWidget(self.employee_table)

        # Çalışan işlemleri düğmeleri
        employee_buttons_layout = QHBoxLayout()
        add_employee_button = QPushButton("Çalışan Ekle")
        add_employee_button.clicked.connect(self.add_employee)
        employee_buttons_layout.addWidget(add_employee_button)
        remove_employee_button = QPushButton("Çalışan Çıkar")
        remove_employee_button.clicked.connect(self.remove_employee)
        employee_buttons_layout.addWidget(remove_employee_button)
        edit_employee_button = QPushButton("Çalışan Bilgilerini Düzenle")
        edit_employee_button.clicked.connect(self.edit_employee)
        employee_buttons_layout.addWidget(edit_employee_button)
        layout.addLayout(employee_buttons_layout)

        # Maaş öde ve dekont gönder düğmeleri
        payment_buttons_layout = QHBoxLayout()
        pay_button = QPushButton("Maaş Öde")
        pay_button.clicked.connect(self.pay_salary)
        payment_buttons_layout.addWidget(pay_button)
        self.send_receipt_button = QPushButton("Dekont Gönder")
        self.send_receipt_button.setEnabled(False)
        self.send_receipt_button.clicked.connect(self.send_receipt)
        payment_buttons_layout.addWidget(self.send_receipt_button)
        layout.addLayout(payment_buttons_layout)

        self.setLayout(layout)

        # Departmanları ve çalışanları yükle
        self.populate_departments()
        self.populate_employees()

    def update_company_balance_label(self):
        self.cursor.execute("SELECT balance FROM company")
        balance = self.cursor.fetchone()[0]
        self.company_balance_label.setText("<b>{}</b>".format(balance))

    def update_company_balance(self):
        new_balance = int(self.new_balance_input.text())
        self.cursor.execute("UPDATE company SET balance=?", (new_balance,))
        self.connection.commit()
        self.update_company_balance_label()
        QMessageBox.information(self, "Bildiri", "Bakiye Güncellendi!")

    def populate_departments(self):
        self.department_combobox.clear()
        self.cursor.execute("SELECT name FROM departments")
        departments = self.cursor.fetchall()
        for department in departments:
            self.department_combobox.addItem(department[0])

    def populate_employees(self):
        department = self.department_combobox.currentText()
        if department == "Bütün Departmanlar":
            self.cursor.execute("SELECT name, department, payment_date, bank_account FROM employees")
        else:
            self.cursor.execute("SELECT name, department, payment_date, bank_account FROM employees WHERE department=?", (department,))
        employees = self.cursor.fetchall()

        self.employee_table.setRowCount(len(employees))
        self.employee_table.setColumnCount(4)

        for i, (name, department, payment_date, iban) in enumerate(employees):
            self.employee_table.setItem(i, 0, QTableWidgetItem(name))
            self.employee_table.setItem(i, 1, QTableWidgetItem(department))
            self.employee_table.setItem(i, 2, QTableWidgetItem(payment_date))
            self.employee_table.setItem(i, 3, QTableWidgetItem(iban))

    def add_employee(self):
        department = self.department_combobox.currentText()
        name, ok_pressed = QInputDialog.getText(self, "Çalışan Ekle", "Çalışan Adı:")
        if ok_pressed:
            iban, ok_pressed = QInputDialog.getText(self, "Çalışan Ekle", "Çalışan IBAN:")
            if ok_pressed:
                payment_date, ok_pressed = QInputDialog.getText(self, "Çalışan Ekle", "Çalışan Maaş Ödeme Tarihi (YYYY-MM-DD):")
                if ok_pressed:
                    self.cursor.execute("INSERT INTO employees (name, department, payment_date, bank_account) VALUES (?, ?, ?, ?)", (name, department, payment_date, iban))
                    self.connection.commit()
                    QMessageBox.information(self, "Başarılı", f"{name} adlı çalışan {department} departmanına eklendi.")
                    self.populate_employees()

    def remove_employee(self):
        current_row = self.employee_table.currentRow()
        if current_row != -1:
            reply = QMessageBox.question(self, 'Uyarı', 'Seçili çalışanı sistemden çıkarmak istediğinizden emin misiniz?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                name = self.employee_table.item(current_row, 0).text()
                self.cursor.execute("DELETE FROM employees WHERE name=?", (name,))
                self.connection.commit()
                QMessageBox.information(self, "Başarılı", f"{name} adlı çalışan sistemden çıkarıldı.")
                self.populate_employees()
        else:
            QMessageBox.warning(self, "Uyarı", "Çıkarılacak bir çalışanı seçiniz.")

    def edit_employee(self):
        current_row = self.employee_table.currentRow()
        if current_row != -1:
            name = self.employee_table.item(current_row, 0).text()
            new_name, ok_pressed = QInputDialog.getText(self, "Çalışan Bilgilerini Düzenle", "Yeni Çalışan Adı:", text=name)
            if ok_pressed:
                new_iban, ok_pressed = QInputDialog.getText(self, "Çalışan Bilgilerini Düzenle", "Yeni Çalışan IBAN:", text=self.employee_table.item(current_row, 3).text())
                if ok_pressed:
                    new_payment_date, ok_pressed = QInputDialog.getText(self, "Çalışan Bilgilerini Düzenle", "Yeni Çalışan Maaş Ödeme Tarihi (YYYY-MM-DD):", text=self.employee_table.item(current_row, 2).text())
                    if ok_pressed:
                        self.cursor.execute("UPDATE employees SET name=?, payment_date=?, bank_account=? WHERE name=?", (new_name, new_payment_date, new_iban, name))
                        self.connection.commit()
                        QMessageBox.information(self, "Başarılı", f"{name} adlı çalışanın bilgileri güncellendi.")
                        self.populate_employees()
        else:
            QMessageBox.warning(self, "Uyarı", "Düzenlenecek bir çalışanı seçiniz.")

    def pay_salary(self):
        department = self.department_combobox.currentText()
        if department == "Bütün Departmanlar":
            QMessageBox.warning(self, "Uyarı", "Lütfen bir departman seçiniz.")
            return

        self.cursor.execute("SELECT salary FROM departments WHERE name=?", (department,))
        salary = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT balance FROM company")
        current_balance = self.cursor.fetchone()[0]
        if current_balance < salary:
            QMessageBox.warning(self, "Uyarı", "Şirket bakiyesi yetersiz.")
        else:
            new_balance = current_balance - salary
            self.cursor.execute("UPDATE company SET balance=?", (new_balance,))
            self.connection.commit()
            QMessageBox.information(self, "Ödeme Başarılı", f"{department} departmanına {salary} TL maaş ödendi.")
            self.update_company_balance_label()
            self.send_receipt_button.setEnabled(True)

    def send_receipt(self):
        # Dekont gönderme işlemleri burada yapılabilir
        QMessageBox.information(self, "Dekont Gönderildi", "Dekont mail adresinize gönderilmiştir.")

if __name__ == "__main__":
    # Veritabanı bağlantısı oluşturma
    connection = sqlite3.connect("salary_system.db")
    cursor = connection.cursor()

    # Şirket tablosu oluşturma
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company (
        id INTEGER PRIMARY KEY,
        balance INTEGER
    )
    """)
    
    # Şirket bakiyesi oluşturma ve başlangıç değeri
    cursor.execute("INSERT INTO company (balance) VALUES (?)", (100000,))
    connection.commit()

    # Çalışanlar tablosu oluşturma
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        payment_date TEXT,
        bank_account TEXT
    )
    """)

    # Departmanlar tablosu oluşturma
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY,
        name TEXT,
        salary INTEGER
    )
    """)

    # Departmanların maaş bilgilerini ekleme
    departments_data = [
        ("Grafik Tasarımcı", 26000),
        ("Sosyal Medya Yöneticisi", 26000),
        ("Temizlik İşçisi", 17002),
        ("Ekip Lideri", 32000),
        ("Çaycı", 17002),
        ("Satış Pazarlamacı", 28000)
    ]

    cursor.executemany("INSERT INTO departments (name, salary) VALUES (?, ?)", departments_data)

    # Değişiklikleri kaydet ve bağlantıyı kapat
    connection.commit()
    connection.close()

    # Uygulamayı başlat
    app = QApplication(sys.argv)
    salary_system = SalaryPaymentSystem()
    salary_system.show()
    sys.exit(app.exec_())
