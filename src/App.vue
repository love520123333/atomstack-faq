<template>
  <!-- 管理后台布局 -->
  <div class="app-wrapper" v-if="isHelpRoute === false">
    <div class="sidebar" :class="{ 'is-collapsed': collapsed }">
      <div class="sidebar-header">
        <div class="logo" v-show="!collapsed">
          <span class="logo-icon">A</span>
          <span class="logo-text">AtomStack FAQ</span>
        </div>
        <div class="logo-collapsed" v-show="collapsed"><span class="logo-icon">A</span></div>
        <div class="collapse-btn" @click="collapsed = !collapsed">
          <el-icon :size="16"><DArrowLeft v-if="!collapsed" /><DArrowRight v-else /></el-icon>
        </div>
      </div>
      <el-menu :default-active="route.path" :collapse="collapsed" :router="true" class="sidebar-menu">
        <el-menu-item index="/"><el-icon><HomeFilled /></el-icon><template #title>首页仪表盘</template></el-menu-item>
        <el-menu-item index="/machines"><el-icon><Monitor /></el-icon><template #title>机型管理</template></el-menu-item>
        <el-menu-item index="/faq"><el-icon><Document /></el-icon><template #title>FAQ 列表</template></el-menu-item>
        <el-menu-item index="/search"><el-icon><Search /></el-icon><template #title>高级搜索</template></el-menu-item>
        <el-menu-item index="/favorites"><el-icon><Star /></el-icon><template #title>我的收藏</template></el-menu-item>
        <el-menu-item index="/categories"><el-icon><Folder /></el-icon><template #title>分类管理</template></el-menu-item>
        <el-menu-item index="/tags"><el-icon><PriceTag /></el-icon><template #title>标签管理</template></el-menu-item>
        <el-menu-item index="/statistics"><el-icon><DataAnalysis /></el-icon><template #title>数据统计</template></el-menu-item>
      </el-menu>
      <div class="sidebar-footer" v-show="!collapsed">
        <el-button text size="small" style="color:rgba(255,255,255,0.5);padding:0" @click="$router.push('/help')">
          <el-icon><View /></el-icon> 帮助中心入口
        </el-button>
        <span style="font-size:11px;color:rgba(255,255,255,0.3)">© AtomStack 2026</span>
      </div>
    </div>
    <div class="main-container">
      <div class="header">
        <div class="header-left">
          <el-breadcrumb separator="/"><el-breadcrumb-item :to="{path:'/'}">首页</el-breadcrumb-item><el-breadcrumb-item v-if="route.meta.title">{{ route.meta.title }}</el-breadcrumb-item></el-breadcrumb>
        </div>
        <div class="header-right">
          <el-input v-model="globalSearch" placeholder="搜索FAQ..." :prefix-icon="Search" clearable class="global-search" @keyup.enter="doSearch" />
          <el-tooltip content="导入数据"><el-button :icon="Upload" circle size="small" @click="showImport=true" /></el-tooltip>
          <el-tooltip content="导出全部"><el-button :icon="Download" circle size="small" @click="exportAll" /></el-tooltip>
          <el-tooltip content="一键清空数据"><el-button :icon="Delete" circle size="small" type="danger" @click="clearAll" /></el-tooltip>
        </div>
      </div>
      <div class="main-content">
        <router-view />
      </div>
    </div>

    <el-dialog v-model="showImport" title="导入数据" width="500px">
      <el-alert type="info" :closable="false" show-icon style="margin-bottom:16px">选择之前导出的 JSON 文件。导入会与现有数据合并（按ID去重）。</el-alert>
      <el-upload :auto-upload="false" :limit="1" accept=".json" :on-change="f => importFile=f.raw" drag>
        <el-icon :size="40"><UploadFilled /></el-icon>
        <div style="margin-top:8px">拖入 JSON 文件或 <em>点击上传</em></div>
      </el-upload>
      <template #footer><el-button @click="showImport=false;importFile=null">取消</el-button><el-button type="primary" :disabled="!importFile" @click="doImport">确认导入</el-button></template>
    </el-dialog>
  </div>

  <!-- 客户端布局（帮助中心公开页面）-->
  <router-view v-else />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { HomeFilled, Monitor, Document, Search, Star, Folder, PriceTag, DataAnalysis, Upload, Download, Delete, DArrowLeft, DArrowRight, UploadFilled, View } from '@element-plus/icons-vue'
import { useFaqStore } from './stores/faq'
import { useMachineStore } from './stores/machine'
import { initSampleData } from './data/sampleData'

const router = useRouter()
const route = useRoute()
const faqStore = useFaqStore()
const machineStore = useMachineStore()
const collapsed = ref(false)
const globalSearch = ref('')
const showImport = ref(false)
const importFile = ref(null)

// 应用启动时初始化数据（只执行一次，main.js 中也会执行）
onMounted(() => {
  initSampleData(machineStore, faqStore)
})

