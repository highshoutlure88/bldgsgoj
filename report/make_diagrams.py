# -*- coding: utf-8 -*-
"""生成 ER 图和系统架构图"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def entity(ax, x, y, w, h, title, fields, color="#dbeafe"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                facecolor=color, edgecolor="#1e3a5f", linewidth=1.5))
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="center",
            fontsize=11, fontweight="bold")
    ax.plot([x + 0.05, x + w - 0.05], [y + h - 0.58, y + h - 0.58], color="#1e3a5f", lw=1)
    for i, f in enumerate(fields):
        ax.text(x + 0.12, y + h - 0.85 - i * 0.30, f, ha="left", va="center", fontsize=8.5)


def arrow(ax, x1, y1, x2, y2, label):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=14, color="#c0392b", lw=1.4))
    ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.12, label, ha="center",
            fontsize=8.5, color="#c0392b", fontweight="bold")


# ---------------- ER 图 ----------------
fig, ax = plt.subplots(figsize=(13, 9))
ax.set_xlim(0, 13)
ax.set_ylim(0, 9)
ax.axis("off")
ax.set_title("公司人事管理系统 ER 图", fontsize=16, fontweight="bold", pad=16)

entity(ax, 0.5, 5.6, 2.8, 2.2, "Department 部门",
       ["PK id", "name 部门名称 (唯一)", "description 部门描述", "created_at 创建时间"], "#fde8c8")
entity(ax, 0.5, 2.2, 2.8, 2.0, "Position 职位",
       ["PK id", "name 职位名称", "level 职级", "FK department 所属部门"], "#fde8c8")
entity(ax, 5.0, 3.6, 3.0, 3.3, "Employee 员工",
       ["PK id", "name 姓名", "gender 性别", "phone 电话", "email 邮箱", "hire_date 入职日期",
        "status 在职状态", "FK department 部门", "FK position 职位"], "#dbeafe")
entity(ax, 9.7, 6.3, 3.0, 2.3, "Attendance 考勤",
       ["PK id", "FK employee 员工", "date 日期", "check_in / check_out",
        "type 考勤类型", "UNIQUE(employee, date)"], "#dcfce7")
entity(ax, 9.7, 3.3, 3.0, 2.5, "LeaveRequest 请假",
       ["PK id", "FK employee 员工", "type 请假类型", "start_date / end_date",
        "reason 原因", "status 审批状态", "created_at"], "#dcfce7")
entity(ax, 9.7, 0.4, 3.0, 2.4, "Salary 薪资",
       ["PK id", "FK employee 员工", "month 月份", "base 基本工资", "bonus 奖金",
        "deduction 扣款", "UNIQUE(employee, month)"], "#dcfce7")

arrow(ax, 1.9, 5.6, 1.9, 4.2, "1:N 拥有职位")
arrow(ax, 3.3, 6.4, 5.0, 5.9, "1:N 包含员工")
arrow(ax, 3.3, 3.3, 5.0, 4.3, "1:N 任职")
arrow(ax, 8.0, 6.0, 9.7, 7.2, "1:N 考勤记录")
arrow(ax, 8.0, 5.0, 9.7, 4.6, "1:N 请假申请")
arrow(ax, 8.0, 4.0, 9.7, 1.7, "1:N 薪资记录")

plt.savefig(r"C:\Users\Administrator\repos\hr-system\report\images\er_diagram.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------- 架构图 ----------------
fig, ax = plt.subplots(figsize=(12, 8.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis("off")
ax.set_title("公司人事管理系统 架构图", fontsize=16, fontweight="bold", pad=16)


def layer(x, y, w, h, title, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03",
                                facecolor=color, edgecolor="#334155", linewidth=1.5))
    ax.text(x + 0.2, y + h - 0.35, title, fontsize=12, fontweight="bold")


def box(x, y, w, h, text):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                facecolor="white", edgecolor="#64748b", linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)


layer(0.5, 7.4, 11, 2.2, "前端层  Vue 2.7 + Element UI + Vue Router + Axios  (Vite 开发服务器 :5173)", "#dbeafe")
for i, name in enumerate(["首页概览", "员工管理", "部门管理", "职位管理", "考勤管理", "请假审批", "薪资管理"]):
    box(0.8 + i * 1.52, 7.6, 1.35, 0.9, name)

ax.add_patch(FancyArrowPatch((6, 7.4), (6, 6.4), arrowstyle="<|-|>", mutation_scale=16, color="#c0392b", lw=1.6))
ax.text(6.2, 6.9, "HTTP / JSON  RESTful API（Vite 代理 /api → :8000）", fontsize=9.5, color="#c0392b")

layer(0.5, 3.6, 11, 2.8, "后端层  Django 6 + Django REST Framework  (:8000)", "#dcfce7")
box(0.8, 4.6, 2.4, 0.9, "URL 路由\nDefaultRouter")
box(3.5, 4.6, 2.4, 0.9, "视图集 ViewSet\nCRUD + 审批动作")
box(6.2, 4.6, 2.4, 0.9, "序列化器\nSerializers")
box(8.9, 4.6, 2.3, 0.9, "模型层 Models\nORM")
box(3.5, 3.8, 5.1, 0.6, "django-cors-headers 跨域中间件 / dashboard 统计接口")

ax.add_patch(FancyArrowPatch((6, 3.6), (6, 2.6), arrowstyle="<|-|>", mutation_scale=16, color="#c0392b", lw=1.6))
ax.text(6.2, 3.1, "Django ORM", fontsize=9.5, color="#c0392b")

layer(0.5, 0.6, 11, 2.0, "数据层  SQLite 数据库", "#fde8c8")
for i, name in enumerate(["Department", "Position", "Employee", "Attendance", "LeaveRequest", "Salary"]):
    box(0.8 + i * 1.78, 0.85, 1.6, 0.9, name)

plt.savefig(r"C:\Users\Administrator\repos\hr-system\report\images\architecture.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("diagrams done")
