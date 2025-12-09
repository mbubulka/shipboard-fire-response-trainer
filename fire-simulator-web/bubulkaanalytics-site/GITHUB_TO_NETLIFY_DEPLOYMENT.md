# GitHub → Netlify Deployment Checklist

## ✅ Phase 1: GitHub Repository Setup

**Timeline:** ~10 minutes

### Step 1.1: Create GitHub Repository
- [ ] Go to https://github.com/new
- [ ] **Repository name:** `military-salary-estimator`
- [ ] **Description:** "GLM-based salary predictor for military-to-civilian transitions (96% accuracy)"
- [ ] **Visibility:** Public
- [ ] **Initialize:** DO NOT add README/license/gitignore (you have these)
- [ ] Click "Create repository"

### Step 1.2: Push to GitHub
```bash
# In PowerShell, navigate to project directory
cd "d:\R projects\week 15\Presentation Folder"

# If git not initialized
git init
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Add all files and commit
git add .
git commit -m "Initial commit: Military-to-Civilian Salary Estimator with Shiny dashboard"

# Add remote and push
git remote add origin https://github.com/mbubulka/military-salary-estimator.git
git branch -M main
git push -u origin main
```

### Step 1.3: Verify GitHub
- [ ] Visit https://github.com/mbubulka/military-salary-estimator
- [ ] Confirm README displays correctly
- [ ] Verify archive folders are NOT present
- [ ] Check that files are tracked (git ls-files shows ~150+ files)
- [ ] Test: Clone to verify it works

**Expected Output:**
```
✓ Repository created
✓ ~200+ files tracked
✓ README.md displays as project overview
✓ .gitignore excludes archives correctly
✓ No archive folders visible
✓ Fresh clone succeeds
```

---

## ✅ Phase 2: Netlify Setup

**Timeline:** ~15 minutes

### Step 2.1: Create Netlify Account
- [ ] Go to https://app.netlify.com/signup
- [ ] Sign in with GitHub (recommended)
- [ ] Authorize Netlify to access your GitHub repos

### Step 2.2: Deploy bubulkaanalytics Site
- [ ] Click "New site from Git"
- [ ] Select "GitHub"
- [ ] Choose `shipboard-fire-response` repository
- [ ] Configure build settings:
  - **Base directory:** `web/bubulkaanalytics-site`
  - **Build command:** (leave blank)
  - **Publish directory:** `.` (dot = root of site folder)
- [ ] Click "Deploy site"

### Step 2.3: Verify Deployment
- [ ] Netlify assigns temporary domain (e.g., `brave-xyz-123.netlify.app`)
- [ ] Wait for build to complete (~30 seconds)
- [ ] Visit temporary domain
- [ ] Check:
  - [ ] Index page loads
  - [ ] Project link to `/projects/military-salary-estimator/` works
  - [ ] GitHub links redirect correctly
  - [ ] No console errors

**Expected Output:**
```
✓ Site deployed successfully
✓ Domain: brave-xyz-123.netlify.app (temporary)
✓ Build status: Published
✓ No deploy errors
```

---

## ✅ Phase 3: Configure Custom Domain

**Timeline:** ~20 minutes (DNS propagation may take up to 24 hours)

### Step 3.1: Add Custom Domain in Netlify
- [ ] Go to Netlify Site Settings
- [ ] Click "Domain management"
- [ ] Click "Add custom domain"
- [ ] Enter: `bubulkaanalytics.com`
- [ ] Netlify will suggest nameservers or CNAME

### Step 3.2: Configure DNS

**Option A: Use Netlify Nameservers (Recommended)**
1. Netlify will provide 4 nameservers
2. Go to your domain registrar (GoDaddy, Namecheap, etc.)
3. Update nameservers to Netlify's nameservers
4. Wait 24-48 hours for propagation

**Option B: CNAME Record (If using existing registrar)**
1. In Netlify: Copy CNAME target (e.g., `brave-xyz-123.netlify.app`)
2. Go to domain registrar DNS settings
3. Add CNAME record:
   - Name: `@` or leave blank
   - Value: Netlify's domain
4. Wait for DNS propagation

