<template>
  <div class="page-container">
    <div class="page-title">
      <el-icon><Document /></el-icon> FAQ 列表
      <div style="flex:1"></div>
      <el-button type="primary" :icon="Plus" @click="$router.push('/faq/create')">新建 FAQ</el-button>
    </div>

    <!-- 筛选栏 -->
    <el-card shadow="never" class="filter-card mb-16">
      <el-row :gutter="12" align="middle">
        <el-col :xs="24" :sm="6">
          <el-select v-model="filterMachine" placeholder="按机型" clearable style="width:100%" @change="doFilter">
            <el-option-group v-for="cat in machineStore.categories" :key="cat.id" :label="cat.name">
              <el-option v-for="m in machineStore.machines.filter(x=>x.categoryId===cat.id)" :key="m.id" :label="m.name" :value="m.id" />
            </el-option-group>
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="4">
          <el-select v-model="filterCategory" placeholder="按分类" clearable style="width:100%" @change="doFilter">
            <el-option v-for="cat in machineStore.categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="4">
          <el-select v-model="filterTag" placeholder="按标签" clearable style="width:100%" @change="doFilter">
            <el-option v-for="tag in faqStore.tags" :key="tag.id" :label="tag.name" :value="tag.id" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="4">
          <el-select v-model="filterPriority" placeholder="按优先级" clearable style="width:100%" @change="doFilter">
            <el-option label="紧急" value="critical" /><el-option label="高" value="high" /><el-option label="中" value="medium" /><el-option label="低" value="low" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="4">
          <el-select v-model="filterStatus" placeholder="按状态" clearable style="width:100%" @change="doFilter">
            <el-option label="已发布" value="published" /><el-option label="草稿" value="draft" /><el-option label="已归档" value="archived" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="2">
          <el-select v-model="sortBy" style="width:100%" @change="doFilter">
            <el-option label="最新" value="newest" /><el-option label="最旧" value="oldest" /><el-option label="热门" value="popular" /><el-option label="评分" value="rating" /><el-option label="有用" value="helpful" />
          </el-select>
        </el-col>
      </el-row>
    </el-card>

    <!-- 选中机型提示 + 搜索 -->
    <div v-if="filterMachine" class="machine-hint">
      <el-tag :color="selectedMachine?.categoryId && machineStore.getCategory(selectedMachine.categoryId)?.color" effect="dark" size="large" style="border:none">
        {{ selectedMachine?.name }}
      </el-tag>
      <span>共 <strong>{{ filteredData.length }}</strong> 条 FAQ</span>
      <el-button type="primary" text @click="$router.push(`/machines/${filterMachine}`)">查看机型详情 →</el-button>
    </div>

    <el-input v-model="searchText" placeholder="输入关键词搜索 FAQ 标题、内容、方案..." :prefix-icon="Search" clearable size="large" style="margin-bottom:16px" @input="doFilter" />

    <!-- FAQ 卡片列表 -->
    <div class="faq-card-list" v-if="pagedData.length">
      <div class="faq-card" v-for="row in pagedData" :key="row.id" @click="$router.push(`/faq/${row.id}`)">
        <div class="faq-card-left">
          <el-tag size="small" :color="getPriorityColor(row.priority)" effect="dark" style="border:none">{{ getPriorityText(row.priority) }}</el-tag>
          <div class="faq-card-title">{{ row.title }}</div>
          <div class="faq-card-tags">
            <el-tag v-for="tid in (row.tags||[]).slice(0,3)" :key="tid" size="small" effect="plain" style="margin-right:4px;cursor:pointer" @click.stop="$router.push(`/tags/${tid}`)">{{ faqStore.getTagName(tid) }}</el-tag>
          </div>
        </div>
        <div class="faq-card-right">
          <div class="faq-card-meta">
            <el-tag size="small" type="info" @click.stop="$router.push(`/machines/${row.machineId}`)" style="cursor:pointer">{{ machineStore.getMachine(row.machineId)?.name || '未指定' }}</el-tag>
            <span><el-icon><View /></el-icon> {{ row.viewCount || 0 }}</span>
            <span><el-icon><Top /></el-icon> {{ row.helpfulCount || 0 }}</span>
            <span>{{ formatDate(row.updatedAt) }}</span>
          </div>
          <p class="faq-card-summary" v-if="!filterMachine && row.summary">{{ truncate(row.summary, 80) }}</p>
        </div>
        <el-icon class="faq-card-arrow"><ArrowRight /></el-icon>
      </div>
    </div>
    <el-empty v-else description="暂无 FAQ" />

    <!-- 分页 -->
    <div style="display:flex;justify-content:center;margin-top:20px" v-if="filteredData.length > pageSize">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="filteredData.length" layout="prev, pager, next" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, Edit, Delete, Document, View, Top, ArrowRight } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { formatDate, getPriorityColor, getPriorityText, truncate } from '../utils'

