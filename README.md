# 公司人事管理系统

前端 Vue 2.7 + Element UI，后端 Django 6 + Django REST Framework，数据库 SQLite。

## 功能模块

- 首页概览：员工/部门/待审批请假统计、部门人数分布
- 员工管理：增删改查、姓名搜索、部门筛选、部门-职位联动
- 部门管理 / 职位管理
- 考勤管理：签到签退、正常/迟到/早退/缺勤
- 请假审批：发起请假、批准/拒绝
- 薪资管理：按月录入，自动计算实发工资

## 运行

后端：

```bash
cd backend
pip install django djangorestframework django-cors-headers
python manage.py migrate
python seed.py   # 初始化示例数据（可选）
python manage.py runserver 0.0.0.0:8000
```

前端：

```bash
cd frontend
npm install
npm run dev
```

浏览器访问 http://localhost:5173/ （前端已配置 Vite 代理，将 /api 转发至 8000 端口）。

## 报告

`report/` 目录包含项目报告（ER 图、架构图、运行截图、功能说明）及图片生成脚本。