// 判断是否为帮助中心路由
const isHelpRoute = computed(() => {
  return route.path.startsWith('/help')
})

function doSearch() {
  if (!globalSearch.value.trim()) return
  router.push({ path: '/search', query: { q: globalSearch.value.trim() } })
}

function doImport() {
  if (!importFile.value) return
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const d = JSON.parse(e.target.result)
      let c = 0
      if (d.machines) { d.machines.forEach(m => machineStore.addMachine(m, true)); c += d.machines.length }
      if (d.categories) { d.categories.forEach(cat => machineStore.addCategory(cat, true)) }
      if (d.tags) { d.tags.forEach(t => faqStore.addTag(t, true)) }
      if (d.faqs) { d.faqs.forEach(f => faqStore.addFaq(f, true)); c += d.faqs.length }
      // 批量更新后才计算标签使用计数，避免每条 FAQ 都触发一次
      faqStore.batchUpdateTagUsage()
      // 持久化机型和机器数据
      if (d.machines) { try { localStorage.setItem('faq-machines', JSON.stringify(machineStore.machines)) } catch {} }
      if (d.faqs) { try { localStorage.setItem('faq-list', JSON.stringify(faqStore.faqs)) } catch {} }
      ElMessage.success(`导入 ${c} 条数据`)
      showImport.value = false; importFile.value = null
    } catch { ElMessage.error('JSON 格式错误') }
  }
  reader.readAsText(importFile.value)
}

function exportAll() {
  const data = { exportTime: new Date().toISOString(), version: '1.0', machines: machineStore.machines, faqs: faqStore.faqs, categories: machineStore.categories, tags: faqStore.tags }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `atomstack-faq-${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  ElMessage.success('导出成功')
}

async function clearAll() {
  await ElMessageBox.confirm('确定要清空所有数据？此操作不可恢复！', '危险操作', { type: 'warning', confirmButtonText: '确认清空', cancelButtonText: '取消' })
  localStorage.removeItem('faq-list')
  localStorage.removeItem('faq-machines')
  localStorage.removeItem('faq-categories')
  localStorage.removeItem('faq-tags')
  localStorage.removeItem('faq-favorites')
  localStorage.removeItem('faq-history')
  localStorage.removeItem('faq-data-version')
  location.reload()
}
</script>

<style scoped>
.app-wrapper { display: flex; height: 100vh; background: #f0f2f5; }
.sidebar {
  width: 220px; height: 100vh; background: linear-gradient(180deg, #0d1b2a 0%, #1b2838 50%, #0d1b2a 100%);
  transition: width 0.3s; display: flex; flex-direction: column; overflow: hidden; flex-shrink: 0;
  box-shadow: 2px 0 12px rgba(0,0,0,0.2);
}
.sidebar.is-collapsed { width: 64px; }
.sidebar-header { display: flex; align-items: center; justify-content: space-between; padding: 16px; border-bottom: 1px solid rgba(255,255,255,0.08); min-height: 60px; }
.logo { display: flex; align-items: center; gap: 10px; color: #fff; font-size: 15px; font-weight: 700; white-space: nowrap; }
.logo-icon { width: 32px; height: 32px; background: linear-gradient(135deg, #409eff, #67c23a); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 900; color: #fff; flex-shrink: 0; }
.logo-collapsed { display: flex; justify-content: center; }
.collapse-btn { cursor: pointer; color: rgba(255,255,255,0.5); transition: color 0.2s; flex-shrink: 0; }
.collapse-btn:hover { color: #fff; }
.sidebar-menu { border-right: none; background: transparent; flex: 1; padding-top: 8px; }
.sidebar-menu .el-menu-item { color: rgba(255,255,255,0.65); height: 48px; line-height: 48px; margin: 2px 8px; border-radius: 8px; }
.sidebar-menu .el-menu-item:hover { background: rgba(255,255,255,0.08); color: #fff; }
.sidebar-menu .el-menu-item.is-active { background: rgba(64,158,255,0.2); color: #409eff; }
.sidebar-footer { padding: 12px 16px; border-top: 1px solid rgba(255,255,255,0.06); text-align: center; display: flex; flex-direction: column; gap: 4px; }
.main-container { flex: 1; display: flex; flex-direction: column; overflow: hidden; min-width: 0; }
.header { display: flex; align-items: center; justify-content: space-between; padding: 12px 24px; background: #fff; border-bottom: 1px solid #e4e7ed; box-shadow: 0 1px 4px rgba(0,0,0,0.04); z-index: 10; }
.header-right { display: flex; align-items: center; gap: 10px; }
.global-search { width: 260px; }
.main-content { flex: 1; overflow-y: auto; padding: 20px 24px; }
@media (max-width: 768px) {
  .sidebar { position: fixed; z-index: 100; }
  .sidebar.is-collapsed { width: 0; }
  .global-search { width: 140px; }
}
</style>
