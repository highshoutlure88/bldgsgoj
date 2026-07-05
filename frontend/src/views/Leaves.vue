<template>
  <div>
    <el-card>
      <el-button type="success" size="small" icon="el-icon-plus" style="margin-bottom: 15px" @click="openDialog()">发起请假</el-button>
      <el-table :data="list" border stripe>
        <el-table-column prop="id" label="ID" width="60"></el-table-column>
        <el-table-column prop="employee_name" label="员工"></el-table-column>
        <el-table-column label="类型" width="80">
          <template slot-scope="{ row }">{{ typeText(row.type) }}</template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期"></el-table-column>
        <el-table-column prop="end_date" label="结束日期"></el-table-column>
        <el-table-column prop="reason" label="原因"></el-table-column>
        <el-table-column label="状态" width="90">
          <template slot-scope="{ row }">
            <el-tag :type="statusTag(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160">
          <template slot-scope="{ row }">
            <template v-if="row.status === 'pending'">
              <el-button size="mini" type="success" @click="approve(row)">批准</el-button>
              <el-button size="mini" type="danger" @click="reject(row)">拒绝</el-button>
            </template>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="发起请假" :visible.sync="dialogVisible" width="450px">
      <el-form :model="form" label-width="80px" size="small">
        <el-form-item label="员工">
          <el-select v-model="form.employee" style="width: 100%">
            <el-option v-for="e in employees" :key="e.id" :label="e.name" :value="e.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" style="width: 100%">
            <el-option label="年假" value="annual"></el-option>
            <el-option label="病假" value="sick"></el-option>
            <el-option label="事假" value="personal"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker v-model="form.start_date" type="date" value-format="yyyy-MM-dd" style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="form.end_date" type="date" value-format="yyyy-MM-dd" style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="原因"><el-input v-model="form.reason" type="textarea"></el-input></el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">提交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'Leaves',
  data() {
    return {
      list: [],
      employees: [],
      dialogVisible: false,
      form: { employee: null, type: 'annual', start_date: '', end_date: '', reason: '' }
    }
  },
  created() {
    this.load()
    api.get('/employees/').then(res => { this.employees = res.data })
  },
  methods: {
    load() {
      api.get('/leaves/').then(res => { this.list = res.data })
    },
    typeText(t) {
      return { annual: '年假', sick: '病假', personal: '事假', other: '其他' }[t] || t
    },
    statusText(s) {
      return { pending: '待审批', approved: '已批准', rejected: '已拒绝' }[s] || s
    },
    statusTag(s) {
      return { pending: 'warning', approved: 'success', rejected: 'danger' }[s] || 'info'
    },
    openDialog() {
      this.form = { employee: null, type: 'annual', start_date: '', end_date: '', reason: '' }
      this.dialogVisible = true
    },
    save() {
      api.post('/leaves/', this.form).then(() => {
        this.$message.success('提交成功')
        this.dialogVisible = false
        this.load()
      }).catch(() => this.$message.error('提交失败'))
    },
    approve(row) {
      api.post(`/leaves/${row.id}/approve/`).then(() => { this.$message.success('已批准'); this.load() })
    },
    reject(row) {
      api.post(`/leaves/${row.id}/reject/`).then(() => { this.$message.success('已拒绝'); this.load() })
    }
  }
}
</script>
