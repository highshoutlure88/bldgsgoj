<template>
  <div>
    <el-card>
      <el-button type="success" size="small" icon="el-icon-plus" style="margin-bottom: 15px" @click="openDialog()">录入考勤</el-button>
      <el-table :data="list" border stripe>
        <el-table-column prop="id" label="ID" width="60"></el-table-column>
        <el-table-column prop="employee_name" label="员工"></el-table-column>
        <el-table-column prop="date" label="日期"></el-table-column>
        <el-table-column prop="check_in" label="签到时间"></el-table-column>
        <el-table-column prop="check_out" label="签退时间"></el-table-column>
        <el-table-column label="类型" width="100">
          <template slot-scope="{ row }">
            <el-tag :type="typeTag(row.type)" size="small">{{ typeText(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template slot-scope="{ row }">
            <el-button size="mini" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="录入考勤" :visible.sync="dialogVisible" width="450px">
      <el-form :model="form" label-width="80px" size="small">
        <el-form-item label="员工">
          <el-select v-model="form.employee" style="width: 100%">
            <el-option v-for="e in employees" :key="e.id" :label="e.name" :value="e.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="form.date" type="date" value-format="yyyy-MM-dd" style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="签到时间">
          <el-time-picker v-model="form.check_in" value-format="HH:mm:ss" style="width: 100%"></el-time-picker>
        </el-form-item>
        <el-form-item label="签退时间">
          <el-time-picker v-model="form.check_out" value-format="HH:mm:ss" style="width: 100%"></el-time-picker>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type" style="width: 100%">
            <el-option label="正常" value="normal"></el-option>
            <el-option label="迟到" value="late"></el-option>
            <el-option label="早退" value="early"></el-option>
            <el-option label="缺勤" value="absent"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import api from '../api'

export default {
  name: 'Attendance',
  data() {
    return {
      list: [],
      employees: [],
      dialogVisible: false,
      form: { employee: null, date: '', check_in: null, check_out: null, type: 'normal' }
    }
  },
  created() {
    this.load()
    api.get('/employees/').then(res => { this.employees = res.data })
  },
  methods: {
    load() {
      api.get('/attendances/').then(res => { this.list = res.data })
    },
    typeText(t) {
      return { normal: '正常', late: '迟到', early: '早退', absent: '缺勤' }[t] || t
    },
    typeTag(t) {
      return { normal: 'success', late: 'warning', early: 'warning', absent: 'danger' }[t] || 'info'
    },
    openDialog() {
      this.form = { employee: null, date: '', check_in: null, check_out: null, type: 'normal' }
      this.dialogVisible = true
    },
    save() {
      api.post('/attendances/', this.form).then(() => {
        this.$message.success('保存成功')
        this.dialogVisible = false
        this.load()
      }).catch(() => this.$message.error('保存失败，同一员工同一天只能有一条记录'))
    },
    remove(row) {
      this.$confirm('确定删除该考勤记录吗？', '提示', { type: 'warning' })
        .then(() => api.delete(`/attendances/${row.id}/`))
        .then(() => { this.$message.success('删除成功'); this.load() })
        .catch(() => {})
    }
  }
}
</script>
