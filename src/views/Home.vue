<template>
  <div class="page-container">
    <!-- 欢迎横幅 -->
    <div class="welcome-banner">
      <div class="welcome-text">
        <h2>欢迎回来，管理员</h2>
        <p>AtomStack FAQ 知识库管理系统 · {{ currentTime }}</p>
      </div>
      <div class="welcome-actions">
        <el-button type="primary" :icon="Plus" @click="$router.push('/faq/create')">新建 FAQ</el-button>
        <el-button :icon="View" @click="$router.push('/help')">帮助中心</el-button>
      </div>
    </div>

    <!-- 顶部统计卡片 -->
    <el-row :gutter="16" class="stat-row">
      <el-col :xs="12" :sm="6" v-for="s in stats" :key="s.label">
        <el-card class="stat-card" :body-style="{ padding: '24px' }" @click="s.action && s.action()">
          <div class="stat-icon-wrap" :style="{ background: s.color + '12' }">
            <el-icon :size="24" :color="s.color"><component :is="s.icon" /></el-icon>
          </div>
          <div class="stat-number" :style="{ color: s.color }">{{ s.value }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <!-- 左侧 -->
      <el-col :xs="24" :lg="16">
        <!-- 快速操作 -->
        <el-card shadow="hover" class="mb-16">
          <template #header><span style="font-weight:700">快速操作</span></template>
          <div class="quick-actions">
            <div class="quick-action-item" @click="$router.push('/faq/create')">
              <el-icon :size="20" color="#1a73e8"><Plus /></el-icon>
              <span>新建 FAQ</span>
            </div>
            <div class="quick-action-item" @click="$router.push('/machines')">
              <el-icon :size="20" color="#67c23a"><Monitor /></el-icon>
              <span>机型管理</span>
            </div>
            <div class="quick-action-item" @click="$router.push('/search')">
              <el-icon :size="20" color="#e6a23c"><Search /></el-icon>
              <span>搜索方案</span>
            </div>
            <div class="quick-action-item" @click="$router.push('/faq')">
              <el-icon :size="20" color="#909399"><Document /></el-icon>
              <span>浏览全部</span>
            </div>
            <div class="quick-action-item" @click="$router.push('/statistics')">
              <el-icon :size="20" color="#b37feb"><DataAnalysis /></el-icon>
              <span>数据统计</span>
            </div>
          </div>
        </el-card>

        <!-- 最近更新 FAQ -->
        <el-card shadow="hover" class="mb-16">
          <template #header><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:700">最近更新</span><el-button text type="primary" @click="$router.push('/faq')">查看全部 →</el-button></div></template>
          <el-table :data="faqStore.recentFaqs.slice(0, 5)" stripe v-if="faqStore.recentFaqs.length" size="large">
            <el-table-column prop="title" label="标题" min-width="200">
              <template #default="{ row }">
                <router-link :to="`/faq/${row.id}`" class="faq-link">{{ row.title }}</router-link>
              </template>
            </el-table-column>
            <el-table-column label="机型" width="140">
              <template #default="{ row }">
                <el-tag size="small" effect="plain">{{ machineStore.getMachine(row.machineId)?.name || '-' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="优先级" width="80" align="center">
              <template #default="{ row }"><el-tag size="small" :color="getPriorityColor(row.priority)" effect="dark" style="border:none">{{ getPriorityText(row.priority) }}</el-tag></template>
            </el-table-column>
            <el-table-column label="更新时间" width="120">
              <template #default="{ row }">{{ formatDate(row.updatedAt) }}</template>
            </el-table-column>
          </el-table>
          <el-empty v-else description="暂无 FAQ，快去创建第一条吧" :image-size="80" />
        </el-card>

        <!-- 热门 FAQ -->
        <el-card shadow="hover">
          <template #header><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:700">热门 FAQ</span><el-button text type="primary" @click="$router.push('/faq?sortBy=popular')">更多 →</el-button></div></template>
          <el-table :data="faqStore.popularFaqs.slice(0, 5)" stripe v-if="faqStore.popularFaqs.length" size="large">
            <el-table-column type="index" label="#" width="50" />
            <el-table-column prop="title" label="标题" min-width="200">
              <template #default="{ row }"><router-link :to="`/faq/${row.id}`" class="faq-link">{{ row.title }}</router-link></template>
            </el-table-column>
            <el-table-column prop="viewCount" label="浏览" width="80" align="center" />
            <el-table-column prop="helpfulCount" label="有用" width="80" align="center" />
            <el-table-column label="评分" width="120" align="center">
              <template #default="{ row }">
                <el-rate :model-value="row.rating" disabled size="small" />
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-else description="暂无热门 FAQ" :image-size="80" />
        </el-card>
      </el-col>

      <!-- 右侧 -->
      <el-col :xs="24" :lg="8">
        <!-- 产品分类 -->
        <el-card shadow="hover" class="mb-16">
          <template #header><span style="font-weight:700">产品分类</span></template>
          <div class="category-list">
            <div class="category-item" v-for="cat in machineStore.categories" :key="cat.id" @click="$router.push({ path: '/faq', query: { category: cat.id } })">
              <div class="category-dot" :style="{ background: cat.color }"></div>
              <span class="category-name">{{ cat.name }}</span>
              <el-badge :value="machineStore.machines.filter(m => m.categoryId === cat.id).length" type="info" />
            </div>
          </div>
        </el-card>

        <!-- 浏览历史 -->
        <el-card shadow="hover" class="mb-16">
          <template #header><div style="display:flex;justify-content:space-between;align-items:center"><span style="font-weight:700">浏览历史</span><el-button text type="danger" size="small" @click="clearHistory">清除</el-button></div></template>
          <div class="history-list" v-if="faqStore.historyWithFaq.length">
            <div class="history-item" v-for="h in faqStore.historyWithFaq.slice(0, 8)" :key="h.faqId" @click="$router.push(`/faq/${h.faqId}`)">
              <span class="history-title">{{ h.faq.title }}</span>
              <span class="history-time">{{ formatDate(h.viewedAt) }}</span>
            </div>
          </div>
          <el-empty v-else description="暂无浏览记录" :image-size="60" />
        </el-card>

        <!-- 热门标签 -->
        <el-card shadow="hover">
          <template #header><span style="font-weight:700">热门标签</span></template>
          <div class="tag-cloud">
            <el-tag v-for="tag in [...faqStore.tags].sort((a,b)=>b.usageCount-a.usageCount).slice(0,12)" :key="tag.id" :color="tag.color" effect="plain" class="tag-item" style="cursor:pointer;border:none" @click="$router.push(`/tags/${tag.id}`)">
              {{ tag.name }} <span v-if="tag.usageCount">({{ tag.usageCount }})</span>
            </el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Search, Document, DataAnalysis, View, Monitor, Star, Folder } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { formatDate, getPriorityColor, getPriorityText } from '../utils'
import { initSampleData } from '../data/sampleData'

const faqStore = useFaqStore()
const machineStore = useMachineStore()
const router = useRouter()

onMounted(() => {
  initSampleData(machineStore, faqStore)
})

function clearHistory() {
  faqStore.viewHistory.splice(0)
  try { localStorage.removeItem('faq-history') } catch {}
}

const currentTime = ref(new Date().toLocaleString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }))

