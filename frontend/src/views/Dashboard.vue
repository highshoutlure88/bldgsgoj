<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <div class="stat">
            <i class="el-icon-user stat-icon" style="color: #409EFF"></i>
            <div>
              <div class="stat-num">{{ stats.employee_count }}</div>
              <div class="stat-label">在职员工</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div class="stat">
            <i class="el-icon-office-building stat-icon" style="color: #67C23A"></i>
            <div>
              <div class="stat-num">{{ stats.department_count }}</div>
              <div class="stat-label">部门数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div class="stat">
            <i class="el-icon-document-checked stat-icon" style="color: #E6A23C"></i>
            <div>
              <div class="stat-num">{{ stats.pending_leaves }}</div>
              <div class="stat-label">待审批请假</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-card style="margin-top: 20px">
      <div slot="header">各部门人数分布</div>
      <div v-for="d in stats.department_stats" :key="d.name" style="margin-bottom: 15px">
        <span style="display: inline-block; width: 80px">{{ d.name }}</span>
        <el-progress :percentage="percent(d.count)" :format="() => d.count + ' 人'" style="display: inline-block; width: 60%"></el-progress>
      </div>
    </el-card>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'Dashboard',
  data() {
    return { stats: { employee_count: 0, department_count: 0, pending_leaves: 0, department_stats: [] } }
  },
  created() {
    api.get('/dashboard/').then(res => { this.stats = res.data })
  },
  methods: {
    percent(count) {
      const total = this.stats.employee_count || 1
      return Math.round((count / total) * 100)
    }
  }
}
</script>

<style scoped>
.stat { display: flex; align-items: center; }
.stat-icon { font-size: 48px; margin-right: 20px; }
.stat-num { font-size: 28px; font-weight: bold; }
.stat-label { color: #909399; }
</style>
