<template>
  <div class="machine-detail" v-if="machine">
    <!-- 顶部导航 -->
    <div class="detail-header">
      <el-button text @click="$router.push('/machines')"><el-icon><ArrowLeft /></el-icon> 返回机型列表</el-button>
      <div style="flex:1"></div>
      <el-button type="primary" :icon="Plus" @click="$router.push(`/faq/create?machine=${machine.id}`)">新建 FAQ</el-button>
    </div>

    <!-- 产品概览区 -->
    <el-row :gutter="24">
      <el-col :xs="24" :lg="10">
        <el-card shadow="never" class="product-card">
          <div class="product-image-wrap">
            <img v-if="machine.image" :src="machine.image" :alt="machine.name" class="product-image" @error="handleImageError" />
            <div v-else class="product-image-placeholder">
              <el-icon :size="64"><Monitor /></el-icon>
              <span>{{ machine.name }}</span>
            </div>
          </div>
          <div class="product-badges">
            <el-tag :color="machineStore.getCategory(machine.categoryId)?.color" effect="dark" size="large" style="border:none">
              {{ machineStore.getCategoryName(machine.categoryId) }}
            </el-tag>
            <el-tag type="success" effect="plain">{{ faqStore.getFaqsByMachine(machine.id).length }} 条 FAQ</el-tag>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="14">
        <el-card shadow="never" class="product-info-card">
          <h1 class="product-title">{{ machine.name }}</h1>
          <p class="product-model" v-if="machine.model">型号: {{ machine.model }}</p>
          <p class="product-desc">{{ machine.description || '暂无描述' }}</p>

          <!-- 核心参数表格 -->
          <div class="specs-section" v-if="machine.specs && Object.keys(machine.specs).length">
            <h3 class="specs-title">📋 产品参数</h3>
            <div class="specs-grid">
              <div class="spec-row" v-for="(value, key) in machine.specs" :key="key">
                <span class="spec-label">{{ key }}</span>
                <span class="spec-value">{{ value }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- FAQ 列表区 -->
    <el-card shadow="never" class="faq-section" style="margin-top:20px">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-weight:700;font-size:16px">📖 全部 FAQ（{{ machineFaqs.length }} 条）</span>
          <el-input v-model="faqSearch" placeholder="搜索 FAQ..." :prefix-icon="Search" clearable style="width:260px" />
        </div>
      </template>

      <!-- FAQ 分类筛选 -->
      <div class="faq-filter-tags" style="margin-bottom:16px">
        <el-check-tag :checked="faqFilter === ''" @change="faqFilter = ''">全部</el-check-tag>
        <el-check-tag v-for="tag in faqStore.tags.filter(t => t.usageCount > 0)" :key="tag.id"
          :checked="faqFilter === tag.id" @change="faqFilter = tag.id">
          {{ tag.name }} ({{ machineFaqs.filter(f => f.tags && f.tags.includes(tag.id)).length }})
        </el-check-tag>
      </div>

      <!-- FAQ 列表 -->
      <div class="faq-list" v-if="filteredFaqs.length">
        <div class="faq-item" v-for="faq in filteredFaqs" :key="faq.id" @click="$router.push(`/faq/${faq.id}`)">
          <div class="faq-item-header">
            <el-tag size="small" :color="getPriorityColor(faq.priority)" effect="dark" style="border:none">
              {{ getPriorityText(faq.priority) }}
            </el-tag>
            <span class="faq-item-title">{{ faq.title }}</span>
            <div style="flex:1"></div>
            <el-icon><ArrowRight /></el-icon>
          </div>
          <p class="faq-item-summary" v-if="faq.summary">{{ truncate(faq.summary, 120) }}</p>
          <div class="faq-item-tags">
            <el-tag v-for="tid in (faq.tags || []).slice(0, 4)" :key="tid" size="small" effect="plain" style="margin-right:4px">
              {{ faqStore.getTagName(tid) }}
            </el-tag>
            <span class="faq-item-meta">
              <el-icon><View /></el-icon> {{ faq.viewCount || 0 }}
              <el-icon style="margin-left:8px"><Top /></el-icon> {{ faq.helpfulCount || 0 }}
            </span>
          </div>
        </div>
      </div>
      <el-empty v-else description="暂无匹配的 FAQ" />
    </el-card>
  </div>

  <!-- 机型不存在 -->
  <div v-else class="not-found">
    <el-empty description="机型不存在">
      <el-button type="primary" @click="$router.push('/machines')">返回机型列表</el-button>
    </el-empty>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, ArrowRight, Plus, Search, Monitor, View, Top } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { getPriorityColor, getPriorityText, truncate } from '../utils'