const stats = computed(() => [
  { label: 'FAQ 总数', value: faqStore.faqCount, color: '#1a73e8', icon: 'Document', action: () => router.push('/faq') },
  { label: '机型总数', value: machineStore.machineCount, color: '#67c23a', icon: 'Monitor', action: () => router.push('/machines') },
  { label: '产品分类', value: machineStore.categoryCount, color: '#e6a23c', icon: 'Folder', action: () => router.push('/categories') },
  { label: '我的收藏', value: faqStore.favoriteCount, color: '#f56c6c', icon: 'Star', action: () => router.push('/favorites') }
])
</script>

<style scoped>
.welcome-banner {
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
  border-radius: 16px; padding: 28px 32px;
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 20px; color: #fff;
}
.welcome-text h2 { font-size: 22px; font-weight: 800; margin-bottom: 4px; }
.welcome-text p { font-size: 14px; color: rgba(255,255,255,0.7); }
.welcome-actions { display: flex; gap: 12px; }

.mb-16 { margin-bottom: 16px; }
.stat-row { margin-bottom: 20px; }
.stat-icon-wrap { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 12px; }

.quick-actions { display: flex; gap: 12px; flex-wrap: wrap; }
.quick-action-item {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 20px; border-radius: 12px; cursor: pointer;
  background: #f8fafc; border: 1px solid #f0f0f0;
  transition: all 0.2s; font-size: 14px; font-weight: 500;
}
.quick-action-item:hover { background: #e8f0fe; border-color: #c2d9f7; transform: translateY(-1px); }

.faq-link { color: #1a73e8; text-decoration: none; font-weight: 500; }
.faq-link:hover { text-decoration: underline; }

.category-list { display: flex; flex-direction: column; gap: 8px; }
.category-item { display: flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 10px; cursor: pointer; transition: background 0.2s; }
.category-item:hover { background: #f5f7fa; }
.category-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.category-name { flex: 1; font-size: 13px; font-weight: 500; }

.history-list { display: flex; flex-direction: column; gap: 6px; }
.history-item { display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; border-radius: 8px; cursor: pointer; font-size: 13px; transition: background 0.2s; }
.history-item:hover { background: #f5f7fa; }
.history-title { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 500; }
.history-time { color: #909399; font-size: 12px; flex-shrink: 0; margin-left: 8px; }

.tag-cloud { display: flex; flex-wrap: wrap; gap: 8px; }
.tag-item { transition: transform 0.2s; padding: 6px 12px !important; font-size: 13px !important; }
.tag-item:hover { transform: scale(1.05); }

@media (max-width: 768px) {
  .welcome-banner { flex-direction: column; gap: 16px; text-align: center; padding: 20px; }
  .welcome-actions { justify-content: center; }
}
</style>
