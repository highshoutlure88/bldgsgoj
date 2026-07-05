from rest_framework import serializers

from .models import Attendance, Department, Employee, LeaveRequest, Position, Salary


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(source="employees.count", read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "description", "created_at", "employee_count"]


class PositionSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Position
        fields = ["id", "name", "level", "department", "department_name"]


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    position_name = serializers.CharField(source="position.name", read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id", "name", "gender", "phone", "email", "hire_date", "status",
            "department", "department_name", "position", "position_name",
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.name", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "employee", "employee_name", "date", "check_in", "check_out", "type"]


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.name", read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            "id", "employee", "employee_name", "type", "start_date", "end_date",
            "reason", "status", "created_at",
        ]


class SalarySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.name", read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Salary
        fields = ["id", "employee", "employee_name", "month", "base", "bonus", "deduction", "total"]
