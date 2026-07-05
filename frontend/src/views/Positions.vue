<template>
  <div>
    <el-card>
      <el-button type="success" size="small" icon="el-icon-plus" style="margin-bottom: 15px" @click="openDialog()">新增职位</el-button>
      <el-table :data="list" border stripe>
        <el-table-column prop="id" label="ID" width="60"></el-table-column>
        <el-table-column prop="name" label="职位名称"></el-table-column>
        <el-table-column prop="level" label="职级" width="100"></el-table-column>
        <el-table-column prop="department_name" label="所属部门"></el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="{ row }">
            <el-button size="mini" @click="openDialog(row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="remove(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="form.id ? '编辑职位' : '新增职位'" :visible.sync="dialogVisible" width="450px">
      <el-form :model="form" label-width="80px" size="small">
        <el-form-item label="职位名称"><el-input v-model="form.name"></el-input></el-form-item>
        <el-form-item label="职级"><el-input v-model="form.level" placeholder="如 P5 / M1"></el-input></el-form-item>
        <el-form-item label="所属部门">
          <el-select v-model="form.department" style="width: 100%">
            <el-option v-for="d in departments" :key="d.id" :label="d.name" :value="d.id"></el-option>
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
  name: 'Positions',
  data() {
    return { list: [], departments: [], dialogVisible: false, form: { id: null, name: '', level: '', department: null } }
  },
  created() {
    this.load()
    api.get('/departments/').then(res => { this.departments = res.data })
  },
  methods: {
    load() {
      api.get('/positions/').then(res => { this.list = res.data })
    },
    openDialog(row) {
      this.form = row ? { ...row } : { id: null, name: '', level: '', department: null }
      this.dialogVisible = true
    },
    save() {
      const req = this.form.id
        ? api.put(`/positions/${this.form.id}/`, this.form)
        : api.post('/positions/', this.form)
      req.then(() => {
        this.$message.success('保存成功')
        this.dialogVisible = false
        this.load()
      }).catch(() => this.$message.error('保存失败'))
    },
    remove(row) {
      this.$confirm(`确定删除职位「${row.name}」吗？`, '提示', { type: 'warning' })
        .then(() => api.delete(`/positions/${row.id}/`))
        .then(() => { this.$message.success('删除成功'); this.load() })
        .catch(() => {})
    }
  }
}
</script>
