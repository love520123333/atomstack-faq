<template>
  <div class="page-container">
    <div class="page-title"><el-icon><Search /></el-icon> {{ isHelp ? '搜索帮助' : '高级搜索' }}</div>

    <el-card shadow="never" class="search-card mb-16">
      <el-row :gutter="16">
        <el-col :span="24">
          <el-input v-model="query" placeholder="输入关键词，支持标题、内容、方案、关键词全文搜索..." :prefix-icon="Search" clearable size="large" @keyup.enter="doSearch" />
        </el-col>
      </el-row>
      <el-row :gutter="12" style="margin-top:16px">
        <el-col :xs="24" :sm="6">
          <el-select v-model="optMachine" placeholder="选择机型" clearable style="width:100%" @change="doSearch">
            <el-option-group v-for="cat in machineStore.categories" :key="cat.id" :label="cat.name">
              <el-option v-for="m in machineStore.machines.filter(x=>x.categoryId===cat.id)" :key="m.id" :label="m.name" :value="m.id" />
            </el-option-group>
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="4">
          <el-select v-model="optCategory" placeholder="分类" clearable style="width:100%" @change="doSearch">
            <el-option v-for="cat in machineStore.categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="4">
          <el-select v-model="optTag" placeholder="标签" clearable style="width:100%" @change="doSearch">
            <el-option v-for="tag in faqStore.tags" :key="tag.id" :label="tag.name" :value="tag.id" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="3">
          <el-select v-model="optPriority" placeholder="优先级" clearable style="width:100%" @change="doSearch">
            <el-option label="紧急" value="critical" /><el-option label="高" value="high" /><el-option label="中" value="medium" /><el-option label="低" value="low" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="3">
          <el-select v-model="optStatus" placeholder="状态" clearable style="width:100%" @change="doSearch">
            <el-option label="已发布" value="published" /><el-option label="草稿" value="draft" /><el-option label="已归档" value="archived" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="4">
          <el-select v-model="sortBy" style="width:100%" @change="doSearch">
            <el-option label="最新" value="newest" /><el-option label="最旧" value="oldest" /><el-option label="热门" value="popular" /><el-option label="评分" value="rating" />
          </el-select>
        </el-col>
      </el-row>
      <div style="margin-top:12px;display:flex;gap:8px">
        <el-button type="primary" :icon="Search" @click="doSearch">搜索</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </div>
    </el-card>

    <!-- 选中机型提示 -->
    <div v-if="optMachine && !query.trim()" class="machine-hint">
      <el-tag :color="selectedMachine?.categoryId && machineStore.getCategory(selectedMachine.categoryId)?.color" effect="dark" size="large" style="border:none">
        {{ selectedMachine?.name }}
      </el-tag>
      <span>全部 <strong>{{ results.length }}</strong> 条 FAQ</span>
      <el-button type="primary" text @click="$router.push(machineDetailRoute(optMachine))">查看机型详情 →</el-button>
    </div>

    <div v-if="searched" style="margin-bottom:12px;color:#909399;font-size:13px">
      找到 <strong style="color:#1a73e8">{{ results.length }}</strong> 条结果
      <span v-if="query"> 关键词「{{ query }}」</span>
    </div>

    <!-- 搜索结果 -->
    <div class="result-list" v-if="results.length">
      <div class="result-card" v-for="item in pagedResults" :key="item.id" @click="$router.push(faqRoute(item.id))">
        <div class="result-header">
          <el-tag size="small" :color="getPriorityColor(item.priority)" effect="dark" style="border:none">{{ getPriorityText(item.priority) }}</el-tag>
          <span class="result-title">{{ item.title }}</span>
          <div style="flex:1"></div>
          <el-tag size="small" type="info" style="cursor:pointer" @click.stop="$router.push(machineDetailRoute(item.machineId))">{{ machineStore.getMachine(item.machineId)?.name || '未知' }}</el-tag>
          <el-tag v-for="tid in (item.tags||[]).slice(0,3)" :key="tid" size="small" effect="plain" style="margin-left:4px" @click.stop="optTag=tid;doSearch()">{{ faqStore.getTagName(tid) }}</el-tag>
        </div>
        <p class="result-summary" v-if="item.summary">{{ truncate(item.summary, 150) }}</p>
        <div class="result-footer">
          <span><el-icon><View /></el-icon> {{ item.viewCount || 0 }}</span>
          <span><el-icon><Top /></el-icon> {{ item.helpfulCount || 0 }}</span>
          <span>{{ formatDate(item.updatedAt) }}</span>
        </div>
      </div>
    </div>
    <el-empty v-if="searched && !results.length" description="没有找到匹配的结果">
      <el-button type="primary" @click="query='';doSearch()">清除搜索</el-button>
    </el-empty>

    <div style="display:flex;justify-content:center;margin-top:20px" v-if="results.length > pageSize">
      <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="results.length" layout="prev, pager, next" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import { Search, View, Top } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { formatDate, getPriorityColor, getPriorityText, truncate } from '../utils'
