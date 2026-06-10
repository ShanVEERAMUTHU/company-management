from django.db import models
from django.utils import timezone
# class Employee(models.Model):
#     Emp_id=models.CharField(max_length=200)
#     name=models.CharField(max_length=100)
#     email=models.EmailField(unique=True)
#     phone = models.CharField(max_length=15)
#     department = models.CharField(max_length=50)
#     salary = models.DecimalField(max_digits=10, decimal_places=2)
#     joining_date = models.DateField()
#     photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
#     def __str__(self):
#      return self.name
    
# class Department(models.Model):
#     dept_id = models.CharField(max_length=20, primary_key=True)
#     dept_name = models.CharField(max_length=100)
#     manager_name = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)

#     def __str__(self):
#         return self.dept_name

from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone

class Employee(models.Model):
    Emp_id = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joining_date = models.DateField()
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    dept_id = models.CharField(max_length=20, primary_key=True)
    dept_name = models.CharField(max_length=100)
    manager_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Half Day', 'Half Day'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pf_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')

    def calculate_net(self):
        gross = self.basic_salary + self.hra + self.allowances
        deductions = self.pf_deduction + self.tax_deduction + self.other_deductions
        self.net_salary = gross - deductions
        return self.net_salary

    def __str__(self):
        return f"{self.employee.name} - {self.month}/{self.year}"
    
class Leave(models.Model):
    LEAVE_TYPES = [
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Annual Leave', 'Annual Leave'),
        ('Maternity Leave', 'Maternity Leave'),
        ('Emergency Leave', 'Emergency Leave'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def total_days(self):
        return (self.to_date - self.from_date).days + 1

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type} - {self.status}"