const route = useRoute()
const router = useRouter()
const faqStore = useFaqStore()
const machineStore = useMachineStore()

const filterMachine = ref('')
const filterCategory = ref('')
const filterTag = ref('')
const filterPriority = ref('')
const filterStatus = ref('')
const sortBy = ref('newest')
const searchText = ref('')
const currentPage = ref(1)
const pageSize = 20

// 从 URL query 读取初始筛选条件
onMounted(() => {
  if (route.query.machine) filterMachine.value = route.query.machine
  if (route.query.category) filterCategory.value = route.query.category
  if (route.query.tag) filterTag.value = route.query.tag
  doFilter()
})

const selectedMachine = computed(() => machineStore.getMachine(filterMachine.value))

function doFilter() {
  currentPage.value = 1
}

const filteredData = computed(() => {
  let result = faqStore.faqs
  if (filterMachine.value) result = result.filter(f => f.machineId === filterMachine.value)
  if (filterCategory.value) {
    const mids = machineStore.machines.filter(m => m.categoryId === filterCategory.value).map(m => m.id)
    result = result.filter(f => mids.includes(f.machineId))
  }
  if (filterTag.value) result = result.filter(f => f.tags && f.tags.includes(filterTag.value))
  if (filterPriority.value) result = result.filter(f => f.priority === filterPriority.value)
  if (filterStatus.value) result = result.filter(f => f.status === filterStatus.value)
  if (searchText.value.trim()) {
    const q = searchText.value.toLowerCase()
    result = result.filter(f => f.title.toLowerCase().includes(q) || (f.content||'').toLowerCase().includes(q) || (f.summary||'').toLowerCase().includes(q) || (f.solution||'').toLowerCase().includes(q) || (f.keywords||'').toLowerCase().includes(q))
  }
  switch (sortBy.value) {
    case 'newest': result.sort((a,b) => new Date(b.updatedAt)-new Date(a.updatedAt)); break
    case 'oldest': result.sort((a,b) => new Date(a.updatedAt)-new Date(b.updatedAt)); break
    case 'popular': result.sort((a,b) => (b.viewCount||0)-(a.viewCount||0)); break
    case 'rating': result.sort((a,b) => (b.rating||0)-(a.rating||0)); break
    case 'helpful': result.sort((a,b) => (b.helpfulCount||0)-(a.helpfulCount||0)); break
  }
  return result
})

const pagedData = computed(() => filteredData.value.slice((currentPage.value-1)*pageSize, currentPage.value*pageSize))

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除 FAQ「${row.title}」？`, '删除确认', { type: 'warning' })
  faqStore.deleteFaq(row.id)
  ElMessage.success('已删除')
}
</script>

<style scoped>
.machine-hint {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: linear-gradient(135deg, #ecf5ff 0%, #f0f7ff 100%);
  border-radius: 10px; margin-bottom: 12px; font-size: 14px; color: #606266;
}

.faq-card-list { display: flex; flex-direction: column; gap: 8px; }
.faq-card {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 20px; border: 1px solid #e5e6eb; border-radius: 10px;
  cursor: pointer; transition: all 0.2s;
}
.faq-card:hover {
  border-color: #409eff; background: #f0f7ff;
  box-shadow: 0 2px 12px rgba(64,158,255,0.08);
}
.faq-card-left { flex: 1; min-width: 0; }
.faq-card-right { flex-shrink: 0; text-align: right; min-width: 140px; }
.faq-card-title { font-size: 14px; font-weight: 600; color: #1d2129; margin: 6px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.faq-card-tags { display: flex; flex-wrap: wrap; gap: 2px; }
.faq-card-meta { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #86909c; margin-bottom: 4px; flex-wrap: wrap; justify-content: flex-end; }
.faq-card-summary { font-size: 12px; color: #c0c4cc; margin: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 200px; }
.faq-card-arrow { color: #c0c4cc; transition: all 0.2s; flex-shrink: 0; }
.faq-card:hover .faq-card-arrow { color: #409eff; transform: translateX(4px); }
</style>
