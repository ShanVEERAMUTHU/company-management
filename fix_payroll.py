import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_management.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS employees_payroll (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, month INTEGER NOT NULL, year INTEGER NOT NULL, basic_salary DECIMAL(10,2) NOT NULL, hra DECIMAL(10,2) NOT NULL DEFAULT 0, allowances DECIMAL(10,2) NOT NULL DEFAULT 0, pf_deduction DECIMAL(10,2) NOT NULL DEFAULT 0, tax_deduction DECIMAL(10,2) NOT NULL DEFAULT 0, other_deductions DECIMAL(10,2) NOT NULL DEFAULT 0, net_salary DECIMAL(10,2) NOT NULL DEFAULT 0, is_paid BOOLEAN NOT NULL DEFAULT 0, paid_date DATE NULL, created_at DATETIME NOT NULL, employee_id INTEGER NOT NULL REFERENCES employees_employee(id), UNIQUE(employee_id, month, year))')
connection.commit()
print('Done!')
