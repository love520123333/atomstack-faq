<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <div class="not-found-code">404</div>
      <h1 class="not-found-title">页面未找到</h1>
      <p class="not-found-desc">抱歉，您访问的页面不存在或已被移除</p>
      <div class="not-found-actions">
        <el-button type="primary" size="large" @click="$router.push('/')">返回首页</el-button>
        <el-button size="large" @click="$router.back()">返回上页</el-button>
      </div>
      <div class="not-found-links">
        <router-link to="/">管理后台</router-link>
        <span class="not-found-divider">|</span>
        <router-link to="/help">帮助中心</router-link>
        <span class="not-found-divider">|</span>
        <router-link to="/help/search">搜索 FAQ</router-link>
      </div>
    </div>
    <div class="not-found-bg"></div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found-page {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: #f0f2f5; position: relative; overflow: hidden;
}
.not-found-content { text-align: center; z-index: 1; }
.not-found-code {
  font-size: 160px; font-weight: 900; line-height: 1;
  background: linear-gradient(135deg, #1a73e8, #0d47a1);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px; letter-spacing: -8px;
}
.not-found-title { font-size: 28px; font-weight: 700; color: #1a1a2e; margin-bottom: 8px; }
.not-found-desc { font-size: 16px; color: #999; margin-bottom: 32px; }
.not-found-actions { display: flex; gap: 12px; justify-content: center; margin-bottom: 24px; }
.not-found-links { display: flex; justify-content: center; align-items: center; gap: 12px; }
.not-found-links a { color: #1a73e8; text-decoration: none; font-size: 14px; }
.not-found-links a:hover { text-decoration: underline; }
.not-found-divider { color: #ddd; }
.not-found-bg {
  position: absolute; width: 600px; height: 600px; border-radius: 50%;
  background: radial-gradient(circle, rgba(26,115,232,0.05) 0%, transparent 70%);
  top: -200px; right: -200px;
}
</style>
