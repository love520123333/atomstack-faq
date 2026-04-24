<template>
  <div class="page-container">
    <div class="page-title">
      <el-icon><EditPen /></el-icon> {{ isEdit ? '编辑 FAQ' : '新建 FAQ' }}
      <div style="flex:1"></div>
      <el-button @click="$router.back()">取消</el-button>
      <el-button type="primary" :icon="Check" @click="handleSave" :loading="saving">保存</el-button>
    </div>

    <el-form :model="form" label-width="100px" label-position="top" class="faq-form">
      <el-row :gutter="20">
        <el-col :xs="24" :lg="16">
          <el-card shadow="never" class="mb-16">
            <el-form-item label="FAQ 标题" required>
              <el-input v-model="form.title" placeholder="简洁描述问题和解决方案" size="large" maxlength="100" show-word-limit />
            </el-form-item>

            <el-form-item label="关键词（逗号分隔，用于搜索）">
              <el-input v-model="form.keywords" placeholder="如: 激光不亮, 不出光, 烧毁" />
            </el-form-item>

            <el-form-item label="问题描述（Markdown）">
              <el-input v-model="form.summary" type="textarea" :rows="4" placeholder="描述用户遇到的问题现象..." />
            </el-form-item>

            <el-form-item label="解决方案（Markdown）">
              <el-input v-model="form.solution" type="textarea" :rows="8" placeholder="详细步骤化解决方案，支持 Markdown 格式..." />
            </el-form-item>

            <el-form-item label="补充内容（Markdown，可选）">
              <el-input v-model="form.content" type="textarea" :rows="6" placeholder="额外的注意事项、原理说明、相关链接等..." />
            </el-form-item>

            <!-- 实时预览 -->
            <el-collapse v-if="form.summary || form.solution || form.content">
              <el-collapse-item title="📖 实时预览" name="preview">
                <div class="faq-content" v-html="renderMarkdown(form.summary)" v-if="form.summary" />
                <h3 v-if="form.summary && form.solution" style="margin-top:16px">解决方案</h3>
                <div class="faq-content" v-html="renderMarkdown(form.solution)" v-if="form.solution" />
                <div class="faq-content" v-html="renderMarkdown(form.content)" v-if="form.content" />
              </el-collapse-item>
            </el-collapse>
          </el-card>
        </el-col>

        <el-col :xs="24" :lg="8">
          <el-card shadow="never" class="mb-16">
            <el-form-item label="所属机型" required>
              <el-select v-model="form.machineId" placeholder="选择机型" style="width:100%" filterable>
                <el-option-group v-for="cat in machineStore.categories" :key="cat.id" :label="cat.name">
                  <el-option v-for="m in machineStore.machines.filter(x=>x.categoryId===cat.id)" :key="m.id" :label="m.name" :value="m.id" />
                </el-option-group>
              </el-select>
            </el-form-item>

            <el-form-item label="优先级" required>
              <el-radio-group v-model="form.priority">
                <el-radio-button value="critical"><span style="color:#f56c6c">紧急</span></el-radio-button>
                <el-radio-button value="high"><span style="color:#e6a23c">高</span></el-radio-button>
                <el-radio-button value="medium"><span style="color:#409eff">中</span></el-radio-button>
                <el-radio-button value="low"><span style="color:#67c23a">低</span></el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="状态">
              <el-radio-group v-model="form.status">
                <el-radio-button value="published">已发布</el-radio-button>
                <el-radio-button value="draft">草稿</el-radio-button>
                <el-radio-button value="archived">已归档</el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="标签">
              <el-select v-model="form.tags" multiple placeholder="选择标签" style="width:100%" collapse-tags collapse-tags-tooltip>
                <el-option v-for="tag in faqStore.tags" :key="tag.id" :label="tag.name" :value="tag.id">
                  <span :style="{ display:'inline-block', width:'8px', height:'8px', borderRadius:'50%', background: tag.color, marginRight:'8px' }"></span>
                  {{ tag.name }}
                </el-option>
              </el-select>
            </el-form-item>
          </el-card>

          <!-- 快速操作 -->
          <el-card shadow="never">
            <template #header><span style="font-weight:600">💡 提示</span></template>
            <ul style="font-size:13px;color:#606266;line-height:2;padding-left:16px">
              <li>问题描述和解决方案支持 <strong>Markdown</strong> 语法</li>
              <li>好的标题能帮助用户快速找到答案</li>
              <li>关键词用逗号分隔，影响搜索结果</li>
              <li>标签可以多选，便于分类筛选</li>
              <li>优先级用于标识问题的重要程度</li>
            </ul>
          </el-card>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Check, EditPen } from '@element-plus/icons-vue'
import { useFaqStore } from '../stores/faq'
import { useMachineStore } from '../stores/machine'
import { renderMarkdown } from '../utils'
import { initSampleData } from '../data/sampleData'

const route = useRoute()
const router = useRouter()
const faqStore = useFaqStore()
const machineStore = useMachineStore()
const saving = ref(false)

const isEdit = computed(() => !!route.params.id)

const form = ref({
  title: '', machineId: '', priority: 'medium', status: 'published',
  tags: [], keywords: '', summary: '', solution: '', content: ''
})

onMounted(async () => {
  initSampleData(machineStore, faqStore)
  await nextTick()
  if (isEdit.value) {
    const faq = faqStore.getFaq(route.params.id)
    if (faq) {
      form.value = { title: faq.title, machineId: faq.machineId, priority: faq.priority || 'medium', status: faq.status || 'published', tags: faq.tags || [], keywords: faq.keywords || '', summary: faq.summary || '', solution: faq.solution || '', content: faq.content || '' }
    } else {
      ElMessage.error('FAQ 不存在')
      router.push('/faq')
    }
  }
  // URL query: 预选机型
  if (route.query.machine) form.value.machineId = route.query.machine
})

function handleSave() {
  if (!form.value.title.trim()) { ElMessage.warning('请输入标题'); return }
  if (!form.value.machineId) { ElMessage.warning('请选择机型'); return }
  saving.value = true
  setTimeout(() => {
    if (isEdit.value) {
      faqStore.updateFaq(route.params.id, form.value)
      ElMessage.success('更新成功')
    } else {
      const newFaq = faqStore.addFaq(form.value)
      ElMessage.success('创建成功')
      router.replace(`/faq/${newFaq.id}`)
    }
    saving.value = false
  }, 200)
}
</script>

<style scoped>
.mb-16 { margin-bottom: 16px; }
.faq-form :deep(.el-card__body) { padding-top: 16px; }
</style>
