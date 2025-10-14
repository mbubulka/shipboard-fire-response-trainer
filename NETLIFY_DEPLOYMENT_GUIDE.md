# 🚀 Netlify Deployment Guide

## Quick Deploy Steps

### Option 1: Direct Netlify Deploy
1. Go to [netlify.com](https://netlify.com) and log in
2. Click "New site from Git" 
3. Connect your GitHub account and select `mbubulka/shipboard-fire-response-trainer`
4. Set build settings:
   - **Build command**: `(leave empty)`
   - **Publish directory**: `web/bubulkaanalytics-site`
   - **Branch to deploy**: `main` (or `tufte-refactor-pass` for latest improvements)

### Option 2: Drag & Drop Deploy
1. Go to [netlify.com](https://netlify.com) and log in
2. Drag the entire `web/bubulkaanalytics-site` folder to the Netlify deploy area
3. Site will be live immediately with a random URL
4. You can change the site name in Site settings

## Site Structure
```
web/bubulkaanalytics-site/
├── index.html                    # Main landing page
├── firetrainer/
│   └── comprehensive.html        # Fire training system
├── analytics-dashboard.html      # Analytics dashboard
├── Michael_9028-Bkgd-square.jpg # Profile image
└── README.md                     # Project documentation
```

## Build Configuration (netlify.toml)
Create this file in the project root if using Git deploy:

```toml
[build]
  publish = "web/bubulkaanalytics-site"
  command = ""

[build.environment]
  NODE_VERSION = "18"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "*.html"
  [headers.values]
    Cache-Control = "public, max-age=3600"

[[headers]]
  for = "*.css"
  [headers.values]
    Cache-Control = "public, max-age=31536000"

[[headers]]
  for = "*.js"
  [headers.values]
    Cache-Control = "public, max-age=31536000"

[[headers]]
  for = "*.jpg"
  [headers.values]
    Cache-Control = "public, max-age=31536000"
```

## Custom Domain Setup (Optional)
1. In Netlify site settings, go to "Domain management"
2. Add custom domain (e.g., `bubulka-analytics.com`)
3. Follow DNS configuration instructions
4. SSL certificate will be provisioned automatically

## Environment Variables (If needed)
- No environment variables required for current setup
- All dependencies are embedded in HTML files

## Testing Checklist
After deployment, verify:
- ✅ Main page loads correctly
- ✅ Fire trainer launches properly
- ✅ Analytics dashboard is accessible
- ✅ All social links work
- ✅ Mobile responsiveness works
- ✅ No console errors in browser dev tools

## Continuous Deployment
Once connected to GitHub:
- Pushes to `main` branch auto-deploy
- Pull request previews available
- Branch deploys for testing available

## Rollback
- Use Netlify's "Deploys" tab to rollback to previous versions
- Git history allows reverting commits if needed

## Performance Optimization
Current optimizations applied:
- ✅ Self-contained HTML files (no external dependencies)
- ✅ Optimized CSS with custom properties
- ✅ Reduced backdrop-filter blur for better performance
- ✅ Responsive images and lazy loading ready
- ✅ Minification ready (can be enabled in Netlify build settings)

## Monitoring
- Netlify provides analytics for site traffic
- Built-in forms handling available
- Function deployment ready if needed

---
## 🎯 Result

Your website will be live at: `https://[your-site-name].netlify.app`

All improvements from the Tufte-Krug-Nielsen refactor are included and deployment-ready!