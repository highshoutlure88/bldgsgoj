<template>
  <div>
    <el-card>
      <el-form :inline="true" size="small">
        <el-form-item label="姓名">
          <el-input v-model="query.name" placeholder="搜索姓名" clearable></el-input>
        </el-form-item>
        <el-form-item label="部门">
          <el-select v-model="query.department" placeholder="全部" clearable>
            <el-option v-for="d in departments" :key="d.id" :label="d.name" :value="d.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
          <el-button type="success" icon="el-icon-plus" @click="openDialog()">新增员工</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="list" border stripe>
        <el-table-column prop="id" label="ID" width="60"></el-table-column>
        <el-table-column prop="name" label="姓名"></el-table-column>
        <el-table-column label="性别" width="70">
          <template slot-scope="{ row }">{{ row.gender === 'M' ? '男' : '女' }}</template>
        </el-table-column>
        <el-table-column prop="phone" label="电话"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column prop="department_name" label="部门"></el-table-column>
        <el-table-column prop="position_name" label="职位"></el-table-column>
        <el-table-column prop="hire_date" label="入职日期"></el-table-column>
        <el-table-column label="状态" width="80">
          <template slot-scope="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">
              {{ row.status === 'active' ? '在职' : '离职' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="{ row }">
            <el-button size="mini" @click="openDialog(row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="form.id ? '编辑员工' : '新增员工'" :visible.sync="dialogVisible" width="500px">
      <el-form :model="form" label-width="80px" size="small">
        <el-form-item label="姓名"><el-input v-model="form.name"></el-input></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.gender">
            <el-radio label="M">男</el-radio>
            <el-radio label="F">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="电话"><el-input v-model="form.phone"></el-input></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="form.email"></el-input></el-form-item>
        <el-form-item label="部门">
          <el-select v-model="form.department" @change="form.position = null" style="width: 100%">
            <el-option v-for="d in departments" :key="d.id" :label="d.name" :value="d.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="职位">
          <el-select v-model="form.position" style="width: 100%">
            <el-option v-for="p in filteredPositions" :key="p.id" :label="p.name" :value="p.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="入职日期">
          <el-date-picker v-model="form.hire_date" type="date" value-format="yyyy-MM-dd" style="width: 100%"></el-date-picker>
        </el-form-item>
        <el-form-item label="状态">
          <el-radio-group v-model="form.status">
            <el-radio label="active">在职</el-radio>
            <el-radio label="left">离职</el-radio>
          </el-radio-group>
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

const emptyForm = { id: null, name: '', gender: 'M', phone: '', email: '', department: null, position: null, hire_date: '', status: 'active' }

export default {
  name: 'Employees',
  data() {
    return {
      list: [],
      departments: [],
      positions: [],
      query: { name: '', department: null },
      dialogVisible: false,
      form: { ...emptyForm }
    }
  },
  computed: {
    filteredPositions() {
      return this.positions.filter(p => p.department === this.form.department)
    }
  },
  created() {
    this.load()
    api.get('/departments/').then(res => { this.departments = res.data })
    api.get('/positions/').then(res => { this.positions = res.data })
  },
  methods: {
    load() {
      api.get('/employees/', { params: { name: this.query.name || undefined, department: this.query.department || undefined } })
        .then(res => { this.list = res.data })
    },
    openDialog(row) {
      this.form = row ? { ...row } : { ...emptyForm }
      this.dialogVisible = true
    },
    save() {
      const req = this.form.id
        ? api.put(`/employees/${this.form.id}/`, this.form)
        : api.post('/employees/', this.form)
      req.then(() => {
        this.$message.success('保存成功')
        this.dialogVisible = false
        this.load()
      }).catch(() => this.$message.error('保存失败，请检查填写内容'))
    },
    remove(row) {
      this.$confirm(`确定删除员工「${row.name}」吗？`, '提示', { type: 'warning' })
        .then(() => api.delete(`/employees/${row.id}/`))
        .then(() => { this.$message.success('删除成功'); this.load() })
        .catch(() => {})
    }
  }
}
</script>
