# ScienceNotion (Cloudflare Pages Starter)

这是一个可直接部署到 Cloudflare Pages 的首发版骨架，包含三层内容结构：

- `Editorial` 主发布内容（权威层）
- `News` 新闻与动态（时效层）
- `Wiki` 社区共建词条（社区层）

## 目录结构

```text
sciencenotion/
  assets/css/styles.css
  data/content-index.json
  pages/*.html
  index.html
  rss.xml
  _headers
  _redirects
```

## 本地预览

在项目目录执行：

```bash
cd /Users/jasper/Documents/codex/sciencenotion
python3 -m http.server 4173
```

浏览器访问 `http://localhost:4173`。

## 部署到 Cloudflare Pages

1. 把该目录推到 GitHub 仓库。
2. 进入 Cloudflare Dashboard -> `Workers & Pages` -> `Create` -> `Pages` -> `Connect to Git`。
3. 选择仓库后，构建配置填写：
- `Framework preset`: `None`
- `Build command`: 留空
- `Build output directory`: `/`（仓库根目录）
4. 点击 `Save and Deploy`。

## 绑定你的域名

1. 在 Cloudflare Pages 项目中进入 `Custom domains`。
2. 添加你的主域名（例如 `sciencenotion.com`）和 `www` 子域。
3. 按提示创建/确认 DNS 记录（如果域名已托管到 Cloudflare，通常自动完成）。
4. 等待 SSL 证书签发，状态变为 Active 后即可访问。

## 上线前必须替换

- `rss.xml` 里的 `https://example.com` 改为你的正式域名。
- `pages/news-weekly-2026-02-15.html` 中示例来源链接替换为真实来源。
- 根据你的定位新增首批概念页（建议至少 20 篇）。

## 下一步升级建议

1. 把静态 HTML 迁移为 Next.js + MDX（便于模板化和搜索）。
2. 引入数据库实现 Wiki 审核流（`draft/pending/approved/rejected/archived`）。
3. 增加全文检索与订阅系统（邮件 + RSS 自动发布）。
