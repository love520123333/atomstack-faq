# AtomStack FAQ 管理系统

AtomStack 雕刻机常见问题解决方案管理系统，支持 FAQ 的增删改查、搜索筛选、收藏、导入导出等功能。

## 在线访问

GitHub Pages: https://love520123333.github.io/atomstack-faq/

## 功能特性

- 机型管理（20+ AtomStack 产品）
- FAQ 增删改查（Markdown 格式）
- 高级搜索和多维筛选
- FAQ 收藏和评分
- 数据导入/导出（JSON）
- 数据统计
- 分类和标签管理
- 响应式布局

## 技术栈

- Vue 3 + Vite
- Vue Router 4
- Pinia
- Element Plus
- Marked.js

## 本地开发

```bash
npm install
npm run dev
```

## 构建

```bash
npm run build
npm run preview
```

## 部署

推送到 `main` 分支后，GitHub Actions 会自动部署到 GitHub Pages。
