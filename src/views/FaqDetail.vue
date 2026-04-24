<template>
  <div class="page-container" v-if="faq">
    <div class="page-title no-print">
      <el-button text @click="goBack"><el-icon><ArrowLeft /></el-icon> 返回</el-button>
      <div style="flex:1"></div>
      <el-button :icon="faqStore.isFavorite(faq.id)?StarFilled:Star" :type="faqStore.isFavorite(faq.id)?'warning':'default'" @click="faqStore.toggleFavorite(faq.id)">
        {{ faqStore.isFavorite(faq.id) ? '已收藏' : '收藏' }}
      </el-button>
      <el-button v-if="!isHelp" :icon="Edit" type="warning" @click="$router.push(`/faq/${faq.id}/edit`)">编辑</el-button>
      <el-button :icon="Download" @click="downloadMd">导出 MD</el-button>
      <el-button :icon="Printer" @click="handlePrint">打印</el-button>
      <el-dropdown v-if="!isHelp" trigger="click">
        <el-button :icon="MoreFilled" />
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="downloadHtml">导出 HTML</el-dropdown-item>
            <el-dropdown-item @click="markHelpful">标记有用</el-dropdown-item>
            <el-dropdown-item divided @click="handleDelete"><span style="color:#f56c6c">删除</span></el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="18">
        <el-card shadow="never">
          <!-- 标题区 -->
          <h1 class="faq-title">
            <el-tag :color="getPriorityColor(faq.priority)" effect="dark" size="small" style="border:none;margin-right:8px">{{ getPriorityText(faq.priority) }}</el-tag>
            {{ faq.title }}
          </h1>
          <p class="faq-meta">
            <span style="cursor:pointer" @click="$router.push(machineRoute)"><el-icon><Monitor /></el-icon> {{ machine?.name || '未知机型' }}</span>
            <span><el-icon><Folder /></el-icon> {{ machineStore.getCategoryName(machine?.categoryId) }}</span>
            <span><el-icon><View /></el-icon> {{ faq.viewCount || 0 }} 次浏览</span>
            <span><el-icon><Clock /></el-icon> {{ formatFullDate(faq.updatedAt) }}</span>
          </p>

          <!-- 标签 -->
          <div class="faq-tags" v-if="faq.tags && faq.tags.length">
            <el-tag v-for="tid in faq.tags" :key="tid" :color="faqStore.getTag(tid)?.color" effect="plain" style="border:none;margin:2px;cursor:pointer" @click="$router.push({ path: searchRoute, query:{ tag: tid } })">
              {{ faqStore.getTagName(tid) }}
            </el-tag>
          </div>

          <el-divider />

          <!-- 问题描述 -->
          <div v-if="faq.summary" class="section">
            <h2>问题描述</h2>
            <div class="faq-content" v-html="renderedSummary"></div>
          </div>

          <!-- 解决方案 -->
          <div v-if="faq.solution" class="section">
            <h2>解决方案</h2>
            <div class="faq-content" v-html="renderedSolution"></div>
          </div>

          <!-- 补充内容 -->
          <div v-if="faq.content" class="section">
            <h2>补充说明</h2>
            <div class="faq-content" v-html="renderedContent"></div>
          </div>

          <el-divider />

          <!-- 互动区 -->
          <div class="action-bar">
            <div class="action-item">
              <span style="font-weight:500">这篇文章有帮助吗？</span>
              <el-button :icon="Top" type="success" @click="rate(5)">有用 ({{ faq.helpfulCount || 0 }})</el-button>
              <el-rate v-model="myRating" @change="rate" style="margin-left:16px" />
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧信息栏 -->
      <el-col :xs="24" :lg="6" class="no-print">
        <el-card shadow="never" class="mb-16">
          <template #header><span style="font-weight:600">信息</span></template>
          <div class="info-list">
            <div class="info-item"><span class="info-label">状态</span><el-tag :color="getStatusColor(faq.status)" effect="dark" size="small" style="border:none">{{ getStatusText(faq.status) }}</el-tag></div>
            <div class="info-item"><span class="info-label">创建时间</span><span>{{ formatFullDate(faq.createdAt) }}</span></div>
            <div class="info-item"><span class="info-label">更新时间</span><span>{{ formatFullDate(faq.updatedAt) }}</span></div>
            <div class="info-item"><span class="info-label">浏览次数</span><span>{{ faq.viewCount || 0 }}</span></div>
            <div class="info-item"><span class="info-label">有用次数</span><span>{{ faq.helpfulCount || 0 }}</span></div>
            <div class="info-item"><span class="info-label">评分</span><span>{{ faq.rating || '-' }} / 5 ({{ faq.ratingCount || 0 }} 人)</span></div>
          </div>
        </el-card>

        <el-card shadow="never" class="mb-16">
          <template #header><span style="font-weight:600">相关 FAQ</span></template>
          <div v-if="relatedFaqs.length">
            <div class="related-item" v-for="r in relatedFaqs" :key="r.id" @click="$router.push(faqRoute(r.id))">
              <el-tag size="small" :color="getPriorityColor(r.priority)" effect="dark" style="border:none;margin-right:4px">{{ getPriorityText(r.priority) }}</el-tag>
              <span class="related-title">{{ r.title }}</span>
            </div>
          </div>
          <el-empty v-else description="暂无相关 FAQ" :image-size="40" />
        </el-card>

        <el-card shadow="never">
          <template #header><span style="font-weight:600">关键词</span></template>
          <div v-if="faq.keywords">
            <el-tag v-for="kw in faq.keywords.split(',').map(s=>s.trim()).filter(Boolean)" :key="kw" size="small" effect="plain" style="margin:3px;cursor:pointer" @click="$router.push({ path: searchRoute, query:{ q: kw } })">
              {{ kw }}
            </el-tag>
          </div>
          <span v-else style="color:#909399;font-size:13px">无关键词</span>
        </el-card>
      </el-col>
    </el-row>
  </div>
  <el-empty v-else description="FAQ 不存在或已删除" />
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Star, StarFilled, Edit, Download, Printer, MoreFilled, ArrowLeft, Monitor, Folder, View, Clock, Top } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { renderMarkdown, formatFullDate, getPriorityColor, getPriorityText, getStatusColor, getStatusText, exportAsMarkdown, exportAsHtml, downloadFile } from '../utils'
import { initSampleData } from '../data/sampleData'