const route = useRoute()
const faqStore = useFaqStore()
const machineStore = useMachineStore()

const faqSearch = ref('')
const faqFilter = ref('')

const machine = computed(() => {
  const id = route.params.id
  return machineStore.getMachine(id)
})

const machineFaqs = computed(() => {
  if (!machine.value) return []
  return faqStore.getFaqsByMachine(machine.value.id).sort((a, b) => {
    const po = { critical: 0, high: 1, medium: 2, low: 3 }
    return (po[a.priority] || 9) - (po[b.priority] || 9)
  })
})

const filteredFaqs = computed(() => {
  let result = machineFaqs.value
  if (faqFilter.value) {
    result = result.filter(f => f.tags && f.tags.includes(faqFilter.value))
  }
  if (faqSearch.value.trim()) {
    const q = faqSearch.value.toLowerCase()
    result = result.filter(f =>
      f.title.toLowerCase().includes(q) ||
      (f.summary || '').toLowerCase().includes(q) ||
      (f.solution || '').toLowerCase().includes(q) ||
      (f.keywords || '').toLowerCase().includes(q)
    )
  }
  return result
})

function handleImageError(e) {
  e.target.style.display = 'none'
}
</script>

<style scoped>
.machine-detail { max-width: 1200px; margin: 0 auto; }

.detail-header {
  display: flex; align-items: center; margin-bottom: 20px;
}

.product-card { text-align: center; }
.product-image-wrap {
  background: #f8f9fb; border-radius: 12px; padding: 24px; margin-bottom: 16px;
  display: flex; align-items: center; justify-content: center; min-height: 280px;
}
.product-image {
  max-width: 100%; max-height: 320px; object-fit: contain;
  transition: transform 0.3s;
}
.product-image:hover { transform: scale(1.05); }
.product-image-placeholder {
  display: flex; flex-direction: column; align-items: center; gap: 12px; color: #c0c4cc;
}
.product-image-placeholder span { font-size: 18px; font-weight: 600; }
.product-badges { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }

.product-info-card { height: 100%; }
.product-title { font-size: 28px; font-weight: 800; color: #1d2129; margin: 0 0 8px; }
.product-model { color: #86909c; font-size: 14px; margin: 0 0 12px; }
.product-desc { color: #4e5969; font-size: 15px; line-height: 1.7; margin: 0 0 24px; }

.specs-section { border-top: 1px solid #e5e6eb; padding-top: 20px; }
.specs-title { font-size: 16px; font-weight: 700; color: #1d2129; margin: 0 0 16px; }
.specs-grid {
  display: grid; grid-template-columns: 140px 1fr; gap: 8px 16px;
}
.spec-row {
  padding: 8px 0; border-bottom: 1px solid #f2f3f5;
}
.spec-row:nth-child(odd) { background: #fafbfc; border-radius: 4px; }
.spec-label {
  font-size: 13px; color: #86909c; font-weight: 500;
  display: flex; align-items: center;
}
.spec-value {
  font-size: 13px; color: #1d2129; font-weight: 500;
}

.faq-section :deep(.el-card__header) { padding: 16px 20px; }
.faq-filter-tags { display: flex; gap: 8px; flex-wrap: wrap; }
.faq-filter-tags .el-check-tag { border-radius: 16px; }

.faq-list { display: flex; flex-direction: column; gap: 8px; }
.faq-item {
  padding: 16px 20px; border: 1px solid #e5e6eb; border-radius: 10px;
  cursor: pointer; transition: all 0.2s;
}
.faq-item:hover {
  border-color: #409eff; background: #f0f7ff;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.08);
  transform: translateY(-1px);
}
.faq-item-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.faq-item-title { font-size: 15px; font-weight: 600; color: #1d2129; flex: 1; }
.faq-item-summary { font-size: 13px; color: #86909c; line-height: 1.6; margin: 0 0 8px; }
.faq-item-tags { display: flex; align-items: center; flex-wrap: wrap; }
.faq-item-meta { font-size: 12px; color: #c0c4cc; display: flex; align-items: center; gap: 2px; margin-left: auto; }

.not-found { display: flex; justify-content: center; align-items: center; min-height: 400px; }

@media (max-width: 768px) {
  .specs-grid { grid-template-columns: 120px 1fr; }
  .product-title { font-size: 22px; }
}
</style>
