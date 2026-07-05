from django.db import models


class Department(models.Model):
    name = models.CharField("部门名称", max_length=50, unique=True)
    description = models.CharField("部门描述", max_length=200, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField("职位名称", max_length=50)
    level = models.CharField("职级", max_length=20, blank=True, default="")
    department = models.ForeignKey(Department, verbose_name="所属部门", on_delete=models.CASCADE, related_name="positions")

    def __str__(self):
        return self.name


class Employee(models.Model):
    GENDER_CHOICES = [("M", "男"), ("F", "女")]
    STATUS_CHOICES = [("active", "在职"), ("left", "离职")]

    name = models.CharField("姓名", max_length=50)
    gender = models.CharField("性别", max_length=1, choices=GENDER_CHOICES, default="M")
    phone = models.CharField("电话", max_length=20, blank=True, default="")
    email = models.EmailField("邮箱", blank=True, default="")
    hire_date = models.DateField("入职日期")
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default="active")
    department = models.ForeignKey(Department, verbose_name="部门", on_delete=models.PROTECT, related_name="employees")
    position = models.ForeignKey(Position, verbose_name="职位", on_delete=models.PROTECT, related_name="employees")

    def __str__(self):
        return self.name


class Attendance(models.Model):
    TYPE_CHOICES = [("normal", "正常"), ("late", "迟到"), ("early", "早退"), ("absent", "缺勤")]

    employee = models.ForeignKey(Employee, verbose_name="员工", on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField("日期")
    check_in = models.TimeField("签到时间", null=True, blank=True)
    check_out = models.TimeField("签退时间", null=True, blank=True)
    type = models.CharField("考勤类型", max_length=10, choices=TYPE_CHOICES, default="normal")

    class Meta:
        unique_together = ("employee", "date")


class LeaveRequest(models.Model):
    TYPE_CHOICES = [("annual", "年假"), ("sick", "病假"), ("personal", "事假"), ("other", "其他")]
    STATUS_CHOICES = [("pending", "待审批"), ("approved", "已批准"), ("rejected", "已拒绝")]

    employee = models.ForeignKey(Employee, verbose_name="员工", on_delete=models.CASCADE, related_name="leaves")
    type = models.CharField("请假类型", max_length=10, choices=TYPE_CHOICES, default="annual")
    start_date = models.DateField("开始日期")
    end_date = models.DateField("结束日期")
    reason = models.CharField("请假原因", max_length=200, blank=True, default="")
    status = models.CharField("审批状态", max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


class Salary(models.Model):
    employee = models.ForeignKey(Employee, verbose_name="员工", on_delete=models.CASCADE, related_name="salaries")
    month = models.CharField("月份", max_length=7)  # e.g. 2026-07
    base = models.DecimalField("基本工资", max_digits=10, decimal_places=2)
    bonus = models.DecimalField("奖金", max_digits=10, decimal_places=2, default=0)
    deduction = models.DecimalField("扣款", max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("employee", "month")

    @property
    def total(self):
        return self.base + self.bonus - self.deduction
