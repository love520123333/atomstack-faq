<template>
  <div class="help-center">
    <!-- 顶部导航栏 -->
    <header class="hc-header">
      <div class="hc-header-inner">
        <div class="hc-logo" @click="$router.push('/')">
          <div class="hc-logo-icon">A</div>
          <span class="hc-logo-text">AtomStack</span>
          <span class="hc-logo-sub">帮助中心</span>
        </div>
        <div class="hc-nav">
          <a class="hc-nav-link" href="javascript:void(0)" @click="scrollTo('products')">产品中心</a>
          <a class="hc-nav-link" href="javascript:void(0)" @click="scrollTo('faq')">常见问题</a>
          <a class="hc-nav-link" href="javascript:void(0)" @click="scrollTo('contact')">联系我们</a>
        </div>
        <div class="hc-search-box">
          <el-input v-model="searchQuery" placeholder="搜索问题和解决方案..." :prefix-icon="Search" clearable size="large" @keyup.enter="doSearch" />
        </div>
      </div>
    </header>

    <!-- Hero Banner -->
    <section class="hc-hero">
      <div class="hc-hero-inner">
        <h1 class="hc-hero-title">AtomStack 帮助中心</h1>
        <p class="hc-hero-subtitle">找到您需要的答案，快速解决激光雕刻机使用问题</p>
        <div class="hc-hero-search">
          <el-input v-model="heroSearch" placeholder="输入您遇到的问题，例如：激光不亮、无法连接..." :prefix-icon="Search" clearable size="large" class="hero-input" @keyup.enter="doHeroSearch" />
          <el-button type="primary" size="large" @click="doHeroSearch">搜索</el-button>
        </div>
        <div class="hc-hero-tags">
          <span class="hc-hero-tag" v-for="tag in hotTags" :key="tag.id" @click="$router.push({ path: '/help/search', query: { tag: tag.id } })">
            {{ tag.name }}
          </span>
        </div>
      </div>
    </section>

    <!-- 快速统计 -->
    <section class="hc-stats">
      <div class="hc-stats-inner">
        <div class="hc-stat-item">
          <div class="hc-stat-num">{{ faqStore.faqCount }}+</div>
          <div class="hc-stat-label">解决方案</div>
        </div>
        <div class="hc-stat-item">
          <div class="hc-stat-num">{{ machineStore.machineCount }}</div>
          <div class="hc-stat-label">产品型号</div>
        </div>
        <div class="hc-stat-item">
          <div class="hc-stat-num">{{ machineStore.categoryCount }}</div>
          <div class="hc-stat-label">产品分类</div>
        </div>
        <div class="hc-stat-item">
          <div class="hc-stat-num">24h</div>
          <div class="hc-stat-label">快速响应</div>
        </div>
      </div>
    </section>

    <!-- 产品中心 -->
    <section class="hc-section" id="products">
      <div class="hc-section-inner">
        <h2 class="hc-section-title">
          <span class="hc-title-icon">📦</span> 产品中心
          <span class="hc-section-desc">选择您的产品，查找专属解决方案</span>
        </h2>
        <!-- 分类 Tab -->
        <div class="hc-category-tabs">
          <div class="hc-cat-tab" :class="{ active: activeCategory === '' }" @click="activeCategory = ''">全部产品</div>
          <div class="hc-cat-tab" :class="{ active: activeCategory === cat.id }" v-for="cat in machineStore.categories" :key="cat.id" @click="activeCategory = cat.id">
            <span class="hc-cat-dot" :style="{ background: cat.color }"></span>
            {{ cat.name }}
          </div>
        </div>
        <!-- 产品卡片 -->
        <div class="hc-product-grid">
          <div class="hc-product-card" v-for="m in filteredMachines" :key="m.id" @click="$router.push(`/help/machines/${m.id}`)">
            <div class="hc-product-img">
              <img v-if="!imgFailed[m.id]" :src="m.image" :alt="m.name" loading="lazy" @error="imgFailed[m.id]=true" />
              <div v-if="!m.image || imgFailed[m.id]" class="hc-product-placeholder">
                <span class="hc-placeholder-letter">{{ m.name.charAt(0) }}</span>
                <span class="hc-placeholder-name">{{ m.name }}</span>
              </div>
            </div>
            <div class="hc-product-info">
              <el-tag size="small" :color="machineStore.getCategory(m.categoryId)?.color" effect="dark" style="border:none;margin-bottom:6px">
                {{ machineStore.getCategoryName(m.categoryId) }}
              </el-tag>
              <h3 class="hc-product-name">{{ m.name }}</h3>
              <p class="hc-product-desc">{{ (m.description || '').substring(0, 60) }}{{ (m.description || '').length > 60 ? '...' : '' }}</p>
              <div class="hc-product-footer">
                <span class="hc-product-faq-count">{{ faqStore.getFaqsByMachine(m.id).length }} 条 FAQ</span>
                <span class="hc-product-arrow">查看详情 →</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 常见问题 -->
    <section class="hc-section hc-section-gray" id="faq">
      <div class="hc-section-inner">
        <h2 class="hc-section-title">
          <span class="hc-title-icon">🔥</span> 热门问题
          <span class="hc-section-desc">用户最常遇到的问题和解决方案</span>
        </h2>
        <!-- 分类 FAQ 切换 -->
        <div class="hc-faq-categories">
          <div class="hc-faq-cat-btn" :class="{ active: faqCategory === '' }" @click="faqCategory = ''">全部</div>
          <div class="hc-faq-cat-btn" :class="{ active: faqCategory === cat.id }" v-for="cat in machineStore.categories" :key="cat.id" @click="faqCategory = faqCategory === cat.id ? '' : cat.id">
            {{ cat.name }}
          </div>
        </div>
        <!-- FAQ 列表 -->
        <div class="hc-faq-list">
          <div class="hc-faq-item" v-for="faq in displayFaqs" :key="faq.id" @click="$router.push(`/help/faq/${faq.id}`)">
            <div class="hc-faq-item-header">
              <el-tag size="small" :color="getPriorityColor(faq.priority)" effect="dark" style="border:none">
                {{ getPriorityText(faq.priority) }}
              </el-tag>
              <span class="hc-faq-item-title">{{ faq.title }}</span>
              <el-icon class="hc-faq-arrow"><ArrowRight /></el-icon>
            </div>
            <div class="hc-faq-item-meta">
              <span>{{ machineStore.getMachine(faq.machineId)?.name || '' }}</span>
              <span>
                <el-icon><View /></el-icon> {{ faq.viewCount || 0 }}
              </span>
              <span>
                <el-icon><Top /></el-icon> {{ faq.helpfulCount || 0 }}
              </span>
            </div>
          </div>
        </div>
        <div class="hc-faq-more">
          <el-button type="primary" size="large" @click="$router.push('/help/search')">
            查看全部 {{ faqStore.faqCount }} 条 FAQ →
          </el-button>
        </div>
      </div>
    </section>

    <!-- 产品分类概览 -->
    <section class="hc-section">
      <div class="hc-section-inner">
        <h2 class="hc-section-title">
          <span class="hc-title-icon">📂</span> 产品分类
          <span class="hc-section-desc">浏览所有产品系列</span>
        </h2>
        <div class="hc-category-grid">
          <div class="hc-category-card" v-for="cat in machineStore.categories" :key="cat.id" @click="activeCategory = cat.id; scrollTo('products')">
            <div class="hc-category-icon" :style="{ background: cat.color + '15' }">
              <span :style="{ color: cat.color, fontSize: '24px' }">{{ getCategoryEmoji(cat.id) }}</span>
            </div>
            <h3 class="hc-category-name">{{ cat.name }}</h3>
            <p class="hc-category-desc">{{ cat.description || '' }}</p>
            <div class="hc-category-count">
              {{ machineStore.machines.filter(m => m.categoryId === cat.id).length }} 个产品 · 
              {{ faqStore.getFaqsByCategory(cat.id, machineStore).length }} 条 FAQ
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 联系我们 -->
    <section class="hc-section hc-section-dark" id="contact">
      <div class="hc-section-inner hc-contact">
        <h2 class="hc-section-title" style="color:#fff">
          <span class="hc-title-icon">💬</span> 没有找到答案？
        </h2>
        <p class="hc-contact-desc">如果以上内容未能解决您的问题，欢迎通过以下方式联系我们的技术支持团队</p>
        <div class="hc-contact-methods">
          <div class="hc-contact-card">
            <el-icon :size="32" color="#409eff"><Message /></el-icon>
            <h4>在线客服</h4>
            <p>工作日 9:00-18:00</p>
          </div>
          <div class="hc-contact-card">
            <el-icon :size="32" color="#67c23a"><Promotion /></el-icon>
            <h4>发送邮件</h4>
            <p>support@atomstack.com</p>
          </div>
          <div class="hc-contact-card">
            <el-icon :size="32" color="#e6a23c"><Phone /></el-icon>
            <h4>电话支持</h4>
            <p>400-xxx-xxxx</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="hc-footer">
      <div class="hc-footer-inner">
        <div class="hc-footer-logo">
          <div class="hc-logo-icon">A</div>
          <span class="hc-logo-text">AtomStack</span>
        </div>
        <p class="hc-footer-text">© 2026 AtomStack. All rights reserved.</p>
        <div class="hc-footer-links">
          <router-link to="/">管理后台</router-link>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Monitor, ArrowRight, View, Top, Message, Promotion, Phone } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { getPriorityColor, getPriorityText } from '../utils'
