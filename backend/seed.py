"""初始化示例数据: python seed.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from datetime import date, time

from hr.models import Attendance, Department, Employee, LeaveRequest, Position, Salary

Attendance.objects.all().delete()
LeaveRequest.objects.all().delete()
Salary.objects.all().delete()
Employee.objects.all().delete()
Position.objects.all().delete()
Department.objects.all().delete()

tech = Department.objects.create(name="技术部", description="负责产品研发与技术支持")
hr_dep = Department.objects.create(name="人事部", description="负责招聘、培训与员工关系")
fin = Department.objects.create(name="财务部", description="负责公司财务管理")
mkt = Department.objects.create(name="市场部", description="负责市场推广与品牌运营")

p_dev = Position.objects.create(name="软件工程师", level="P5", department=tech)
p_lead = Position.objects.create(name="技术经理", level="M1", department=tech)
p_hr = Position.objects.create(name="人事专员", level="P3", department=hr_dep)
p_acc = Position.objects.create(name="会计", level="P4", department=fin)
p_mkt = Position.objects.create(name="市场专员", level="P3", department=mkt)

e1 = Employee.objects.create(name="张伟", gender="M", phone="13800000001", email="zhangwei@example.com", hire_date=date(2022, 3, 1), department=tech, position=p_lead)
e2 = Employee.objects.create(name="李娜", gender="F", phone="13800000002", email="lina@example.com", hire_date=date(2023, 6, 15), department=tech, position=p_dev)
e3 = Employee.objects.create(name="王芳", gender="F", phone="13800000003", email="wangfang@example.com", hire_date=date(2021, 9, 1), department=hr_dep, position=p_hr)
e4 = Employee.objects.create(name="刘强", gender="M", phone="13800000004", email="liuqiang@example.com", hire_date=date(2024, 1, 8), department=fin, position=p_acc)
e5 = Employee.objects.create(name="陈静", gender="F", phone="13800000005", email="chenjing@example.com", hire_date=date(2024, 5, 20), department=mkt, position=p_mkt)
e6 = Employee.objects.create(name="赵磊", gender="M", phone="13800000006", email="zhaolei@example.com", hire_date=date(2023, 2, 10), department=tech, position=p_dev)

for emp in [e1, e2, e3, e4, e5, e6]:
    Attendance.objects.create(employee=emp, date=date(2026, 7, 3), check_in=time(9, 0), check_out=time(18, 0), type="normal")
Attendance.objects.create(employee=e2, date=date(2026, 7, 2), check_in=time(9, 40), check_out=time(18, 5), type="late")
Attendance.objects.create(employee=e5, date=date(2026, 7, 2), check_in=time(9, 0), check_out=time(16, 30), type="early")

LeaveRequest.objects.create(employee=e2, type="annual", start_date=date(2026, 7, 10), end_date=date(2026, 7, 12), reason="家庭旅行", status="pending")
LeaveRequest.objects.create(employee=e4, type="sick", start_date=date(2026, 6, 20), end_date=date(2026, 6, 21), reason="感冒发烧", status="approved")
LeaveRequest.objects.create(employee=e6, type="personal", start_date=date(2026, 7, 8), end_date=date(2026, 7, 8), reason="办理个人事务", status="pending")

for emp, base in [(e1, 25000), (e2, 15000), (e3, 10000), (e4, 12000), (e5, 9000), (e6, 16000)]:
    Salary.objects.create(employee=emp, month="2026-06", base=base, bonus=base * 0.1, deduction=200)

print("示例数据初始化完成")
