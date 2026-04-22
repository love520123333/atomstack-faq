import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

function genId() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8) }
function load(key, def = []) { try { const d = localStorage.getItem(key); return d ? JSON.parse(d) : def } catch { return def } }
function save(key, data) { try { localStorage.setItem(key, JSON.stringify(data)) } catch { } }

export const useFaqStore = defineStore('faq', () => {
  const faqs = ref(load('faq-list', []))
  const tags = ref(load('faq-tags', [
    { id: 'tag-1', name: '激光不亮', color: '#f56c6c', usageCount: 0 },
    { id: 'tag-2', name: '连接失败', color: '#409eff', usageCount: 0 },
    { id: 'tag-3', name: '雕刻模糊', color: '#e6a23c', usageCount: 0 },
    { id: 'tag-4', name: '切割不透', color: '#67c23a', usageCount: 0 },
    { id: 'tag-5', name: '软件问题', color: '#909399', usageCount: 0 },
    { id: 'tag-6', name: '焦点调节', color: '#b37feb', usageCount: 0 },
    { id: 'tag-7', name: '运动异常', color: '#36cfc9', usageCount: 0 },
    { id: 'tag-8', name: '限位开关', color: '#ff85c0', usageCount: 0 },
    { id: 'tag-9', name: '空气辅助', color: '#ffc53d', usageCount: 0 },
    { id: 'tag-10', name: '安全保护', color: '#ff4d4f', usageCount: 0 },
    { id: 'tag-11', name: '旋转附件', color: '#73d13d', usageCount: 0 },
    { id: 'tag-12', name: '固件升级', color: '#597ef7', usageCount: 0 },
    { id: 'tag-13', name: '材质适配', color: '#9254de', usageCount: 0 },
    { id: 'tag-14', name: '维护保养', color: '#ffa940', usageCount: 0 },
    { id: 'tag-15', name: '配件更换', color: '#ff7a45', usageCount: 0 }
  ]))
  const favorites = ref(load('faq-favorites', []))
  const viewHistory = ref(load('faq-history', []))

  const faqCount = computed(() => faqs.value.length)
  const favoriteCount = computed(() => favorites.value.length)
  const recentFaqs = computed(() => [...faqs.value].sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt)).slice(0, 10))
  const popularFaqs = computed(() => [...faqs.value].sort((a, b) => (b.viewCount || 0) - (a.viewCount || 0)).slice(0, 10))
  const topRatedFaqs = computed(() => [...faqs.value].filter(f => f.rating && f.ratingCount > 0).sort((a, b) => b.rating - a.rating).slice(0, 10))

  function getFaqsByMachine(machineId) { return faqs.value.filter(f => f.machineId === machineId) }
  function getFaqsByCategory(categoryId, machineStore) {
    const mids = machineStore.machines.filter(m => m.categoryId === categoryId).map(m => m.id)
    return faqs.value.filter(f => mids.includes(f.machineId))
  }
  function getFaq(id) { return faqs.value.find(f => f.id === id) }

  function addFaq(faq, skipSave = false) {
    const now = new Date().toISOString()
    const n = { ...faq, id: faq.id || genId(), createdAt: faq.createdAt || now, updatedAt: now, viewCount: faq.viewCount || 0, rating: faq.rating || 0, ratingCount: faq.ratingCount || 0, helpfulCount: faq.helpfulCount || 0 }
    const idx = faqs.value.findIndex(f => f.id === n.id)
    if (idx !== -1) faqs.value[idx] = { ...faqs.value[idx], ...n }
    else faqs.value.push(n)
    updateTagUsage()
    if (!skipSave) save('faq-list', faqs.value)
    return n
  }

  function updateFaq(id, data) {
    const i = faqs.value.findIndex(f => f.id === id)
    if (i !== -1) {
      faqs.value[i] = { ...faqs.value[i], ...data, updatedAt: new Date().toISOString() }
      updateTagUsage(); save('faq-list', faqs.value)
      return faqs.value[i]
    }
    return null
  }

  function deleteFaq(id) {
    const i = faqs.value.findIndex(f => f.id === id)
    if (i !== -1) {
      faqs.value.splice(i, 1)
      favorites.value = favorites.value.filter(fid => fid !== id)
      viewHistory.value = viewHistory.value.filter(h => h.faqId !== id)
      updateTagUsage()
      save('faq-list', faqs.value); save('faq-favorites', favorites.value); save('faq-history', viewHistory.value)
    }
  }

  function recordView(id) {
    const faq = faqs.value.find(f => f.id === id)
    if (faq) { faq.viewCount = (faq.viewCount || 0) + 1; faq.updatedAt = new Date().toISOString(); save('faq-list', faqs.value) }
    const ei = viewHistory.value.findIndex(h => h.faqId === id)
    if (ei !== -1) { viewHistory.value[ei].viewedAt = new Date().toISOString(); viewHistory.value[ei].count = (viewHistory.value[ei].count || 0) + 1 }
    else viewHistory.value.unshift({ faqId: id, viewedAt: new Date().toISOString(), count: 1 })
    if (viewHistory.value.length > 100) viewHistory.value = viewHistory.value.slice(0, 100)
    save('faq-history', viewHistory.value)
  }

  function rateFaq(id, rating) {
    const faq = faqs.value.find(f => f.id === id)
    if (faq) {
      const total = (faq.rating || 0) * (faq.ratingCount || 0) + rating
      faq.ratingCount = (faq.ratingCount || 0) + 1
      faq.rating = Math.round((total / faq.ratingCount) * 10) / 10
      save('faq-list', faqs.value)
    }
  }

  function markHelpful(id) { const faq = faqs.value.find(f => f.id === id); if (faq) { faq.helpfulCount = (faq.helpfulCount || 0) + 1; save('faq-list', faqs.value) } }

  function toggleFavorite(id) {
    const i = favorites.value.indexOf(id)
    if (i !== -1) favorites.value.splice(i, 1); else favorites.value.push(id)
    save('faq-favorites', favorites.value)
    return favorites.value.includes(id)
  }

  function isFavorite(id) { return favorites.value.includes(id) }
  const favoriteFaqs = computed(() => favorites.value.map(id => faqs.value.find(f => f.id === id)).filter(Boolean))
  const historyWithFaq = computed(() => viewHistory.value.slice(0, 50).map(h => ({ ...h, faq: faqs.value.find(f => f.id === h.faqId) })).filter(h => h.faq))

  // 标签管理
  function addTag(tag, skipSave = false) {
    const n = { ...tag, id: tag.id || genId(), usageCount: 0 }
    if (!tags.value.find(t => t.id === n.id)) tags.value.push(n)
    if (!skipSave) save('faq-tags', tags.value)
    return n
  }
  function updateTag(id, data) {
    const i = tags.value.findIndex(t => t.id === id)
    if (i !== -1) { tags.value[i] = { ...tags.value[i], ...data }; save('faq-tags', tags.value) }
  }
  function deleteTag(id) {
    tags.value = tags.value.filter(t => t.id !== id)
    faqs.value.forEach(f => { if (f.tags) f.tags = f.tags.filter(tid => tid !== id) })
    save('faq-tags', tags.value); save('faq-list', faqs.value)
  }
  function updateTagUsage() {
    tags.value.forEach(tag => { tag.usageCount = faqs.value.filter(f => f.tags && f.tags.includes(tag.id)).length })
    save('faq-tags', tags.value)
  }
  function getTagName(id) { const t = tags.value.find(x => x.id === id); return t ? t.name : '未知标签' }
  function getTag(id) { return tags.value.find(x => x.id === id) }

  function searchFaqs(query, options = {}) {
    const q = query.toLowerCase()
    let result = faqs.value.filter(f =>
      f.title.toLowerCase().includes(q) || (f.content || '').toLowerCase().includes(q) ||
      (f.summary || '').toLowerCase().includes(q) || (f.solution || '').toLowerCase().includes(q) ||
      (f.keywords || '').toLowerCase().includes(q)
    )
    if (options.machineId) result = result.filter(f => f.machineId === options.machineId)
    if (options.tagId) result = result.filter(f => f.tags && f.tags.includes(options.tagId))
    if (options.categoryId && options.machineStore) {
      const mids = options.machineStore.machines.filter(m => m.categoryId === options.categoryId).map(m => m.id)
      result = result.filter(f => mids.includes(f.machineId))
    }
    if (options.priority) result = result.filter(f => f.priority === options.priority)
    if (options.status) result = result.filter(f => f.status === options.status)
    switch (options.sortBy) {
      case 'newest': result.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt)); break
      case 'oldest': result.sort((a, b) => new Date(a.updatedAt) - new Date(b.updatedAt)); break
      case 'popular': result.sort((a, b) => (b.viewCount || 0) - (a.viewCount || 0)); break
      case 'rating': result.sort((a, b) => (b.rating || 0) - (a.rating || 0)); break
      case 'helpful': result.sort((a, b) => (b.helpfulCount || 0) - (a.helpfulCount || 0)); break
      default: result.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt))
    }
    return result
  }

  return {
    faqs, tags, favorites, viewHistory, faqCount, favoriteCount,
    recentFaqs, popularFaqs, topRatedFaqs, favoriteFaqs, historyWithFaq,
    getFaqsByMachine, getFaqsByCategory, getFaq,
    addFaq, updateFaq, deleteFaq, recordView, rateFaq, markHelpful, toggleFavorite, isFavorite,
    addTag, updateTag, deleteTag, getTagName, getTag,
    searchFaqs
  }
})
