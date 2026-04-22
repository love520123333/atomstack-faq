import { marked } from 'marked'
marked.setOptions({ breaks: true, gfm: true })

export function renderMarkdown(content) {
  if (!content) return ''
  return marked.parse(content)
}

export function formatDate(dateStr) {
  if (!dateStr) return '-'
  const diff = Date.now() - new Date(dateStr).getTime()
  const m = Math.floor(diff / 60000), h = Math.floor(diff / 3600000), d = Math.floor(diff / 86400000)
  if (m < 1) return '刚刚'
  if (m < 60) return `${m}分钟前`
  if (h < 24) return `${h}小时前`
  if (d < 7) return `${d}天前`
  if (d < 30) return `${Math.floor(d / 7)}周前`
  return new Date(dateStr).toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

export function formatFullDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

export function getPriorityColor(p) { return { critical: '#f56c6c', high: '#e6a23c', medium: '#409eff', low: '#67c23a' }[p] || '#909399' }
export function getPriorityText(p) { return { critical: '紧急', high: '高', medium: '中', low: '低' }[p] || '未知' }
export function getStatusColor(s) { return { draft: '#909399', published: '#67c23a', archived: '#e6a23c' }[s] || '#909399' }
export function getStatusText(s) { return { draft: '草稿', published: '已发布', archived: '已归档' }[s] || '未知' }

export function truncate(text, len = 100) {
  if (!text) return ''
  const plain = text.replace(/<[^>]*>/g, '').replace(/[#*_`~>\-\[\]()]/g, '')
  return plain.length > len ? plain.slice(0, len) + '...' : plain
}

export function downloadFile(content, filename, type = 'text/markdown') {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = filename; a.click()
  URL.revokeObjectURL(url)
}

export function exportAsMarkdown(faq, machineStore) {
  const machine = machineStore.getMachine(faq.machineId)
  const mname = machine ? machine.name : '未知机型'
  const cname = machine ? machineStore.getCategoryName(machine.categoryId) : '未知分类'
  let md = `# ${faq.title}\n\n`
  md += `- **机型**: ${mname}\n- **分类**: ${cname}\n- **优先级**: ${getPriorityText(faq.priority)}\n- **创建时间**: ${formatFullDate(faq.createdAt)}\n- **更新时间**: ${formatFullDate(faq.updatedAt)}\n\n`
  if (faq.summary) md += `## 问题描述\n\n${faq.summary}\n\n`
  if (faq.solution) md += `## 解决方案\n\n${faq.solution}\n\n`
  if (faq.content) md += `## 详细内容\n\n${faq.content}\n\n`
  return md
}

export function exportAsHtml(faq, machineStore) {
  const machine = machineStore.getMachine(faq.machineId)
  const mname = machine ? machine.name : '未知机型'
  const cname = machine ? machineStore.getCategoryName(machine.categoryId) : '未知分类'
  let html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>${faq.title}</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif;max-width:800px;margin:40px auto;padding:20px;color:#333;line-height:1.8}
h1{border-bottom:2px solid #409eff;padding-bottom:10px}.meta{background:#f5f7fa;padding:16px;border-radius:8px;margin:16px 0}.meta span{margin-right:24px}.label{font-weight:bold;color:#606266}
pre{background:#282c34;color:#abb2bf;padding:16px;border-radius:6px;overflow-x:auto}code{background:#f5f5f5;padding:2px 6px;border-radius:3px}
blockquote{border-left:4px solid #409eff;padding:8px 16px;background:#ecf5ff;margin:12px 0}@media print{body{margin:20px}}</style></head><body>`
  html += `<h1>${faq.title}</h1><div class="meta"><span><span class="label">机型:</span> ${mname}</span><span><span class="label">分类:</span> ${cname}</span><span><span class="label">更新时间:</span> ${formatFullDate(faq.updatedAt)}</span></div>`
  if (faq.summary) html += `<h2>问题描述</h2><div>${renderMarkdown(faq.summary)}</div>`
  if (faq.solution) html += `<h2>解决方案</h2><div>${renderMarkdown(faq.solution)}</div>`
  if (faq.content) html += `<h2>详细内容</h2><div>${renderMarkdown(faq.content)}</div>`
  html += `</body></html>`
  return html
}
