from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Attendance, Department, Employee, LeaveRequest, Position, Salary
from .serializers import (
    AttendanceSerializer,
    DepartmentSerializer,
    EmployeeSerializer,
    LeaveRequestSerializer,
    PositionSerializer,
    SalarySerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by("id")
    serializer_class = DepartmentSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.select_related("department").order_by("id")
    serializer_class = PositionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        department = self.request.query_params.get("department")
        if department:
            qs = qs.filter(department_id=department)
        return qs


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related("department", "position").order_by("id")
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get("name")
        department = self.request.query_params.get("department")
        status_ = self.request.query_params.get("status")
        if name:
            qs = qs.filter(name__icontains=name)
        if department:
            qs = qs.filter(department_id=department)
        if status_:
            qs = qs.filter(status=status_)
        return qs


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("employee").order_by("-date")
    serializer_class = AttendanceSerializer


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.select_related("employee").order_by("-created_at")
    serializer_class = LeaveRequestSerializer

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        leave = self.get_object()
        leave.status = "approved"
        leave.save()
        return Response(LeaveRequestSerializer(leave).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        leave = self.get_object()
        leave.status = "rejected"
        leave.save()
        return Response(LeaveRequestSerializer(leave).data)


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.select_related("employee").order_by("-month")
    serializer_class = SalarySerializer


@api_view(["GET"])
def dashboard(request):
    return Response({
        "employee_count": Employee.objects.filter(status="active").count(),
        "department_count": Department.objects.count(),
        "pending_leaves": LeaveRequest.objects.filter(status="pending").count(),
        "department_stats": [
            {"name": d.name, "count": d.employees.filter(status="active").count()}
            for d in Department.objects.all()
        ],
    })
