from django.shortcuts import render,redirect,get_object_or_404
from .models import Employee  
from django.db.models import Sum

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/list.html', {
        'employees': employees
    })


def add_employee(request):
    if request.method == "POST":
        Employee.objects.create(
            Emp_id=request.POST['Emp_id'],
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            department=request.POST['department'],
            salary=request.POST['salary'],
            joining_date=request.POST['joining_date'],
            photo=request.FILES.get('photo')
        )
        return redirect('employee_list')
    return render(request, 'employees/add_employee.html')

def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, Emp_id=emp_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employees/delete_confirm.html', {'employee': employee})

def update_employee(request, emp_id):
    employee = get_object_or_404(Employee, Emp_id=emp_id)

    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.phone = request.POST.get('phone')
        employee.department = request.POST.get('department')
        employee.salary = request.POST.get('salary')
        employee.joining_date = request.POST.get('joining_date')

        if request.FILES.get('photo'):
            employee.photo = request.FILES['photo']

        employee.save()
        return redirect('employee_list')

    return render(request, 'employees/edit.html', {'employee': employee})




from django.shortcuts import render, redirect
from .models import Department

def department_list(request):
    departments = Department.objects.all()
    return render(
        request,
        'employees/department_list.html',
        {'departments': departments}
    )


def add_department(request):

    if request.method == "POST":

        Department.objects.create(
            dept_id=request.POST['dept_id'],
            dept_name=request.POST['dept_name'],
            manager_name=request.POST['manager_name'],
            location=request.POST['location']
        )

        return redirect('department_list')

    return render(request, 'employees/add_department.html')

def update_department(request, dept_id):

    department = get_object_or_404(
        Department,
        dept_id=dept_id
    )

    if request.method == "POST":

        department.dept_name = request.POST['dept_name']
        department.manager_name = request.POST['manager_name']
        department.location = request.POST['location']

        department.save()

        return redirect('department_list')

    return render(
        request,
        'employees/edit_department.html',
        {'department': department}
    )

from django.shortcuts import render, redirect, get_object_or_404

def delete_department(request, dept_id):

    department = get_object_or_404(
        Department,
        dept_id=dept_id
    )

    if request.method == "POST":
        department.delete()
        return redirect('department_list')

    return render(
        request,
        'employees/delete_department.html',
        {'department': department}
    )




from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Employee, Attendance

def attendance_page(request):
    from datetime import date as dt_date
    import calendar
    today = dt_date.today()

    if request.method == 'POST':
        emp_id = request.POST.get('employee')
        att_date = request.POST.get('date')
        status = request.POST.get('status')
        check_in = request.POST.get('check_in') or None
        check_out = request.POST.get('check_out') or None
        employee = get_object_or_404(Employee, id=emp_id)
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=att_date
        )
        attendance.status = status
        attendance.check_in = check_in
        attendance.check_out = check_out
        attendance.save()
        return redirect('attendance_page')

    month = today.month
    year = today.year
    import calendar
    total_days = calendar.monthrange(year, month)[1]

    employees = Employee.objects.all()
    monthly = []
    for emp in employees:
        present = Attendance.objects.filter(employee=emp, date__month=month, date__year=year, status='Present').count()
        half = Attendance.objects.filter(employee=emp, date__month=month, date__year=year, status='Half Day').count()
        absent = Attendance.objects.filter(employee=emp, date__month=month, date__year=year, status='Absent').count()
        monthly.append({
            'employee': emp,
            'present': present,
            'half_day': half,
            'absent': absent,
        })

    attendances = Attendance.objects.all().order_by('-date').select_related('employee')
    return render(request, 'employees/attendance.html', {
        'today': today,
        'employees': employees,
        'attendances': attendances,
        'monthly': monthly,
        'month_name': today.strftime('%B %Y'),
    })


def check_in(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=timezone.now().date()
    )
    attendance.check_in = timezone.now().time()
    attendance.status = "Present"
    attendance.save()
    return redirect('attendance_page')

def check_out(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    try:
        attendance = Attendance.objects.get(
            employee=employee,
            date=timezone.now().date()
        )
        attendance.check_out = timezone.now().time()
        attendance.save()
    except Attendance.DoesNotExist:
        pass
    return redirect('attendance_page')

from datetime import date as dt_date
from .models import Employee, Department, Attendance, Payroll
def payroll_list(request):
    today = dt_date.today()
    payrolls = Payroll.objects.all().order_by('-year', '-month').select_related('employee')
    employees = Employee.objects.all()
    return render(request, 'employees/payroll.html', {
        'payrolls': payrolls,
        'employees': employees,
        'today': today,
    })


def add_payroll(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        emp_id = request.POST.get('employee')
        employee = get_object_or_404(Employee, id=emp_id)
        basic = float(request.POST.get('basic_salary', 0))
        hra = float(request.POST.get('hra', 0))
        allowances = float(request.POST.get('allowances', 0))
        pf = float(request.POST.get('pf_deduction', 0))
        tax = float(request.POST.get('tax_deduction', 0))
        other = float(request.POST.get('other_deductions', 0))
        net = (basic + hra + allowances) - (pf + tax + other)
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))
        payroll, created = Payroll.objects.get_or_create(
            employee=employee, month=month, year=year,
            defaults={
                'basic_salary': basic, 'hra': hra,
                'allowances': allowances, 'pf_deduction': pf,
                'tax_deduction': tax, 'other_deductions': other,
                'net_salary': net
            }
        )
        if not created:
            payroll.basic_salary = basic
            payroll.hra = hra
            payroll.allowances = allowances
            payroll.pf_deduction = pf
            payroll.tax_deduction = tax
            payroll.other_deductions = other
            payroll.net_salary = net
            payroll.save()
        return redirect('payroll_list')
    return render(request, 'employees/add_payroll.html', {'employees': employees})