import { initSampleData } from '../data/sampleData'

const router = useRouter()
const faqStore = useFaqStore()
const machineStore = useMachineStore()

onMounted(() => {
  initSampleData(machineStore, faqStore)
})

const searchQuery = ref('')
const heroSearch = ref('')
const activeCategory = ref('')
const faqCategory = ref('')
const imgFailed = reactive({})

const hotTags = computed(() => [...faqStore.tags].sort((a, b) => b.usageCount - a.usageCount).slice(0, 8))

const filteredMachines = computed(() => {
  let list = machineStore.machines
  if (activeCategory.value) list = list.filter(m => m.categoryId === activeCategory.value)
  return list
})

const categoryFaqs = computed(() => {
  if (!faqCategory.value) return faqStore.popularFaqs.slice(0, 12)
  return faqStore.getFaqsByCategory(faqCategory.value, machineStore)
    .sort((a, b) => (b.viewCount || 0) - (a.viewCount || 0))
    .slice(0, 12)
})

const displayFaqs = computed(() => categoryFaqs.value)

function doSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/help/search', query: { q: searchQuery.value.trim() } })
  }
}

function doHeroSearch() {
  if (heroSearch.value.trim()) {
    router.push({ path: '/help/search', query: { q: heroSearch.value.trim() } })
  }
}

