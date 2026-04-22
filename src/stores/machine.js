import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

function genId() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8) }
function load(key, def = []) { try { const d = localStorage.getItem(key); return d ? JSON.parse(d) : def } catch { return def } }
function save(key, data) { try { localStorage.setItem(key, JSON.stringify(data)) } catch { } }

export const useMachineStore = defineStore('machine', () => {
  const categories = ref(load('faq-categories', [
    { id: 'cat-1', name: 'A系列半导体雕刻机', icon: 'Cpu', color: '#409eff', description: 'A5 Pro, A6 Pro, A10 Pro V2, A12 Pro, A20 Pro V2 等' },
    { id: 'cat-2', name: '大功率雕刻机', icon: 'Lightning', color: '#e6a23c', description: 'A70 Pro, A70 Max, AE85 等大功率工业级雕刻机' },
    { id: 'cat-3', name: '创新系列', icon: 'MagicStick', color: '#67c23a', description: 'Kraft, P1, Fusion, Atelier, Swift, Swift Mini 等创新产品' },
    { id: 'cat-4', name: 'CNC雕刻机', icon: 'SetUp', color: '#f56c6c', description: 'C4 Pro 四轴CNC雕刻机' },
    { id: 'cat-5', name: 'CO₂激光雕刻机', icon: 'Sunny', color: '#b37feb', description: 'Hurricane (K60) 二氧化碳激光雕刻机' },
    { id: 'cat-6', name: '拓展配件', icon: 'Box', color: '#909399', description: '旋转模块、传送带、空气净化器、空气辅助等' },
    { id: 'cat-7', name: '防护与工作台', icon: 'Shield', color: '#36cfc9', description: '防护箱、蜂窝板、增高台等' }
  ]))

  const machines = ref(load('faq-machines', []))

  const machineCount = computed(() => machines.value.length)
  const categoryCount = computed(() => categories.value.length)

  function getCategoryName(id) { const c = categories.value.find(x => x.id === id); return c ? c.name : '未分类' }
  function getCategory(id) { return categories.value.find(x => x.id === id) }

  function addCategory(cat, skipSave = false) {
    const n = { ...cat, id: cat.id || genId() }
    if (!categories.value.find(x => x.id === n.id)) categories.value.push(n)
    if (!skipSave) save('faq-categories', categories.value)
    return n
  }
  function updateCategory(id, data) {
    const i = categories.value.findIndex(x => x.id === id)
    if (i !== -1) { categories.value[i] = { ...categories.value[i], ...data }; save('faq-categories', categories.value) }
  }
  function deleteCategory(id) {
    const i = categories.value.findIndex(x => x.id === id)
    if (i !== -1) {
      categories.value.splice(i, 1)
      machines.value.forEach(m => { if (m.categoryId === id) m.categoryId = '' })
      save('faq-categories', categories.value); save('faq-machines', machines.value)
    }
  }
  function addMachine(m, skipSave = false) {
    const n = { ...m, id: m.id || genId() }
    if (!machines.value.find(x => x.id === n.id)) machines.value.push(n)
    if (!skipSave) save('faq-machines', machines.value)
    return n
  }
  function updateMachine(id, data) {
    const i = machines.value.findIndex(x => x.id === id)
    if (i !== -1) { machines.value[i] = { ...machines.value[i], ...data }; save('faq-machines', machines.value) }
  }
  function deleteMachine(id) {
    const i = machines.value.findIndex(x => x.id === id)
    if (i !== -1) { machines.value.splice(i, 1); save('faq-machines', machines.value) }
  }
  function getMachine(id) { return machines.value.find(x => x.id === id) }
  function searchMachines(query) {
    const q = query.toLowerCase()
    return machines.value.filter(m => m.name.toLowerCase().includes(q) || (m.brand || '').toLowerCase().includes(q) || (m.model || '').toLowerCase().includes(q) || (m.description || '').toLowerCase().includes(q))
  }
  return { categories, machines, machineCount, categoryCount, getCategoryName, getCategory, addCategory, updateCategory, deleteCategory, addMachine, updateMachine, deleteMachine, getMachine, searchMachines }
})
