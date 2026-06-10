import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_management.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS employees_attendance')
cursor.execute('CREATE TABLE employees_attendance (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date DATE NOT NULL, check_in TIME NULL, check_out TIME NULL, status VARCHAR(20) NOT NULL, employee_id INTEGER NOT NULL REFERENCES employees_employee(id), UNIQUE(employee_id, date))')
connection.commit()
print('Done!')
