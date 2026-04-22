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

    <!-- 搜索和列表 -->
    <el-input v-model="searchText" placeholder="输入关键词搜索 FAQ 标题、内容、方案..." :prefix-icon="Search" clearable size="large" style="margin-bottom:16px" @input="doFilter" />

    <el-table :data="pagedData" stripe v-if="filteredData.length" style="width:100%">
      <el-table-column prop="title" label="标题" min-width="260">
        <template #default="{ row }">
          <div style="display:flex;align-items:center;gap:8px">
            <el-tag size="small" :color="getPriorityColor(row.priority)" effect="dark" style="border:none">{{ getPriorityText(row.priority) }}</el-tag>
            <router-link :to="`/faq/${row.id}`" class="faq-link" style="font-weight:500">{{ row.title }}</router-link>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="机型" width="130">
        <template #default="{ row }"><el-tag size="small" type="info">{{ machineStore.getMachine(row.machineId)?.name || '未指定' }}</el-tag></template>
      </el-table-column>
      <el-table-column label="标签" width="150">
        <template #default="{ row }">
          <el-tag v-for="tid in (row.tags||[]).slice(0,2)" :key="tid" size="small" effect="plain" style="margin:2px">{{ faqStore.getTagName(tid) }}</el-tag>
          <el-tag v-if="(row.tags||[]).length>2" size="small" type="info">+{{ row.tags.length-2 }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="80" align="center">
        <template #default="{ row }"><el-tag size="small" :color="getStatusColor(row.status)" effect="dark" style="border:none">{{ getStatusText(row.status) }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="viewCount" label="浏览" width="70" align="center" sortable />
      <el-table-column prop="helpfulCount" label="有用" width="70" align="center" sortable />
      <el-table-column label="更新时间" width="110">
        <template #default="{ row }">{{ formatDate(row.updatedAt) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <el-button text type="primary" size="small" @click="$router.push(`/faq/${row.id}`)">查看</el-button>
          <el-button text type="warning" size="small" @click="$router.push(`/faq/${row.id}/edit`)">编辑</el-button>
          <el-button text type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-empty v-if="!filteredData.length" description="没有找到匹配的 FAQ" />

    <div style="display:flex;justify-content:center;margin-top:20px" v-if="filteredData.length > pageSize">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="filteredData.length" layout="prev, pager, next" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { formatDate, getPriorityColor, getPriorityText, getStatusColor, getStatusText } from '../utils'

const route = useRoute()
const router = useRouter()
const faqStore = useFaqStore()
const machineStore = useMachineStore()

const searchText = ref('')
const filterMachine = ref('')
const filterCategory = ref('')
const filterTag = ref('')
const filterPriority = ref('')
const filterStatus = ref('')
const sortBy = ref('newest')
const currentPage = ref(1)
const pageSize = 20

onMounted(() => {
  // 读取 URL query 参数
  if (route.query.machine) filterMachine.value = route.query.machine
  if (route.query.category) filterCategory.value = route.query.category
  if (route.query.tag) filterTag.value = route.query.tag
  if (route.query.q) searchText.value = route.query.q
})

const filteredData = computed(() => {
  return faqStore.searchFaqs(searchText.value || '.*', {
    machineId: filterMachine.value || undefined,
    categoryId: filterCategory.value || undefined,
    tagId: filterTag.value || undefined,
    priority: filterPriority.value || undefined,
    status: filterStatus.value || undefined,
    sortBy: sortBy.value,
    machineStore
  })
})

const pagedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredData.value.slice(start, start + pageSize)
})

function doFilter() { currentPage.value = 1 }

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除「${row.title}」？`, '删除确认', { type: 'warning' })
  faqStore.deleteFaq(row.id)
  ElMessage.success('删除成功')
}
</script>

<style scoped>
.mb-16 { margin-bottom: 16px; }
.filter-card { background: #fafafa; }
.faq-link { color: #303133; text-decoration: none; }
.faq-link:hover { color: #409eff; text-decoration: underline; }
</style>
