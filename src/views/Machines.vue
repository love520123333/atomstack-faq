<template>
  <div class="page-container">
    <div class="page-title">
      <el-icon><Monitor /></el-icon> 机型管理
      <div style="flex:1"></div>
      <el-button type="primary" :icon="Plus" @click="openDialog()">添加机型</el-button>
    </div>

    <!-- 分类筛选 -->
    <div class="filter-bar">
      <el-radio-group v-model="filterCategory" @change="currentPage=1">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button v-for="cat in machineStore.categories" :key="cat.id" :label="cat.id">{{ cat.name }}</el-radio-button>
      </el-radio-group>
      <el-input v-model="filterText" placeholder="搜索机型..." :prefix-icon="Search" clearable style="width:240px;margin-left:16px" @input="currentPage=1" />
    </div>

    <!-- 机型卡片网格 -->
    <el-row :gutter="16">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="machine in filteredMachines" :key="machine.id">
        <el-card shadow="hover" class="machine-card" :body-style="{ padding: '0' }" @click="$router.push(`/machines/${machine.id}`)">
          <!-- 卡片图片 -->
          <div class="card-image-wrap">
            <img :src="machine.image" :alt="machine.name" class="card-image" loading="lazy" @error="handleImgError($event, machine.id)" />
            <div class="card-image-fallback" v-if="imgFailed[machine.id]">
              <div class="fallback-inner">
                <span class="fallback-letter">{{ machine.name.charAt(0) }}</span>
                <span class="fallback-name">{{ machine.name }}</span>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="machine-card-header">
              <el-tag :color="machineStore.getCategory(machine.categoryId)?.color" effect="dark" size="small" style="border:none">{{ machineStore.getCategoryName(machine.categoryId) }}</el-tag>
              <el-dropdown trigger="click" @click.stop>
                <el-button text size="small" @click.stop><el-icon><MoreFilled /></el-icon></el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click.stop="openDialog(machine)"><el-icon><Edit /></el-icon> 编辑</el-dropdown-item>
                    <el-dropdown-item @click.stop="$router.push(`/machines/${machine.id}`)"><el-icon><View /></el-icon> 查看详情</el-dropdown-item>
                    <el-dropdown-item @click.stop="$router.push(`/faq/create?machine=${machine.id}`)"><el-icon><Plus /></el-icon> 新建 FAQ</el-dropdown-item>
                    <el-dropdown-item divided @click.stop="handleDelete(machine)"><el-icon><Delete /></el-icon> <span style="color:#f56c6c">删除</span></el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
            <h3 class="machine-name">{{ machine.name }}</h3>
            <p class="machine-model" v-if="machine.model">{{ machine.model }}</p>
            <p class="machine-desc">{{ (machine.description || '暂无描述').substring(0, 50) }}{{ (machine.description || '').length > 50 ? '...' : '' }}</p>
            <div class="machine-footer">
              <el-tag size="small" type="info">{{ faqCountMap[machine.id] || 0 }} 条 FAQ</el-tag>
              <el-icon class="arrow-icon"><ArrowRight /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-empty v-if="!filteredMachines.length" description="暂无机型，点击上方按钮添加" />

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="editingMachine ? '编辑机型' : '添加机型'" width="600px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px" label-position="top">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="机型名称" required>
              <el-input v-model="form.name" placeholder="如 A10 Pro V2" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品图片URL">
              <el-input v-model="form.image" placeholder="https://..." />
              <div v-if="form.image" style="margin-top:8px;text-align:center">
                <img :src="form.image" style="max-height:80px;max-width:100%;border-radius:8px;border:1px solid #eee" @error="$event.target.style.display='none'" />
              </div>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="产品型号">
              <el-input v-model="form.model" placeholder="如 ATOMSTACK-A10PROV2" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属分类" required>
              <el-select v-model="form.categoryId" placeholder="选择分类" style="width:100%">
                <el-option v-for="cat in machineStore.categories" :key="cat.id" :label="cat.name" :value="cat.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="产品描述">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="简要描述该机型..." />
        </el-form-item>
        <el-divider content-position="left">规格参数</el-divider>
        <el-row :gutter="12" v-for="(spec, idx) in specEntries" :key="idx">
          <el-col :span="10"><el-input v-model="specEntries[idx].key" placeholder="参数名" /></el-col>
          <el-col :span="10"><el-input v-model="specEntries[idx].value" placeholder="参数值" /></el-col>
          <el-col :span="4"><el-button :icon="Delete" circle size="small" @click="specEntries.splice(idx,1)" /></el-col>
        </el-row>
        <el-button :icon="Plus" size="small" @click="specEntries.push({key:'',value:''})" style="margin-top:8px">添加参数</el-button>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Edit, Delete, MoreFilled, View, ArrowRight } from '@element-plus/icons-vue'
