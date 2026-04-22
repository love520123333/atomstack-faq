<template>
  <div class="page-container">
    <div class="page-title"><el-icon><Star /></el-icon> 我的收藏 <el-tag>{{ faqStore.favoriteFaqs.length }}</el-tag></div>

    <el-empty v-if="!faqStore.favoriteFaqs.length" description="暂无收藏，浏览 FAQ 时点击收藏按钮即可添加">
      <el-button type="primary" @click="$router.push('/faq')">去浏览 FAQ</el-button>
    </el-empty>

    <el-row :gutter="16" v-else>
      <el-col :xs="24" :sm="12" :lg="8" v-for="item in faqStore.favoriteFaqs" :key="item.id">
        <el-card shadow="hover" class="fav-card">
          <div class="fav-header">
            <el-tag size="small" :color="getPriorityColor(item.priority)" effect="dark" style="border:none">{{ getPriorityText(item.priority) }}</el-tag>
            <el-button :icon="StarFilled" type="warning" size="small" circle @click.stop="faqStore.toggleFavorite(item.id)" />
          </div>
          <h3 class="fav-title" @click="$router.push(`/faq/${item.id}`)">{{ item.title }}</h3>
          <p class="fav-machine">{{ machineStore.getMachine(item.machineId)?.name || '未知机型' }}</p>
          <p class="fav-summary">{{ truncate(item.summary || item.solution, 80) }}</p>
          <div class="fav-footer">
            <span>{{ formatDate(item.updatedAt) }}</span>
            <span>浏览 {{ item.viewCount || 0 }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { Star, StarFilled } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { formatDate, getPriorityColor, getPriorityText, truncate } from '../utils'

const faqStore = useFaqStore()
const machineStore = useMachineStore()
</script>

<style scoped>
.fav-card { margin-bottom: 16px; transition: transform 0.2s; }
.fav-card:hover { transform: translateY(-2px); }
.fav-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.fav-title { font-size: 15px; font-weight: 600; cursor: pointer; margin: 4px 0; }
.fav-title:hover { color: #409eff; }
.fav-machine { font-size: 12px; color: #909399; }
.fav-summary { font-size: 13px; color: #606266; margin: 8px 0; }
.fav-footer { display: flex; justify-content: space-between; font-size: 12px; color: #909399; }
</style>