function getCategoryEmoji(catId) {
  const map = {
    'cat-1': '🔹', 'cat-2': '⚡', 'cat-3': '✨', 'cat-4': '🔧',
    'cat-5': '🔥', 'cat-6': '🧩', 'cat-7': '🛡️'
  }
  return map[catId] || '📦'
}

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) {
    const top = el.getBoundingClientRect().top + window.scrollY - 80
    window.scrollTo({ top, behavior: 'smooth' })
  }
}
</script>

<style scoped>
/* Header */
.hc-header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  background: rgba(255,255,255,0.95); backdrop-filter: blur(12px);
  border-bottom: 1px solid #f0f0f0;
  transition: box-shadow 0.3s;
}
.hc-header-inner {
  max-width: 1200px; margin: 0 auto; padding: 0 24px;
  display: flex; align-items: center; height: 64px; gap: 32px;
}
.hc-logo { display: flex; align-items: center; gap: 10px; cursor: pointer; flex-shrink: 0; }
.hc-logo-icon {
  width: 36px; height: 36px; border-radius: 10px;
  background: linear-gradient(135deg, #1a73e8, #0d47a1);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 900; color: #fff;
}
.hc-logo-text { font-size: 18px; font-weight: 800; color: #1a1a2e; letter-spacing: -0.5px; }
.hc-logo-sub { font-size: 13px; color: #666; margin-left: 4px; }
.hc-nav { display: flex; gap: 24px; flex-shrink: 0; }
.hc-nav-link { font-size: 14px; color: #555; text-decoration: none; font-weight: 500; transition: color 0.2s; }
.hc-nav-link:hover { color: #1a73e8; }
.hc-search-box { flex: 1; max-width: 320px; }
.hc-search-box :deep(.el-input__wrapper) { border-radius: 20px; }

/* Hero */
.hc-hero {
  padding: 140px 24px 60px;
  background: linear-gradient(135deg, #0d1b2a 0%, #1a3a5c 40%, #1a73e8 100%);
  text-align: center; color: #fff;
}
.hc-hero-inner { max-width: 720px; margin: 0 auto; }
.hc-hero-title { font-size: 42px; font-weight: 900; margin-bottom: 12px; letter-spacing: -1px; }
.hc-hero-subtitle { font-size: 18px; color: rgba(255,255,255,0.7); margin-bottom: 32px; }
.hc-hero-search { display: flex; gap: 12px; max-width: 600px; margin: 0 auto 24px; }
.hero-input { flex: 1; }
.hero-input :deep(.el-input__wrapper) { border-radius: 12px; padding: 4px 16px; }
.hero-input :deep(.el-input__inner) { height: 22px; }
.hc-hero-tags { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; }
.hc-hero-tag {
  padding: 6px 16px; border-radius: 20px; font-size: 13px;
  background: rgba(255,255,255,0.12); color: rgba(255,255,255,0.85);
  cursor: pointer; transition: all 0.2s;
}
.hc-hero-tag:hover { background: rgba(255,255,255,0.25); color: #fff; }

/* Stats */
.hc-stats {
  background: #fff; padding: 32px 24px;
  border-bottom: 1px solid #f0f0f0;
  margin-top: -24px; position: relative; z-index: 10;
}
.hc-stats-inner {
  max-width: 800px; margin: 0 auto;
  display: flex; justify-content: space-around;
}
.hc-stat-item { text-align: center; }
.hc-stat-num { font-size: 32px; font-weight: 900; color: #1a73e8; }
.hc-stat-label { font-size: 13px; color: #999; margin-top: 4px; }

/* Sections */
.hc-section { padding: 60px 24px; }
.hc-section-gray { background: #f8fafc; }
.hc-section-dark { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
.hc-section-inner { max-width: 1200px; margin: 0 auto; }
.hc-section-title {
  font-size: 28px; font-weight: 800; color: #1a1a2e; margin-bottom: 8px;
  display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
}
.hc-title-icon { font-size: 28px; }
.hc-section-desc {
  font-size: 15px; color: #999; font-weight: 400; display: block;
  width: 100%; margin-bottom: 28px;
}

/* Category Tabs */
.hc-category-tabs {
  display: flex; gap: 8px; margin-bottom: 28px; overflow-x: auto;
  padding-bottom: 8px; flex-wrap: wrap;
}
.hc-cat-tab {
  padding: 8px 18px; border-radius: 20px; font-size: 13px; font-weight: 500;
  background: #f0f2f5; color: #666; cursor: pointer; transition: all 0.2s;
  white-space: nowrap; display: flex; align-items: center; gap: 6px;
  border: 1px solid transparent;
}
.hc-cat-tab:hover { background: #e8f0fe; color: #1a73e8; }
.hc-cat-tab.active { background: #1a73e8; color: #fff; border-color: #1a73e8; }
.hc-cat-dot { width: 8px; height: 8px; border-radius: 50%; }

/* Product Grid */
.hc-product-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}
.hc-product-card {
  background: #fff; border-radius: 16px; overflow: hidden;
  border: 1px solid #f0f0f0; cursor: pointer;
  transition: all 0.3s; position: relative;
}
.hc-product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.08);
  border-color: transparent;
}
.hc-product-img {
  height: 180px; background: linear-gradient(135deg, #f5f7fa, #e8ecf1);
  display: flex; align-items: center; justify-content: center; overflow: hidden;
}
.hc-product-img img { max-width: 100%; max-height: 180px; object-fit: contain; transition: transform 0.3s; }
.hc-product-card:hover .hc-product-img img { transform: scale(1.05); }
.hc-product-placeholder {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  color: #86909c; text-align: center; width: 100%; height: 100%;
  background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
}
.hc-placeholder-letter { font-size: 36px; font-weight: 900; text-shadow: 0 2px 8px rgba(0,0,0,0.15); color: rgba(255,255,255,0.9); }
.hc-placeholder-name { font-size: 11px; opacity: 0.7; margin-top: 4px; color: rgba(255,255,255,0.8); }
.hc-product-info { padding: 16px; }
.hc-product-name { font-size: 16px; font-weight: 700; color: #1a1a2e; margin: 0 0 4px; }
.hc-product-desc { font-size: 12px; color: #999; margin: 0 0 12px; line-height: 1.5; }
.hc-product-footer { display: flex; justify-content: space-between; align-items: center; }
.hc-product-faq-count { font-size: 12px; color: #1a73e8; font-weight: 600; }
.hc-product-arrow { font-size: 12px; color: #ccc; transition: all 0.2s; }
.hc-product-card:hover .hc-product-arrow { color: #1a73e8; }

/* FAQ List */
.hc-faq-categories {
  display: flex; gap: 8px; margin-bottom: 20px; overflow-x: auto;
  padding-bottom: 8px; flex-wrap: wrap;
}
.hc-faq-cat-btn {
  padding: 6px 16px; border-radius: 20px; font-size: 13px;
  background: #f0f2f5; color: #666; cursor: pointer; transition: all 0.2s;
  white-space: nowrap; border: 1px solid transparent;
}
.hc-faq-cat-btn:hover { background: #e8f0fe; color: #1a73e8; }
.hc-faq-cat-btn.active { background: #1a73e8; color: #fff; border-color: #1a73e8; }
.hc-faq-list { display: flex; flex-direction: column; gap: 8px; }
.hc-faq-item {
  padding: 16px 20px; background: #fff; border: 1px solid #f0f0f0;
  border-radius: 12px; cursor: pointer; transition: all 0.2s;
}
.hc-faq-item:hover { border-color: #1a73e8; background: #f8fbff; box-shadow: 0 4px 12px rgba(26,115,232,0.06); }
.hc-faq-item-header { display: flex; align-items: center; gap: 10px; }
.hc-faq-item-title { font-size: 15px; font-weight: 600; color: #1a1a2e; flex: 1; }
.hc-faq-arrow { color: #ccc; transition: all 0.2s; }
.hc-faq-item:hover .hc-faq-arrow { color: #1a73e8; transform: translateX(4px); }
.hc-faq-item-meta { display: flex; gap: 16px; font-size: 12px; color: #bbb; margin-top: 8px; padding-left: 66px; }
.hc-faq-item-meta span { display: flex; align-items: center; gap: 3px; }
.hc-faq-more { text-align: center; margin-top: 28px; }

/* Category Grid */
.hc-category-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;
}
.hc-category-card {
  padding: 24px; background: #fff; border: 1px solid #f0f0f0;
  border-radius: 16px; cursor: pointer; transition: all 0.3s;
}
.hc-category-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.06); border-color: transparent; }
.hc-category-icon { width: 56px; height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin-bottom: 14px; }
.hc-category-name { font-size: 17px; font-weight: 700; color: #1a1a2e; margin: 0 0 6px; }
.hc-category-desc { font-size: 13px; color: #999; margin: 0 0 12px; line-height: 1.5; }
.hc-category-count { font-size: 12px; color: #bbb; }

/* Contact */
.hc-contact { text-align: center; }
.hc-contact-desc { color: rgba(255,255,255,0.6); font-size: 16px; margin-bottom: 36px; }
.hc-contact-methods { display: flex; justify-content: center; gap: 32px; flex-wrap: wrap; }
.hc-contact-card {
  padding: 28px 32px; border-radius: 16px; text-align: center;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
  min-width: 180px; transition: all 0.3s;
}
.hc-contact-card:hover { background: rgba(255,255,255,0.1); transform: translateY(-2px); }
.hc-contact-card h4 { font-size: 16px; color: #fff; margin: 12px 0 6px; }
.hc-contact-card p { font-size: 13px; color: rgba(255,255,255,0.5); margin: 0; }

/* Footer */
.hc-footer {
  background: #0a0a14; padding: 28px 24px;
}
.hc-footer-inner {
  max-width: 1200px; margin: 0 auto;
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
}
.hc-footer-logo { display: flex; align-items: center; gap: 8px; }
.hc-footer-logo .hc-logo-icon { width: 28px; height: 28px; font-size: 16px; border-radius: 8px; }
.hc-footer-logo .hc-logo-text { color: #fff; font-size: 16px; }
.hc-footer-text { font-size: 12px; color: #666; }
.hc-footer-links { display: flex; gap: 16px; }
.hc-footer-links a { font-size: 12px; color: #888; text-decoration: none; }
.hc-footer-links a:hover { color: #fff; }

/* Responsive */
@media (max-width: 768px) {
  .hc-header-inner { padding: 0 16px; gap: 12px; }
  .hc-nav { display: none; }
  .hc-hero { padding: 120px 16px 48px; }
  .hc-hero-title { font-size: 28px; }
  .hc-hero-search { flex-direction: column; }
  .hc-hero-search .el-button { width: 100%; }
  .hc-stats-inner { flex-wrap: wrap; gap: 16px; }
  .hc-stat-num { font-size: 24px; }
  .hc-section { padding: 40px 16px; }
  .hc-section-title { font-size: 22px; }
  .hc-product-grid { grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
  .hc-category-grid { grid-template-columns: 1fr; }
  .hc-contact-methods { flex-direction: column; align-items: center; }
  .hc-footer-inner { flex-direction: column; text-align: center; }
  .hc-faq-item-meta { padding-left: 0; }
}
</style>