### Step 3.3: Verify Domain
- [ ] DNS records propagated (check at https://dnschecker.org)
- [ ] Visit https://bubulkaanalytics.com
- [ ] Confirm main site loads
- [ ] Confirm HTTPS enabled (green lock icon)
- [ ] Test project link: https://bubulkaanalytics.com/projects/military-salary-estimator/

**Expected Output:**
```
✓ Domain points to Netlify
✓ HTTPS certificate issued (automatic)
✓ Main site accessible
✓ Project page accessible
✓ GitHub links work
```

---

## ✅ Phase 4: Update Portfolio

**Timeline:** ~5 minutes

### Step 4.1: Update Main Index

Edit the main `bubulkaanalytics-site/index.html` to add a link to the new project:

```html
<!-- Add to projects section -->
<div class="project-card">
    <a href="projects/military-salary-estimator/">
        <h3>🎯 Military Salary Estimator</h3>
        <p>96% accurate GLM model predicting military-to-civilian salary transitions</p>
        <span class="tag">Data Science</span>
        <span class="tag">R Shiny</span>
        <span class="tag">GitHub</span>
    </a>
</div>
```

### Step 4.2: Commit and Push
```bash
cd "d:\projects\shipboard-fire-response\web\bubulkaanalytics-site"

git add .
git commit -m "Add Military Salary Estimator to portfolio"
git push origin main
```

### Step 4.3: Verify Auto-Deploy
- [ ] Netlify automatically deploys on git push
- [ ] Check Netlify Dashboard → Deploys
- [ ] Wait for "Published" status
- [ ] Visit updated portfolio site

**Expected Output:**
```
✓ New commit pushed to GitHub
✓ Netlify auto-deploys within 30 seconds
✓ Project appears on portfolio
✓ All links work
```

---

## ✅ Phase 5: Final Testing

**Timeline:** ~10 minutes

### Test Checklist

**Main Site (bubulkaanalytics.com)**
- [ ] Index page loads
- [ ] CSS/styling renders correctly
- [ ] All images load
- [ ] Navigation works
- [ ] Mobile responsive
- [ ] No console errors

**Project Page (/projects/military-salary-estimator/)**
- [ ] Page loads quickly
- [ ] Hero section displays
- [ ] Stats cards visible
- [ ] Quick links functional
- [ ] GitHub link redirects correctly
- [ ] Mobile responsive

**GitHub Repository**
- [ ] Public and accessible
- [ ] README displays on GitHub
- [ ] Clone works: `git clone https://github.com/mbubulka/military-salary-estimator.git`
- [ ] requirements.R executable
- [ ] Shiny app runnable (local testing)

**Redirects**
- [ ] `/salary-estimator-repo` → GitHub
- [ ] `/military-salary` → project page
- [ ] `/health` → main page

### Performance Checks
- [ ] Page load time < 2 seconds
- [ ] No 404 errors
- [ ] No mixed content warnings
- [ ] HTTPS everywhere (no insecure content)

---

## 📋 Deployment Rollback Plan

If something goes wrong:

### Revert Git Commit
```bash
git log --oneline -5          # View recent commits
git revert HEAD               # Undo last commit
git push origin main          # Netlify redeploys
```

### Deploy Previous Version
```bash
git checkout <commit-hash>    # Go to specific version
git push --force origin main  # Force push (careful!)
```

### Netlify Rollback
1. Go to Netlify Dashboard
2. Click "Deploys" tab
3. Find previous successful deploy
4. Click menu (⋯) → "Publish deploy"

---

## 🔒 Post-Deployment Security

### Step 1: Enable Branch Protection
1. GitHub repo → Settings → Branches
2. Add rule for "main" branch
3. Require pull request reviews
4. Require status checks before merge

### Step 2: Monitor Netlify
- [ ] Enable Netlify notifications
- [ ] Monitor deploy logs for errors
- [ ] Check uptime status

### Step 3: GitHub Security
- [ ] Enable "Dependabot alerts"
- [ ] Review security tab
- [ ] Enable two-factor authentication

---

## 📊 Post-Deployment Analytics

### Add Google Analytics (Optional)
```html
<!-- Add to head of bubulkaanalytics-site/index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Monitor Performance
- Netlify Dashboard → Analytics
- Check deployment success rate
- Monitor page load times
- Track bandwidth usage

---

## 🚀 Go Live Checklist

### Before Announcement
- [ ] All tests passing
- [ ] Domain verified (HTTPS working)
- [ ] GitHub repo public and complete
- [ ] Portfolio updated
- [ ] No console errors
- [ ] Mobile tested

### Day of Launch
- [ ] All systems operational
- [ ] Backup created
- [ ] Support documentation ready
- [ ] Social media posts prepared

### After Launch
- [ ] Monitor for errors (first 24 hours)
- [ ] Respond to any issues quickly
- [ ] Share portfolio on GitHub/LinkedIn
- [ ] Collect feedback

---

## ❓ Troubleshooting

### Site Not Deploying
```
1. Check git push succeeded: git log -1
2. Verify netlify.toml is in correct directory
3. Check Netlify Dashboard → Deploys for errors
4. Review build logs (click failed deploy)
```

### Domain Not Resolving
```
1. Check DNS propagation: https://dnschecker.org
2. Verify nameservers at registrar match Netlify
3. Clear browser cache (Ctrl+Shift+Delete)
4. Wait up to 24 hours for propagation
```

### Project Page 404
```
1. Verify /projects/military-salary-estimator/index.html exists
2. Check netlify.toml has correct redirect rules
3. Verify _redirects file is present
4. Test locally: open index.html in browser
```

### HTTPS Issues
```
1. Netlify auto-provisions SSL (no action needed)
2. If certificate error, check domain is correct
3. Force HTTPS: Netlify Dashboard → Domain settings
```

---

## 📞 Support Links

- **Netlify Docs:** https://docs.netlify.com/
- **GitHub Pages:** https://docs.github.com/en/pages
- **DNS Checker:** https://dnschecker.org/
- **SSL Checker:** https://www.sslshopper.com/ssl-checker.html
- **Website Speed Test:** https://gtmetrix.com/

---

## ✅ Final Sign-Off

When all checks are complete:

- [ ] GitHub repository public & accessible
- [ ] Netlify deployment successful
- [ ] Custom domain working with HTTPS
- [ ] Portfolio updated with new project
- [ ] All tests passing
- [ ] Documentation complete

**Status:** ✅ READY FOR PUBLIC LAUNCH

---

**Estimated Total Time:** 45 minutes - 2 hours (depends on DNS propagation)

**Go Live:** You're ready to share! 🚀