import { useMachineStore } from '../stores/machine'
import { useFaqStore } from '../stores/faq'
import { initSampleData } from '../data/sampleData'

const machineStore = useMachineStore()
const faqStore = useFaqStore()

const filterCategory = ref('')
const filterText = ref('')
const currentPage = ref(1)

// 图片加载失败追踪
const imgFailed = reactive({})

onMounted(() => {
  initSampleData(machineStore, faqStore)
})

function handleImgError(e, machineId) {
  imgFailed[machineId] = true
}

// FAQ 计数缓存（避免每次渲染都遍历全部 FAQ）
const faqCountMap = computed(() => {
  const map = {}
  for (const faq of faqStore.faqs) {
    map[faq.machineId] = (map[faq.machineId] || 0) + 1
  }
  return map
})

const filteredMachines = computed(() => {
  let list = machineStore.machines
  if (filterCategory.value) list = list.filter(m => m.categoryId === filterCategory.value)
  if (filterText.value) {
    const q = filterText.value.toLowerCase()
    list = list.filter(m => m.name.toLowerCase().includes(q) || (m.model || '').toLowerCase().includes(q))
  }
  return list
})

const dialogVisible = ref(false)
const editingMachine = ref(null)
const form = ref({ name: '', model: '', image: '', categoryId: '', description: '', specs: {} })
const specEntries = ref([])

function openDialog(machine = null) {
  editingMachine.value = machine
  if (machine) {
    form.value = { name: machine.name, model: machine.model || '', image: machine.image || '', categoryId: machine.categoryId || '', description: machine.description || '', specs: machine.specs ? { ...machine.specs } : {} }
    specEntries.value = Object.entries(form.value.specs).map(([k, v]) => ({ key: k, value: v }))
  } else {
    form.value = { name: '', model: '', image: '', categoryId: '', description: '', specs: {} }
    specEntries.value = []
  }
  dialogVisible.value = true
}

function handleSave() {
  if (!form.value.name.trim()) { ElMessage.warning('请输入机型名称'); return }
  if (!form.value.categoryId) { ElMessage.warning('请选择分类'); return }
  const specs = {}
  specEntries.value.forEach(s => { if (s.key.trim() && s.value.trim()) specs[s.key.trim()] = s.value.trim() })
  const data = { ...form.value, specs }
  if (editingMachine.value) {
    machineStore.updateMachine(editingMachine.value.id, data)
    ElMessage.success('更新成功')
  } else {
    machineStore.addMachine(data)
    ElMessage.success('添加成功')
  }
  dialogVisible.value = false
}

async function handleDelete(machine) {
  const count = faqCountMap.value[machine.id] || 0
  const msg = count > 0 ? `该机型下有 ${count} 条 FAQ，删除后 FAQ 将变为无机型状态，确定删除？` : `确定删除机型「${machine.name}」？`
  await ElMessageBox.confirm(msg, '删除确认', { type: 'warning' })
  machineStore.deleteMachine(machine.id)
  ElMessage.success('删除成功')
}
</script>

<style scoped>
.filter-bar { margin-bottom: 16px; display: flex; align-items: center; flex-wrap: wrap; gap: 8px; }

.machine-card {
  margin-bottom: 16px;
  overflow: hidden; border-radius: 12px;
  cursor: pointer;
  /* 移除 transition: transform，减少 GPU 重绘 */
}
.machine-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}
.card-image-wrap {
  height: 150px; background: #f5f7fa;
  display: flex; align-items: center; justify-content: center; overflow: hidden;
  position: relative;
}
.card-image {
  width: 100%; height: 100%; object-fit: cover;
  position: absolute; top: 0; left: 0;
  background: transparent;
}
.card-image-fallback {
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  display: flex; align-items: center; justify-content: center;
  z-index: 1;
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
}
.fallback-inner {
  text-align: center; color: rgba(255,255,255,0.9);
}
.fallback-letter {
  display: block; font-size: 32px; font-weight: 900; margin-bottom: 4px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.fallback-name {
  font-size: 11px; opacity: 0.7; letter-spacing: 0.5px;
}

.card-body { padding: 14px 16px; }
.machine-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.machine-name { font-size: 16px; font-weight: 700; margin: 2px 0; color: #1d2129; }
.machine-model { font-size: 11px; color: #86909c; margin: 0 0 4px; }
.machine-desc { font-size: 12px; color: #86909c; margin: 6px 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.5; }

.machine-footer {
  display: flex; justify-content: space-between; align-items: center;
  padding-top: 8px; border-top: 1px solid #f2f3f5; margin-top: 8px;
}
.arrow-icon { color: #c0c4cc; }
.machine-card:hover .arrow-icon { color: #409eff; }
</style>
