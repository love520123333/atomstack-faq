<template>
  <div class="page-container">
    <div class="page-title"><el-icon><DataAnalysis /></el-icon> 数据统计</div>

    <el-row :gutter="16" class="stat-row">
      <el-col :xs="12" :sm="6" v-for="s in stats" :key="s.label">
        <el-card shadow="hover" class="stat-card"><div class="stat-number" :style="{ color: s.color }">{{ s.value }}</div><div class="stat-label">{{ s.label }}</div></el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="mb-16">
          <template #header><span style="font-weight:600">📊 各分类 FAQ 数量</span></template>
          <div class="bar-chart">
            <div class="bar-item" v-for="item in categoryStats" :key="item.name">
              <span class="bar-label">{{ item.name }}</span>
              <div class="bar-track"><div class="bar-fill" :style="{ width: item.pct + '%', background: item.color }"></div></div>
              <span class="bar-value">{{ item.count }}</span>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover">
          <template #header><span style="font-weight:600">🏷️ 标签使用 TOP 10</span></template>
          <div class="bar-chart">
            <div class="bar-item" v-for="item in tagStats" :key="item.name">
              <span class="bar-label">{{ item.name }}</span>
              <div class="bar-track"><div class="bar-fill" :style="{ width: item.pct + '%', background: item.color }"></div></div>
              <span class="bar-value">{{ item.count }}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="mb-16">
          <template #header><span style="font-weight:600">🏆 机型 FAQ 排行 TOP 10</span></template>
          <el-table :data="machineRank" stripe size="small">
            <el-table-column type="index" label="#" width="40" />
            <el-table-column prop="name" label="机型" min-width="120" />
            <el-table-column prop="count" label="FAQ数" width="80" align="center" />
            <el-table-column prop="views" label="总浏览" width="80" align="center" />
          </el-table>
        </el-card>

        <el-card shadow="hover" class="mb-16">
          <template #header><span style="font-weight:600">📈 优先级分布</span></template>
          <div class="priority-dist">
            <div class="priority-item" v-for="item in priorityDist" :key="item.label">
              <el-tag :color="item.color" effect="dark" size="large" style="border:none;min-width:60px;text-align:center">{{ item.label }}</el-tag>
              <div style="flex:1"></div>
              <span class="priority-count">{{ item.count }}</span>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover">
          <template #header><span style="font-weight:600">🔥 浏览最多 TOP 10</span></template>
          <el-table :data="faqStore.popularFaqs.slice(0,10)" stripe size="small">
            <el-table-column type="index" label="#" width="40" />
            <el-table-column prop="title" label="标题" min-width="180">
              <template #default="{ row }"><router-link :to="`/faq/${row.id}`" style="color:#409eff;text-decoration:none">{{ row.title }}</router-link></template>
            </el-table-column>
            <el-table-column prop="viewCount" label="浏览" width="70" align="center" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'

const faqStore = useFaqStore()
const machineStore = useMachineStore()

const stats = computed(() => [
  { label: 'FAQ 总数', value: faqStore.faqCount, color: '#409eff' },
  { label: '总浏览量', value: faqStore.faqs.reduce((s, f) => s + (f.viewCount || 0), 0), color: '#67c23a' },
  { label: '总有用数', value: faqStore.faqs.reduce((s, f) => s + (f.helpfulCount || 0), 0), color: '#e6a23c' },
  { label: '平均评分', value: faqStore.faqs.length ? (faqStore.faqs.reduce((s, f) => s + (f.rating || 0), 0) / faqStore.faqs.length).toFixed(1) : '-', color: '#f56c6c' }
])

const categoryStats = computed(() => {
  const max = Math.max(...machineStore.categories.map(c => faqStore.getFaqsByCategory(c.id, machineStore).length), 1)
  return machineStore.categories.map(c => ({
    name: c.name.replace(/激光雕刻机|雕刻机|系列/g, ''),
    count: faqStore.getFaqsByCategory(c.id, machineStore).length,
    pct: Math.round((faqStore.getFaqsByCategory(c.id, machineStore).length / max) * 100),
    color: c.color
  })).sort((a, b) => b.count - a.count)
})

const tagStats = computed(() => {
  const max = Math.max(...faqStore.tags.map(t => t.usageCount), 1)
  return [...faqStore.tags].sort((a, b) => b.usageCount - a.usageCount).slice(0, 10).map(t => ({
    name: t.name, count: t.usageCount, pct: Math.round((t.usageCount / max) * 100), color: t.color
  }))
})

const machineRank = computed(() => {
  return machineStore.machines.map(m => {
    const mfaqs = faqStore.getFaqsByMachine(m.id)
    return { name: m.name, count: mfaqs.length, views: mfaqs.reduce((s, f) => s + (f.viewCount || 0), 0) }
  }).sort((a, b) => b.count - a.count).slice(0, 10)
})

const priorityDist = computed(() => {
  const map = { critical: { label: '紧急', color: '#f56c6c' }, high: { label: '高', color: '#e6a23c' }, medium: { label: '中', color: '#409eff' }, low: { label: '低', color: '#67c23a' } }
  return Object.entries(map).map(([k, v]) => ({ ...v, count: faqStore.faqs.filter(f => f.priority === k).length }))
})
</script>

<style scoped>
.stat-row { margin-bottom: 20px; }
.stat-card { text-align: center; border-radius: 12px; }
.stat-number { font-size: 36px; font-weight: 800; }
.stat-label { font-size: 13px; color: #909399; margin-top: 4px; }
.mb-16 { margin-bottom: 16px; }
.bar-chart { display: flex; flex-direction: column; gap: 10px; }
.bar-item { display: flex; align-items: center; gap: 10px; }
.bar-label { width: 100px; text-align: right; font-size: 12px; color: #606266; flex-shrink: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.bar-track { flex: 1; height: 20px; background: #f0f2f5; border-radius: 4px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 4px; transition: width 0.5s; min-width: 2px; }
.bar-value { width: 30px; text-align: left; font-size: 12px; font-weight: 600; }
.priority-dist { display: flex; flex-direction: column; gap: 12px; }
.priority-item { display: flex; align-items: center; }
.priority-count { font-size: 18px; font-weight: 700; margin-left: 16px; }
</style>
