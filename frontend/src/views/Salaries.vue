<template>
  <div>
    <el-card>
      <el-button type="success" size="small" icon="el-icon-plus" style="margin-bottom: 15px" @click="openDialog()">录入薪资</el-button>
      <el-table :data="list" border stripe>
        <el-table-column prop="id" label="ID" width="60"></el-table-column>
        <el-table-column prop="employee_name" label="员工"></el-table-column>
        <el-table-column prop="month" label="月份"></el-table-column>
        <el-table-column prop="base" label="基本工资"></el-table-column>
        <el-table-column prop="bonus" label="奖金"></el-table-column>
        <el-table-column prop="deduction" label="扣款"></el-table-column>
        <el-table-column prop="total" label="实发工资"></el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="{ row }">
            <el-button size="mini" @click="openDialog(row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="form.id ? '编辑薪资' : '录入薪资'" :visible.sync="dialogVisible" width="450px">
      <el-form :model="form" label-width="80px" size="small">
        <el-form-item label="员工">
          <el-select v-model="form.employee" style="width: 100%">
            <el-option v-for="e in employees" :key="e.id" :label="e.name" :value="e.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="月份"><el-input v-model="form.month" placeholder="如 2026-07"></el-input></el-form-item>
        <el-form-item label="基本工资"><el-input-number v-model="form.base" :min="0" style="width: 100%"></el-input-number></el-form-item>
        <el-form-item label="奖金"><el-input-number v-model="form.bonus" :min="0" style="width: 100%"></el-input-number></el-form-item>
        <el-form-item label="扣款"><el-input-number v-model="form.deduction" :min="0" style="width: 100%"></el-input-number></el-form-item>
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
  name: 'Salaries',
  data() {
    return {
      list: [],
      employees: [],
      dialogVisible: false,
      form: { id: null, employee: null, month: '', base: 0, bonus: 0, deduction: 0 }
    }
  },
  created() {
    this.load()
    api.get('/employees/').then(res => { this.employees = res.data })
  },
  methods: {
    load() {
      api.get('/salaries/').then(res => { this.list = res.data })
    },
    openDialog(row) {
      this.form = row
        ? { id: row.id, employee: row.employee, month: row.month, base: Number(row.base), bonus: Number(row.bonus), deduction: Number(row.deduction) }
        : { id: null, employee: null, month: '', base: 0, bonus: 0, deduction: 0 }
      this.dialogVisible = true
    },
    save() {
      const req = this.form.id
        ? api.put(`/salaries/${this.form.id}/`, this.form)
        : api.post('/salaries/', this.form)
      req.then(() => {
        this.$message.success('保存成功')
        this.dialogVisible = false
        this.load()
      }).catch(() => this.$message.error('保存失败，同一员工同一月份只能有一条记录'))
    },
    remove(row) {
      this.$confirm('确定删除该薪资记录吗？', '提示', { type: 'warning' })
        .then(() => api.delete(`/salaries/${row.id}/`))
        .then(() => { this.$message.success('删除成功'); this.load() })
        .catch(() => {})
    }
  }
}
</script>
