import Vue from 'vue'
import VueRouter from 'vue-router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import Employees from './views/Employees.vue'
import Departments from './views/Departments.vue'
import Positions from './views/Positions.vue'
import Attendance from './views/Attendance.vue'
import Leaves from './views/Leaves.vue'
import Salaries from './views/Salaries.vue'

Vue.use(VueRouter)
Vue.use(ElementUI)

const router = new VueRouter({
  routes: [
    { path: '/', component: Dashboard, meta: { title: '首页概览' } },
    { path: '/employees', component: Employees, meta: { title: '员工管理' } },
    { path: '/departments', component: Departments, meta: { title: '部门管理' } },
    { path: '/positions', component: Positions, meta: { title: '职位管理' } },
    { path: '/attendance', component: Attendance, meta: { title: '考勤管理' } },
    { path: '/leaves', component: Leaves, meta: { title: '请假审批' } },
    { path: '/salaries', component: Salaries, meta: { title: '薪资管理' } }
  ]
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
