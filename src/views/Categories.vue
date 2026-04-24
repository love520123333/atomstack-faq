<template>
  <div class="page-container">
    <div class="page-title"><el-icon><Folder /></el-icon> 分类管理 <div style="flex:1"></div><el-button type="primary" :icon="Plus" @click="openDialog()">添加分类</el-button></div>

    <el-row :gutter="16">
      <el-col :xs="24" :sm="12" :lg="8" v-for="cat in machineStore.categories" :key="cat.id">
        <el-card shadow="hover" class="cat-card">
          <div class="cat-header">
            <div class="cat-dot" :style="{ background: cat.color }"></div>
            <h3 class="cat-name">{{ cat.name }}</h3>
            <el-dropdown trigger="click">
              <el-button text size="small"><el-icon><MoreFilled /></el-icon></el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="openDialog(cat)"><el-icon><Edit /></el-icon> 编辑</el-dropdown-item>
                  <el-dropdown-item @click="$router.push({ path:'/faq', query:{ category: cat.id } })"><el-icon><Document /></el-icon> 查看FAQ</el-dropdown-item>
                  <el-dropdown-item divided @click="handleDelete(cat)"><span style="color:#f56c6c">删除</span></el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <p class="cat-desc">{{ cat.description || '暂无描述' }}</p>
          <div class="cat-stats">
            <el-statistic title="机型数" :value="machineStore.machines.filter(m=>m.categoryId===cat.id).length" />
            <el-statistic title="FAQ数" :value="faqStore.getFaqsByCategory(cat.id, machineStore).length" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑分类' : '添加分类'" width="500px">
      <el-form :model="form" label-position="top">
        <el-form-item label="分类名称" required><el-input v-model="form.name" placeholder="如 A系列半导体雕刻机" /></el-form-item>
        <el-form-item label="分类颜色">
          <el-color-picker v-model="form.color" />
        </el-form-item>
        <el-form-item label="描述"><el-input v-model="form.description" type="textarea" :rows="2" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible=false">取消</el-button><el-button type="primary" @click="handleSave">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, MoreFilled, Document, Folder } from '@element-plus/icons-vue'
import { useMachineStore } from '../stores/machine'
import { useFaqStore } from '../stores/faq'
import { initSampleData } from '../data/sampleData'

const machineStore = useMachineStore()
const faqStore = useFaqStore()

onMounted(() => {
  initSampleData(machineStore, faqStore)
})

const dialogVisible = ref(false)
const editing = ref(null)
const form = ref({ name: '', color: '#409eff', description: '' })

function openDialog(cat = null) {
  editing.value = cat
  form.value = cat ? { name: cat.name, color: cat.color, description: cat.description || '' } : { name: '', color: '#409eff', description: '' }
  dialogVisible.value = true
}

function handleSave() {
  if (!form.value.name.trim()) { ElMessage.warning('请输入名称'); return }
  if (editing.value) machineStore.updateCategory(editing.value.id, form.value)
  else machineStore.addCategory(form.value)
  ElMessage.success('保存成功')
  dialogVisible.value = false
}

async function handleDelete(cat) {
  await ElMessageBox.confirm(`删除分类「${cat.name}」？下级机型将变为未分类`, '确认', { type: 'warning' })
  machineStore.deleteCategory(cat.id)
  ElMessage.success('已删除')
}
</script>

<style scoped>
.cat-card { margin-bottom: 16px; }
.cat-header { display: flex; align-items: center; gap: 8px; }
.cat-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.cat-name { font-size: 16px; font-weight: 600; flex: 1; }
.cat-desc { font-size: 13px; color: #909399; margin: 8px 0; }
.cat-stats { display: flex; justify-content: space-around; margin-top: 12px; padding-top: 12px; border-top: 1px solid #f0f0f0; }
</style>
