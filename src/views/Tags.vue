<template>
  <div class="page-container">
    <div class="page-title"><el-icon><PriceTag /></el-icon> 标签管理 <div style="flex:1"></div><el-button type="primary" :icon="Plus" @click="openDialog()">添加标签</el-button></div>

    <el-row :gutter="12">
      <el-col :xs="12" :sm="8" :md="6" v-for="tag in sortedTags" :key="tag.id">
        <el-card shadow="hover" class="tag-card" :body-style="{ padding: '16px' }" @click="$router.push(`/tags/${tag.id}`)" style="cursor:pointer">
          <div class="tag-header">
            <el-tag :color="tag.color" effect="dark" size="large" style="border:none">{{ tag.name }}</el-tag>
            <el-dropdown trigger="click" @click.stop>
              <el-button text size="small" @click.stop><el-icon><MoreFilled /></el-icon></el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click.stop="openDialog(tag)"><el-icon><Edit /></el-icon> 编辑</el-dropdown-item>
                  <el-dropdown-item @click.stop="$router.push({ path:'/search', query:{ tag: tag.id } })"><el-icon><Search /></el-icon> 搜索</el-dropdown-item>
                  <el-dropdown-item divided @click.stop="handleDelete(tag)"><span style="color:#f56c6c">删除</span></el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <div class="tag-count">关联 FAQ: <strong>{{ tag.usageCount }}</strong> 条</div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog v-model="dialogVisible" :title="editing ? '编辑标签' : '添加标签'" width="450px">
      <el-form :model="form" label-position="top">
        <el-form-item label="标签名称" required><el-input v-model="form.name" placeholder="如 激光不亮" /></el-form-item>
        <el-form-item label="标签颜色"><el-color-picker v-model="form.color" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="dialogVisible=false">取消</el-button><el-button type="primary" @click="handleSave">保存</el-button></template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, MoreFilled, Search } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { initSampleData } from '../data/sampleData'

const faqStore = useFaqStore()
const machineStore = useMachineStore()
const sortedTags = computed(() => [...faqStore.tags].sort((a, b) => b.usageCount - a.usageCount))

onMounted(() => {
  initSampleData(machineStore, faqStore)
})

const dialogVisible = ref(false)
const editing = ref(null)
const form = ref({ name: '', color: '#409eff' })

function openDialog(tag = null) {
  editing.value = tag
  form.value = tag ? { name: tag.name, color: tag.color } : { name: '', color: '#409eff' }
  dialogVisible.value = true
}

function handleSave() {
  if (!form.value.name.trim()) { ElMessage.warning('请输入名称'); return }
  if (editing.value) faqStore.updateTag(editing.value.id, form.value)
  else faqStore.addTag(form.value)
  ElMessage.success('保存成功')
  dialogVisible.value = false
}

async function handleDelete(tag) {
  await ElMessageBox.confirm(`删除标签「${tag.name}」？相关 FAQ 的标签将被移除`, '确认', { type: 'warning' })
  faqStore.deleteTag(tag.id)
  ElMessage.success('已删除')
}
</script>

<style scoped>
.tag-card { margin-bottom: 12px; text-align: center; transition: all 0.2s; }
.tag-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.08); }
.tag-header { display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 8px; }
.tag-count { font-size: 12px; color: #909399; }
</style>