def mark_paid(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id)
    payroll.is_paid = True
    payroll.paid_date = dt_date.today()
    payroll.save()
    return redirect('payroll_list')

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def payslip(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id)
    
    # PDF generate pannurom
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payslip_{payroll.employee.name}_{payroll.month}_{payroll.year}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#7f77dd'),
        spaceAfter=6,
        alignment=1  # center
    )
    
    sub_style = ParagraphStyle(
        'Sub',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#888888'),
        alignment=1
    )
    
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#333333'),
    )

    # Company header
    elements.append(Paragraph("CompanyMS", title_style))
    elements.append(Paragraph("Payslip", sub_style))
    elements.append(Spacer(1, 0.3*inch))

    # Employee details table
    emp_data = [
        ['Employee Name', payroll.employee.name, 'Pay Period', f"{payroll.month}/{payroll.year}"],
        ['Employee ID', payroll.employee.Emp_id, 'Department', payroll.employee.department],
        ['Status', 'Paid' if payroll.is_paid else 'Unpaid', 'Paid Date', str(payroll.paid_date) if payroll.paid_date else '-'],
    ]
    
    emp_table = Table(emp_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    emp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f0eeff')),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#f0eeff')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#333333')),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#fafafa')]),
    ]))
    elements.append(emp_table)
    elements.append(Spacer(1, 0.3*inch))

    # Earnings & Deductions
    gross = float(payroll.basic_salary) + float(payroll.hra) + float(payroll.allowances)
    total_deductions = float(payroll.pf_deduction) + float(payroll.tax_deduction) + float(payroll.other_deductions)

    pay_data = [
        ['EARNINGS', 'AMOUNT', 'DEDUCTIONS', 'AMOUNT'],
        ['Basic Salary', f"Rs. {payroll.basic_salary}", 'PF Deduction', f"Rs. {payroll.pf_deduction}"],
        ['HRA', f"Rs. {payroll.hra}", 'Tax Deduction', f"Rs. {payroll.tax_deduction}"],
        ['Allowances', f"Rs. {payroll.allowances}", 'Other Deductions', f"Rs. {payroll.other_deductions}"],
        ['Gross Total', f"Rs. {gross:.2f}", 'Total Deductions', f"Rs. {total_deductions:.2f}"],
    ]

    pay_table = Table(pay_data, colWidths=[2*inch, 1.5*inch, 2*inch, 1.5*inch])
    pay_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#7f77dd')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#f0eeff')),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#fafafa')]),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('ALIGN', (3,0), (3,-1), 'RIGHT'),
    ]))
    elements.append(pay_table)
    elements.append(Spacer(1, 0.3*inch))

    # Net salary box
    net_data = [['NET SALARY', f"Rs. {payroll.net_salary}"]]
    net_table = Table(net_data, colWidths=[5.5*inch, 1.5*inch])
    net_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#7f77dd')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.white),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 14),
        ('PADDING', (0,0), (-1,-1), 12),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    elements.append(net_table)
    elements.append(Spacer(1, 0.5*inch))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#aaaaaa'),
        alignment=1
    )
    elements.append(Paragraph("This is a computer generated payslip. No signature required.", footer_style))

    doc.build(elements)
    return response


from .models import Employee, Department, Attendance, Payroll, Leave

def leave_list(request):
    leaves = Leave.objects.all().order_by('-id').select_related('employee')
    pending = leaves.filter(status='Pending').count()
    approved = leaves.filter(status='Approved').count()
    rejected = leaves.filter(status='Rejected').count()
    return render(request, 'employees/leave_list.html', {
        'leaves': leaves,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
    })

def apply_leave(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        emp_id = request.POST.get('employee')
        employee = get_object_or_404(Employee, id=emp_id)
        Leave.objects.create(
            employee=employee,
            leave_type=request.POST.get('leave_type'),
            from_date=request.POST.get('from_date'),
            to_date=request.POST.get('to_date'),
            reason=request.POST.get('reason'),
        )
        return redirect('leave_list')
    return render(request, 'employees/apply_leave.html', {'employees': employees})

def approve_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'Approved'
    leave.approved_on = dt_date.today()
    leave.save()
    return redirect('leave_list')

def reject_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)
    leave.status = 'Rejected'
    leave.save()
    return redirect('leave_list')

