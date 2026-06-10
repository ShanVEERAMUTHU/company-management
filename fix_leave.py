import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_management.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS employees_leave (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, leave_type VARCHAR(50) NOT NULL, start_date DATE NOT NULL, end_date DATE NOT NULL, reason TEXT NOT NULL, status VARCHAR(20) NOT NULL DEFAULT ''Pending'', applied_on DATETIME NOT NULL, approved_on DATE NULL, employee_id INTEGER NOT NULL REFERENCES employees_employee(id))')
connection.commit()
print('Done!')
