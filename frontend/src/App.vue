<template>
  <el-container style="height: 100vh">
    <el-aside width="200px" style="background-color: #304156">
      <div class="logo">人事管理系统</div>
      <el-menu :default-active="$route.path" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF">
        <el-menu-item index="/"><i class="el-icon-s-home"></i>首页概览</el-menu-item>
        <el-menu-item index="/employees"><i class="el-icon-user"></i>员工管理</el-menu-item>
        <el-menu-item index="/departments"><i class="el-icon-office-building"></i>部门管理</el-menu-item>
        <el-menu-item index="/positions"><i class="el-icon-postcard"></i>职位管理</el-menu-item>
        <el-menu-item index="/attendance"><i class="el-icon-alarm-clock"></i>考勤管理</el-menu-item>
        <el-menu-item index="/leaves"><i class="el-icon-document-checked"></i>请假审批</el-menu-item>
        <el-menu-item index="/salaries"><i class="el-icon-money"></i>薪资管理</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background: #fff; border-bottom: 1px solid #e6e6e6; line-height: 60px">
        <span style="font-size: 18px; font-weight: bold">{{ $route.meta.title }}</span>
      </el-header>
      <el-main style="background: #f0f2f5">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default { name: 'App' }
</script>

<style>
body { margin: 0; }
.logo {
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  line-height: 60px;
}
</style>
