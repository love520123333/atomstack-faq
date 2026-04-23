<template>
  <div class="page-container">
    <div class="page-title"><el-icon><DataAnalysis /></el-icon> 数据统计</div>

    <el-row :gutter="16" class="stat-row">
      <el-col :xs="12" :sm="6" v-for="s in stats" :key="s.label">
        <el-card shadow="hover" class="stat-card clickable" @click="s.action && s.action()">
          <div class="stat-number" :style="{ color: s.color }">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :xs="24" :lg="12">
        <el-card shadow="hover" class="mb-16">
          <template #header><span style="font-weight:600">📊 各分类 FAQ 数量</span></template>
          <div class="bar-chart">
            <div class="bar-item clickable" v-for="item in categoryStats" :key="item.name" @click="$router.push({ path: '/faq', query: { category: item.id } })">
              <span class="bar-label">{{ item.name }}</span>
              <div class="bar-track"><div class="bar-fill" :style="{ width: item.pct + '%', background: item.color }"></div></div>
              <span class="bar-value">{{ item.count }}</span>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover">
          <template #header><span style="font-weight:600">🏷️ 标签使用 TOP 10</span></template>
          <div class="bar-chart">
            <div class="bar-item clickable" v-for="item in tagStats" :key="item.id" @click="$router.push(`/tags/${item.id}`)">
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
            <el-table-column prop="name" label="机型" min-width="120">
              <template #default="{ row }">
                <router-link :to="`/machines/${row.id}`" class="link">{{ row.name }}</router-link>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="FAQ数" width="80" align="center">
              <template #default="{ row }">
                <router-link :to="{ path: '/faq', query: { machine: row.id } }" class="link">{{ row.count }}</router-link>
              </template>
            </el-table-column>
            <el-table-column prop="views" label="总浏览" width="80" align="center" />
          </el-table>
        </el-card>

        <el-card shadow="hover" class="mb-16">
          <template #header><span style="font-weight:600">📈 优先级分布</span></template>
          <div class="priority-dist">
            <div class="priority-item" v-for="item in priorityDist" :key="item.label">
              <el-tag :color="item.color" effect="dark" size="large" style="border:none;min-width:60px;text-align:center;cursor:pointer" @click="$router.push({ path: '/faq', query: { priority: item.value } })">{{ item.label }}</el-tag>
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
              <template #default="{ row }"><router-link :to="`/faq/${row.id}`" class="link">{{ row.title }}</router-link></template>
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
import { useRouter } from 'vue-router'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'

const router = useRouter()
const faqStore = useFaqStore()
const machineStore = useMachineStore()

const stats = computed(() => [
  { label: 'FAQ 总数', value: faqStore.faqCount, color: '#409eff', action: () => router.push('/faq') },
  { label: '机型数', value: machineStore.machineCount, color: '#67c23a', action: () => router.push('/machines') },
  { label: '分类数', value: machineStore.categoryCount, color: '#e6a23c', action: () => router.push('/categories') },
  { label: '标签数', value: faqStore.tags.length, color: '#b37feb', action: () => router.push('/tags') },
])

const categoryStats = computed(() => {
  const items = machineStore.categories.map(cat => {
    const count = faqStore.getFaqsByCategory(cat.id, machineStore).length
    return { id: cat.id, name: cat.name, count, color: cat.color }
  })
  const max = Math.max(...items.map(i => i.count), 1)
  return items.map(i => ({ ...i, pct: (i.count / max * 100).toFixed(0) * 1 })).sort((a, b) => b.count - a.count)
})

const tagStats = computed(() => {
  const sorted = [...faqStore.tags].sort((a, b) => b.usageCount - a.usageCount).slice(0, 10)
  const max = Math.max(...sorted.map(t => t.usageCount), 1)
  return sorted.map(t => ({ id: t.id, name: t.name, count: t.usageCount, color: t.color, pct: (t.usageCount / max * 100).toFixed(0) * 1 }))
})

const machineRank = computed(() => {
  return machineStore.machines.map(m => {
    const faqs = faqStore.getFaqsByMachine(m.id)
    return { id: m.id, name: m.name, count: faqs.length, views: faqs.reduce((s, f) => s + (f.viewCount || 0), 0) }
  }).sort((a, b) => b.count - a.count).slice(0, 10)
})

const priorityDist = computed(() => {
  const labels = { critical: { label: '紧急', color: '#f56c6c', value: 'critical' }, high: { label: '高', color: '#e6a23c', value: 'high' }, medium: { label: '中', color: '#409eff', value: 'medium' }, low: { label: '低', color: '#67c23a', value: 'low' } }
  return Object.entries(labels).map(([k, v]) => ({ ...v, count: faqStore.faqs.filter(f => f.priority === k).length }))
})
</script>

<style scoped>
.stat-card.clickable { cursor: pointer; transition: transform 0.2s; }
.stat-card.clickable:hover { transform: translateY(-2px); }
.stat-number { font-size: 32px; font-weight: 800; }
.stat-label { font-size: 13px; color: #909399; margin-top: 4px; }
.link { color: #409eff; text-decoration: none; }
.link:hover { text-decoration: underline; }
.bar-chart { display: flex; flex-direction: column; gap: 12px; }
.bar-item { display: flex; align-items: center; gap: 8px; }
.bar-item.clickable { cursor: pointer; padding: 4px 0; border-radius: 4px; }
.bar-item.clickable:hover { background: #f5f7fa; }
.bar-label { width: 120px; font-size: 13px; color: #606266; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bar-track { flex: 1; height: 20px; background: #f0f2f5; border-radius: 10px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 10px; transition: width 0.5s; }
.bar-value { width: 30px; text-align: right; font-size: 13px; font-weight: 600; color: #303133; }
.priority-dist { display: flex; flex-direction: column; gap: 12px; }
.priority-item { display: flex; align-items: center; gap: 16px; }
.priority-count { font-size: 24px; font-weight: 700; color: #303133; }
.mb-16 { margin-bottom: 16px; }
</style>
