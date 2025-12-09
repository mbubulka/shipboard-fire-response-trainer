# 🛡️ Portfolio Maintenance Guide - Prevent Future Issues

## Problem Identified
Multiple old versions of portfolio files are causing navigation to break when projects are updated:
- `index-professional.html` (OLD - only 4 projects)
- `firetrainer-professional.html` (OLD)
- `potomac_dashboard_hybrid.html` (TEST VERSION)
- `potomac_dashboard_live.html` (TEST VERSION)
- `potomac_static.html` (STATIC HTML BACKUP)

**Solution:** Clean up old files and establish a single source of truth.

---

## 📋 Current Production Files (USE ONLY THESE)

```
d:\Projects\fire-simulator-web\bubulkaanalytics-site\

✅ ACTIVE PRODUCTION
├── index.html                          ← MAIN PORTFOLIO (all 6 projects)
├── firetrainer/comprehensive.html      ← Fire trainer project
├── potomac_dashboard.html              ← Static River Flow backup
└── (other project files as needed)

⚠️ OLD/TEST FILES TO DELETE
├── index-professional.html             ❌ DELETE (outdated)
├── firetrainer-professional.html       ❌ DELETE (outdated)
├── potomac_dashboard_hybrid.html       ❌ DELETE (test version)
├── potomac_dashboard_live.html         ❌ DELETE (test version)
├── potomac_dashboard_final_exact.html  ❌ DELETE (test version)
├── potomac_dashboard_simple.html       ❌ DELETE (test version)
└── firetrainer-professional.html       ❌ DELETE (duplicate)
```

---

## ✅ Cleanup Checklist

### Step 1: Delete Old Files
```powershell
cd d:\Projects\fire-simulator-web\bubulkaanalytics-site

# Remove old versions
Remove-Item index-professional.html
Remove-Item firetrainer-professional.html
Remove-Item potomac_dashboard_hybrid.html
Remove-Item potomac_dashboard_live.html
Remove-Item potomac_dashboard_final_exact.html
Remove-Item potomac_dashboard_simple.html
```

### Step 2: Verify Production Files
Make sure these are the ONLY active files:
- ✅ `index.html` - Has all 6 projects with correct links
- ✅ `firetrainer/comprehensive.html` - Links back to index.html
- ✅ `potomac_dashboard.html` - Static backup (links to Shiny app)

### Step 3: Commit Cleanup
```bash
git add -A
git commit -m "Clean up old portfolio test files - keep only production index.html"
git push origin main
```

---

## 🚀 Adding New Projects - Safe Process

### Step 1: Edit ONLY `index.html`
```html
<!-- New project card -->
<div class="project-card">
    <div class="project-header">
        <span class="live-badge">Live</span>
        <p class="project-type">Project Type</p>
        <h3>Project Name</h3>
    </div>
    <div class="project-body">
        <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 0.75rem; margin-bottom: 1rem; border-radius: 4px;">
            <strong>Problem:</strong> What problem does it solve?
        </div>
        <p class="project-description">Brief description...</p>
        <div class="project-tech">
            <span class="tech-tag">Tech1</span>
            <span class="tech-tag">Tech2</span>
        </div>
        <div class="project-links">
            <a href="[LIVE_URL]" target="_blank" class="project-link">Live Demo</a>
            <a href="https://github.com/mbubulka" class="project-link">View Code</a>
        </div>
    </div>
</div>
```

### Step 2: NEVER Edit These Files
❌ Don't create new index files (index-v2.html, index-new.html, etc.)
❌ Don't create duplicate project files
❌ Don't copy/paste index.html with a new name

### Step 3: Test Before Committing
1. Open `index.html` locally in browser
2. Click through all project links
3. Verify "Back to Portfolio" buttons work
4. Check that all 6 projects display

### Step 4: Commit & Push
```bash
git add index.html
git commit -m "Add new project: [Project Name]"
git push origin main
# Netlify auto-deploys
```

---

## 🔒 Prevent Accidental File Multiplication