import { initSampleData } from '../data/sampleData'

const route = useRoute()
const faqStore = useFaqStore()
const machineStore = useMachineStore()

// 判断是否在帮助中心路由下
const isHelp = computed(() => route.path.startsWith('/help'))
function machineDetailRoute(machineId) { return isHelp.value ? `/help/machines/${machineId}` : `/machines/${machineId}` }
function faqRoute(id) { return isHelp.value ? `/help/faq/${id}` : `/faq/${id}` }

const query = ref('')
const optMachine = ref('')
const optCategory = ref('')
const optTag = ref('')
const optPriority = ref('')
const optStatus = ref('')
const sortBy = ref('newest')
const searched = ref(false)
const currentPage = ref(1)
const pageSize = 20

const selectedMachine = computed(() => machineStore.getMachine(optMachine.value))

onMounted(() => {
  initSampleData(machineStore, faqStore)
})

// 响应 URL query 变化（包括首次加载和在当前页面改变 query 的情况）
watchEffect(() => {
  const q = route.query.q
  const machine = route.query.machine
  const tag = route.query.tag
  const category = route.query.category
  const priority = route.query.priority
  // 始终同步 query 参数（包括清空的情况）
  query.value = q ? String(q) : ''
  optMachine.value = machine ? String(machine) : ''
  optTag.value = tag ? String(tag) : ''
  optCategory.value = category ? String(category) : ''
  optPriority.value = priority ? String(priority) : ''
  if (q || machine || tag || category || priority) {
    searched.value = true
    currentPage.value = 1
  }
})

function doSearch() {
  searched.value = true
  currentPage.value = 1
}

function resetSearch() {
  query.value = ''; optMachine.value = ''; optCategory.value = ''; optTag.value = ''
  optPriority.value = ''; optStatus.value = ''; sortBy.value = 'newest'; searched.value = false
}

const results = computed(() => {
  if (!searched.value) return []
  return faqStore.searchFaqs(query.value || ' ', {
    machineId: optMachine.value,
    categoryId: optCategory.value ? optCategory.value : undefined,
    tagId: optTag.value,
    priority: optPriority.value,
    status: optStatus.value,
    sortBy: sortBy.value,
    machineStore
  })
})

const pagedResults = computed(() => results.value.slice((currentPage.value-1)*pageSize, currentPage.value*pageSize))
</script>

<style scoped>
.machine-hint {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  background: linear-gradient(135deg, #e8f0fe 0%, #f0f7ff 100%);
  border-radius: 10px; margin-bottom: 12px; font-size: 14px; color: #444;
}

.result-list { display: flex; flex-direction: column; gap: 8px; }
.result-card {
  padding: 16px 20px; border: 1px solid #f0f0f0; border-radius: 12px;
  cursor: pointer; transition: all 0.25s; background: #fff;
}
.result-card:hover {
  border-color: #1a73e8; background: #f8fbff;
  box-shadow: 0 4px 16px rgba(26,115,232,0.08);
  transform: translateY(-1px);
}
.result-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap; }
.result-title { font-size: 15px; font-weight: 600; color: #1d2129; }
.result-summary { font-size: 13px; color: #86909c; line-height: 1.6; margin: 0 0 8px; }
.result-footer { display: flex; align-items: center; gap: 16px; font-size: 12px; color: #c0c4cc; }
</style>
