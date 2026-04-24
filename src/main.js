import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import './styles/index.css'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

const pinia = createPinia()
app.use(pinia)

// 在 mount 之前初始化数据，确保所有组件渲染时 store 已有数据
import { useMachineStore } from './stores/machine'
import { useFaqStore } from './stores/faq'
import { initSampleData } from './data/sampleData'
const machineStore = useMachineStore()
const faqStore = useFaqStore()
initSampleData(machineStore, faqStore)

app.use(router)
app.use(ElementPlus, { locale: zhCn })
app.mount('#app')
