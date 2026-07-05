from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("departments", views.DepartmentViewSet)
router.register("positions", views.PositionViewSet)
router.register("employees", views.EmployeeViewSet)
router.register("attendances", views.AttendanceViewSet)
router.register("leaves", views.LeaveRequestViewSet)
router.register("salaries", views.SalaryViewSet)

urlpatterns = [
    path("dashboard/", views.dashboard),
    path("", include(router.urls)),
]
