# No-Token Deployment Runbook

适用场景：不提供 Cloudflare API Token，仅使用 GitHub 自动触发 Cloudflare Pages 部署。

## 一次性设置（你在 Cloudflare 控制台点一次）

1. Cloudflare -> `Workers & Pages` -> `Create` -> `Pages` -> `Connect to Git`
2. 选择仓库：`yangyuezh/scholarnotion`
3. 配置：
- Framework preset: `None`
- Build command: 留空
- Build output directory: `/`
4. 点击 `Save and Deploy`
5. 在 `Custom domains` 绑定你的域名和 `www`

完成后，后续每次推送到 `main` 都会自动部署。

## 日常发布（我来执行）

```bash
cd /Users/jasper/Documents/codex/scholarnotion
./scripts/release.sh https://你的域名 "feat: 本次改动说明" v0.1.1
```

这个流程会自动：
- 检查站内链接
- 生成 `sitemap.xml`
- 提交并推送 `main`
- 可选打 tag 并推送

## 版本同步策略

- `main`: 生产环境（Cloudflare 自动部署）
- `vX.Y.Z` tag: 可回滚版本快照

## 何时再引入 Token

当你需要我自动做这些操作时再加：
- 改 Cloudflare DNS / WAF / 缓存规则
- 自动创建或修改 Pages 项目配置
- 自动发布运维报表到 Cloudflare 相关服务