def leave_balance(request):
    employees = Employee.objects.all()
    balance_data = []
    for emp in employees:
        sick = Leave.objects.filter(employee=emp, leave_type='Sick Leave', status='Approved').count()
        casual = Leave.objects.filter(employee=emp, leave_type='Casual Leave', status='Approved').count()
        annual = Leave.objects.filter(employee=emp, leave_type='Annual Leave', status='Approved').count()
        balance_data.append({
            'employee': emp,
            'sick_used': sick,
            'sick_balance': 12 - sick,
            'casual_used': casual,
            'casual_balance': 12 - casual,
            'annual_used': annual,
            'annual_balance': 18 - annual,
        })
    return render(request, 'employees/leave_balance.html', {'balance_data': balance_data})

def reports(request):
    from datetime import date as dt_date
    from django.db.models import Sum
    
    today = dt_date.today()
    month = today.month
    year = today.year

    # Employee Report
    total_employees = Employee.objects.count()
    dept_wise = {}
    for emp in Employee.objects.all():
        dept = emp.department or 'Unknown'
        dept_wise[dept] = dept_wise.get(dept, 0) + 1
    total_salary = Employee.objects.aggregate(total=Sum('salary'))['total'] or 0

    # Attendance Report
    total_present = Attendance.objects.filter(date__month=month, date__year=year, status='Present').count()
    total_absent = Attendance.objects.filter(date__month=month, date__year=year, status='Absent').count()
    total_halfday = Attendance.objects.filter(date__month=month, date__year=year, status='Half Day').count()

    # Payroll Report
    total_payroll = Payroll.objects.filter(month=month, year=year).aggregate(total=Sum('net_salary'))['total'] or 0
    paid_count = Payroll.objects.filter(month=month, year=year, is_paid=True).count()
    unpaid_count = Payroll.objects.filter(month=month, year=year, is_paid=False).count()

    # Leave Report
    total_leaves = Leave.objects.count()
    pending_leaves = Leave.objects.filter(status='Pending').count()
    approved_leaves = Leave.objects.filter(status='Approved').count()
    rejected_leaves = Leave.objects.filter(status='Rejected').count()
    leave_type_wise = {}
    for leave in Leave.objects.all():
        lt = leave.leave_type
        leave_type_wise[lt] = leave_type_wise.get(lt, 0) + 1

    return render(request, 'employees/reports.html', {
        'today': today,
        'month_name': today.strftime('%B %Y'),
        'total_employees': total_employees,
        'dept_wise': dept_wise,
        'total_salary': total_salary,
        'total_present': total_present,
        'total_absent': total_absent,
        'total_halfday': total_halfday,
        'total_payroll': total_payroll,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
        'total_leaves': total_leaves,
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves': rejected_leaves,
        'leave_type_wise': leave_type_wise,
    })


from django.contrib.auth.decorators import login_required

@login_required

def dashboard(request):
    from datetime import date as dt_date
    from django.db.models import Sum

    today = dt_date.today()
    month = today.month
    year = today.year

    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    total_salary = Employee.objects.aggregate(total=Sum('salary'))['total'] or 0

    today_present = Attendance.objects.filter(date=today, status='Present').count()
    today_absent = Attendance.objects.filter(date=today, status='Absent').count()

    pending_leaves = Leave.objects.filter(status='Pending').count()
    approved_leaves = Leave.objects.filter(status='Approved').count()

    total_payroll = Payroll.objects.filter(month=month, year=year).aggregate(total=Sum('net_salary'))['total'] or 0
    unpaid_payroll = Payroll.objects.filter(month=month, year=year, is_paid=False).count()

    recent_employees = Employee.objects.all().order_by('-id')[:5]
    recent_attendance = Attendance.objects.filter(date=today).select_related('employee')
    pending_leave_list = Leave.objects.filter(status='Pending').select_related('employee')[:5]

    return render(request, 'employees/dashboard.html', {
        'today': today,
        'month_name': today.strftime('%B %Y'),
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_salary': total_salary,
        'today_present': today_present,
        'today_absent': today_absent,
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'total_payroll': total_payroll,
        'unpaid_payroll': unpaid_payroll,
        'recent_employees': recent_employees,
        'recent_attendance': recent_attendance,
        'pending_leave_list': pending_leave_list,
    })


from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        print("USERNAME =", username)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("USER =", user)

        if user is not None:
            print("LOGIN SUCCESS")
            login(request, user)
            return redirect('dashboard')

        print("LOGIN FAILED")
        messages.error(request, "Invalid Username or Password!")

    return render(request, 'employees/login.html')

# def login_view(request):

#      if request.method == "POST":

#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # print("USERNAME:", username)
#         # print("PASSWORD:", password)

#         user = authenticate(
#             request,
#             username=username,
#             password=password
#         )

#         # print("USER:", user)

#         if user is not None:
#             print("LOGIN SUCCESS")
#             login(request, user)
#             return redirect('dashboard')

#         else:
#             print("LOGIN FAILED")
#             messages.error(request, "Invalid Username or Password!")

#         return render(request, 'employees/login.html')


# # def logout_view(request):
# #     logout(request)
# #     return redirect('login')