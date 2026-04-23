<template>
  <div class="tag-detail" v-if="tag">
    <div class="detail-header">
      <el-button text @click="$router.push('/tags')"><el-icon><ArrowLeft /></el-icon> 返回标签管理</el-button>
    </div>

    <el-card shadow="never" class="tag-info-card">
      <div class="tag-header">
        <el-tag :color="tag.color" effect="dark" size="large" style="border:none;font-size:18px;padding:8px 20px">{{ tag.name }}</el-tag>
        <el-statistic title="关联 FAQ 数" :value="relatedFaqs.length" style="margin-left:auto" />
      </div>
    </el-card>

    <el-card shadow="never" style="margin-top:16px">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-weight:600">关联 FAQ（{{ filteredFaqs.length }} 条）</span>
          <el-input v-model="searchText" placeholder="搜索..." :prefix-icon="Search" clearable style="width:200px" size="small" />
        </div>
      </template>
      <div class="faq-list" v-if="filteredFaqs.length">
        <div class="faq-item" v-for="faq in filteredFaqs" :key="faq.id" @click="$router.push(`/faq/${faq.id}`)">
          <div style="display:flex;align-items:center;gap:8px">
            <el-tag size="small" :color="getPriorityColor(faq.priority)" effect="dark" style="border:none">{{ getPriorityText(faq.priority) }}</el-tag>
            <span class="faq-title">{{ faq.title }}</span>
          </div>
          <div class="faq-meta">
            <el-tag size="small" type="info">{{ machineStore.getMachine(faq.machineId)?.name || '-' }}</el-tag>
            <span><el-icon><View /></el-icon> {{ faq.viewCount || 0 }}</span>
          </div>
        </div>
      </div>
      <el-empty v-else description="暂无关联 FAQ" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, Search, View } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { getPriorityColor, getPriorityText } from '../utils'

const route = useRoute()
const faqStore = useFaqStore()
const machineStore = useMachineStore()
const searchText = ref('')

const tag = computed(() => faqStore.getTag(route.params.id))
const relatedFaqs = computed(() => faqStore.faqs.filter(f => f.tags && f.tags.includes(route.params.id)).sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt)))
const filteredFaqs = computed(() => {
  if (!searchText.value.trim()) return relatedFaqs.value
  const q = searchText.value.toLowerCase()
  return relatedFaqs.value.filter(f => f.title.toLowerCase().includes(q) || (f.summary || '').toLowerCase().includes(q))
})
</script>

<style scoped>
.tag-detail { max-width: 1000px; margin: 0 auto; }
.detail-header { margin-bottom: 16px; }
.tag-header { display: flex; align-items: center; }
.tag-info-card { margin-bottom: 16px; }
.faq-list { display: flex; flex-direction: column; gap: 8px; }
.faq-item { padding: 14px 16px; border: 1px solid #e5e6eb; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
.faq-item:hover { border-color: #409eff; background: #f0f7ff; }
.faq-title { font-size: 14px; font-weight: 600; }
.faq-meta { display: flex; align-items: center; gap: 12px; margin-top: 6px; font-size: 12px; color: #86909c; }
</style>