const route = useRoute()
const router = useRouter()
const faqStore = useFaqStore()
const machineStore = useMachineStore()
const myRating = ref(0)

// 判断是否在帮助中心路由下
const isHelp = computed(() => route.path.startsWith('/help'))
const machineRoute = computed(() => {
  if (!faq.value) return isHelp.value ? '/help' : '/machines'
  return isHelp.value ? `/help/machines/${faq.value.machineId}` : `/machines/${faq.value.machineId}`
})
const searchRoute = computed(() => isHelp.value ? '/help/search' : '/search')
function faqRoute(id) { return isHelp.value ? `/help/faq/${id}` : `/faq/${id}` }

const faq = computed(() => faqStore.getFaq(route.params.id))
const machine = computed(() => faq.value ? machineStore.getMachine(faq.value.machineId) : null)
const renderedSummary = computed(() => renderMarkdown(faq.value?.summary))
const renderedSolution = computed(() => renderMarkdown(faq.value?.solution))
const renderedContent = computed(() => renderMarkdown(faq.value?.content))

const relatedFaqs = computed(() => {
  if (!faq.value) return []
  return faqStore.faqs
    .filter(f => f.id !== faq.value.id && (f.machineId === faq.value.machineId || (f.tags||[]).some(t => (faq.value.tags||[]).includes(t))))
    .sort((a, b) => (b.viewCount || 0) - (a.viewCount || 0))
    .slice(0, 8)
})

onMounted(async () => {
  initSampleData(machineStore, faqStore)
  await nextTick()
  if (faq.value) {
    faqStore.recordView(faq.value.id)
    myRating.value = faq.value.rating || 0
  }
})

function rate(val) { if (faq.value && val) { faqStore.rateFaq(faq.value.id, val); ElMessage.success('感谢评价！') } }
function markHelpful() { if (faq.value) { faqStore.markHelpful(faq.value.id); ElMessage.success('已标记有用') } }
function handlePrint() { window.print() }

// 智能返回：优先回退历史，无历史时跳到合适的列表页
function goBack() {
  if (window.history.length > 1) {
    router.back()
  } else {
    if (isHelp.value) {
      if (faq.value) router.push(`/help/machines/${faq.value.machineId}`)
      else router.push('/help')
    } else {
      if (faq.value) router.push(`/machines/${faq.value.machineId}`)
      else router.push('/faq')
    }
  }
}

function downloadMd() { if (faq.value) downloadFile(exportAsMarkdown(faq.value, machineStore), `${faq.value.title}.md`) }
function downloadHtml() { if (faq.value) downloadFile(exportAsHtml(faq.value, machineStore), `${faq.value.title}.html`, 'text/html') }

async function handleDelete() {
  await ElMessageBox.confirm('确定删除此 FAQ？', '删除确认', { type: 'warning' })
  faqStore.deleteFaq(route.params.id)
  ElMessage.success('已删除')
  router.push('/faq')
}
</script>

<style scoped>
.faq-title { font-size: 24px; font-weight: 700; line-height: 1.4; margin-bottom: 12px; display: flex; align-items: center; flex-wrap: wrap; }
.faq-meta { display: flex; flex-wrap: wrap; gap: 16px; color: #909399; font-size: 13px; align-items: center; }
.faq-meta span { display: flex; align-items: center; gap: 4px; }
.faq-tags { margin: 12px 0; display: flex; flex-wrap: wrap; }
.section { margin: 16px 0; }
.section h2 { font-size: 18px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #1a73e8; }
.action-bar { display: flex; justify-content: center; padding: 16px 0; }
.action-item { display: flex; align-items: center; gap: 12px; font-size: 14px; }
.mb-16 { margin-bottom: 16px; }
.info-list { display: flex; flex-direction: column; gap: 10px; }
.info-item { display: flex; justify-content: space-between; align-items: center; font-size: 13px; }
.info-label { color: #909399; }
.related-item { padding: 6px 0; cursor: pointer; font-size: 13px; border-bottom: 1px solid #f0f0f0; }
.related-item:hover .related-title { color: #1a73e8; }
.related-title { transition: color 0.2s; }
</style>
