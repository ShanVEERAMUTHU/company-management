import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_management.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute("PRAGMA table_info(employees_leave)")
cols = cursor.fetchall()
for col in cols:
    print(col)
