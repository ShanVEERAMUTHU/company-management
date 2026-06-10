from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('delete/<str:emp_id>/', views.delete_employee, name='delete_employee'),
    path('update/<str:emp_id>/', views.update_employee, name='update_employee'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.add_department, name='add_department'),
    path('departments/update/<str:dept_id>/', views.update_department, name='update_department'),
    path('departments/delete/<str:dept_id>/', views.delete_department, name='delete_department'),
    path('attendance/', views.attendance_page, name='attendance_page'),
    path('checkin/<int:emp_id>/', views.check_in, name='check_in'),
    path('checkout/<int:emp_id>/', views.check_out, name='check_out'),
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/add/', views.add_payroll, name='add_payroll'),
    path('payroll/paid/<int:payroll_id>/', views.mark_paid, name='mark_paid'),
    path('payroll/payslip/<int:payroll_id>/', views.payslip, name='payslip'),
    path('leave/', views.leave_list, name='leave_list'),
    path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('leave/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('leave/balance/', views.leave_balance, name='leave_balance'),
    path('reports/', views.reports, name='reports'),
]





# from django.urls import path
# from . import views

# urlpatterns = [
#     # path('', views.login_view, name='home'),
#     path('', views.dashboard, name='dashboard'),
#     path('employees/', views.employee_list, name='employee_list'),
#     path('add/', views.add_employee, name='add_employee'),
#     path('delete/<str:emp_id>/', views.delete_employee, name='delete_employee'),
#     path('update/<str:emp_id>/', views.update_employee, name='update_employee'),
#     path('departments/', views.department_list, name='department_list'),
#     path('departments/add/', views.add_department, name='add_department'),
#     path('departments/update/<str:dept_id>/', views.update_department, name='update_department'),
#     path('departments/delete/<str:dept_id>/', views.delete_department, name='delete_department'),
#     path('attendance/', views.attendance_page, name='attendance_page'),
#     path('checkin/<int:emp_id>/', views.check_in, name='check_in'),
#     path('checkout/<int:emp_id>/', views.check_out, name='check_out'),
#     path('payroll/', views.payroll_list, name='payroll_list'),
#     path('payroll/add/', views.add_payroll, name='add_payroll'),
#     path('payroll/paid/<int:payroll_id>/', views.mark_paid, name='mark_paid'),
#     path('payroll/payslip/<int:payroll_id>/', views.payslip, name='payslip'),
#     path('leave/', views.leave_list, name='leave_list'),
#     path('leave/apply/', views.apply_leave, name='apply_leave'),
#     path('leave/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
#     path('leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
#     path('leave/balance/', views.leave_balance, name='leave_balance'),
#     path('reports/', views.reports, name='reports'),
#     #  path('login/', views.login_view, name='login'),
#     # path('logout/', views.logout_view, name='logout'),
#     # path('test-email/', views.test_email),
# ]










