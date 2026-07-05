<template>
  <div>
    <el-card>
      <el-button type="success" size="small" icon="el-icon-plus" style="margin-bottom: 15px" @click="openDialog()">新增部门</el-button>
      <el-table :data="list" border stripe>
        <el-table-column prop="id" label="ID" width="60"></el-table-column>
        <el-table-column prop="name" label="部门名称"></el-table-column>
        <el-table-column prop="description" label="部门描述"></el-table-column>
        <el-table-column prop="employee_count" label="员工人数" width="100"></el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="{ row }">
            <el-button size="mini" @click="openDialog(row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="form.id ? '编辑部门' : '新增部门'" :visible.sync="dialogVisible" width="450px">
      <el-form :model="form" label-width="80px" size="small">
        <el-form-item label="部门名称"><el-input v-model="form.name"></el-input></el-form-item>
        <el-form-item label="部门描述"><el-input v-model="form.description" type="textarea"></el-input></el-form-item>
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
  name: 'Departments',
  data() {
    return { list: [], dialogVisible: false, form: { id: null, name: '', description: '' } }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      api.get('/departments/').then(res => { this.list = res.data })
    },
    openDialog(row) {
      this.form = row ? { ...row } : { id: null, name: '', description: '' }
      this.dialogVisible = true
    },
    save() {
      const req = this.form.id
        ? api.put(`/departments/${this.form.id}/`, this.form)
        : api.post('/departments/', this.form)
      req.then(() => {
        this.$message.success('保存成功')
        this.dialogVisible = false
        this.load()
      }).catch(() => this.$message.error('保存失败'))
    },
    remove(row) {
      this.$confirm(`确定删除部门「${row.name}」吗？`, '提示', { type: 'warning' })
        .then(() => api.delete(`/departments/${row.id}/`))
        .then(() => { this.$message.success('删除成功'); this.load() })
        .catch(err => { if (err) this.$message.error('删除失败，该部门下可能仍有员工') })
    }
  }
}
</script>