### Use .gitignore to Prevent Test Files
Add to `d:\Projects\.gitignore`:
```
# Ignore test portfolio versions
*-professional.html
*-test.html
*-draft.html
*-old.html
*-backup.html
*-hybrid.html
*-live.html
*-simple.html
*-final*.html
```

### Use a Consistent Naming Convention
✅ **Good:**
- `index.html` - Main portfolio
- `projectname/page.html` - Project pages

❌ **Bad:**
- `index-professional.html`
- `index_new.html`
- `index_v2.html`
- `index_backup.html`

---

## 📊 Current Portfolio Structure (Correct)

```
6 Projects in index.html:

1. Fire Response Trainer
   ├── Type: AI Training System
   ├── Link: firetrainer/comprehensive.html
   └── Back button: ../index.html ✅

2. River Flow Predictor
   ├── Type: Predictive Analytics
   ├── Link: https://mbubulka.shinyapps.io/potomac-river-predictor/
   └── Badge: Live on Shiny ✅

3. College Cost Analysis Suite
   ├── Type: Cross-Platform Analytics
   ├── Tech: Tableau + Power BI
   └── Links: integrated-analytics.html ✅

4. Military Pay Estimator
   ├── Type: Financial Planning
   ├── Link: https://mbubulka.shinyapps.io/military-salary-estimator/
   └── Badge: Live on Shiny ✅

5. River Access MVP
   ├── Type: Location-Based Analytics
   ├── Tech: Python/PostgreSQL
   └── Link: GitHub profile ✅

6. Explainable Heart Disease Prediction
   ├── Type: Healthcare AI
   ├── Link: Azure ML Dashboard
   └── Badge: Live on Azure ✅
```

---

## 🎯 Best Practices Going Forward

### DO ✅
- Edit ONLY `index.html` for portfolio updates
- Use consistent HTML structure for new project cards
- Test locally before pushing
- Write clear git commit messages
- Keep project links as URLs when possible (Shiny, Azure, GitHub)

### DON'T ❌
- Create new portfolio files with different names
- Leave old test files in the repo
- Link to `index-professional.html` or other old versions
- Copy/paste entire HTML files
- Make changes without testing first

### Before Adding a Project
1. ✅ Have the live URL ready (Shiny, GitHub, etc.)
2. ✅ Write the problem statement
3. ✅ List the tech stack
4. ✅ Copy the HTML structure from an existing project
5. ✅ Update only the content, not the structure
6. ✅ Test all links locally

### When Something Breaks
1. Check if multiple versions of index.html exist
2. Search for hardcoded links to old files
3. Verify all "back to portfolio" buttons point to `index.html`
4. Look for old project files still being referenced

---

## 🧹 Immediate Action Items

### This Session:
1. Delete old portfolio versions:
   - index-professional.html
   - firetrainer-professional.html
   - potomac_dashboard_hybrid.html
   - potomac_dashboard_live.html
   - potomac_dashboard_final_exact.html
   - potomac_dashboard_simple.html

2. Verify index.html has correct links for all 6 projects

3. Commit cleanup

### Future Sessions:
- Always edit ONLY index.html
- Never create duplicate portfolio files
- Test locally before pushing
- Verify back buttons point to index.html

---

## 📞 Troubleshooting Checklist

If portfolio breaks after an update:

- [ ] Check how many `index*.html` files exist
- [ ] Verify which one is linked from project pages
- [ ] Search for references to old file names in HTML
- [ ] Confirm all "back" links point to `index.html`
- [ ] Check Netlify deployment logs
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Check git diff to see what changed
- [ ] Revert last commit if needed: `git revert HEAD`

---

## 🎓 Why This Happened

1. You created test versions to see how they looked
2. Old files weren't deleted from the repo
3. Some project pages still pointed to old index files
4. When editing, it was easy to edit the wrong file
5. Git tracked all versions, causing confusion

**Solution:** Single source of truth (index.html) + delete old files

---

**Created:** December 9, 2025
**Status:** Implementation Ready
**Next Step:** Delete old files and commit cleanup
