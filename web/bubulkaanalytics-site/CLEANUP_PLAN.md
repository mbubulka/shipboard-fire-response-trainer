# 🧹 Bubulka Analytics Site Cleanup Plan

## Current Status
✅ **All files fixed for deployment - no external JavaScript dependencies**
✅ **Git commit completed with deployment fixes**

## Essential Production Files (KEEP)
```
📁 bubulkaanalytics-site/
├── index.html                    ✅ Main landing page
├── Michael_9028-Bkgd-square.jpg  ✅ Profile image for index
├── DEPLOYMENT_CHECKLIST.md       ✅ Deployment documentation
└── firetrainer/
    └── comprehensive.html         ✅ Main training app (linked from index)
```

## Development/Backup Files (SAFE TO REMOVE)

### Root Level - Development Files
- ❌ `api-test.html` - API testing file
- ❌ `comprehensive-fixed.html` - Backup/duplicate 
- ❌ `comprehensive.html` - Duplicate (firetrainer version is main)
- ❌ `feedback-test.html` - Development testing
- ❌ `fire-response-training.html` - Duplicate training file
- ❌ `netlify-diagnostic.html` - Deployment testing
- ❌ `test-simple.html` - Simple test file
- ❌ `working-fire-training.html` - Working/development file

### Root Level - External JS Files (No Longer Needed)
- ❌ `dca-feedback-integration.js` - Now embedded in HTML files
- ❓ `dca-knowledge-base.js` - Check if used by any pages
- ❓ `enhanced-dca-knowledge-base.js` - Check if used by any pages

### Firetrainer Folder Cleanup
- ❌ `comprehensive_backup.html` - Backup file
- ❌ `comprehensive_temp.html` - Temporary development file
- ❌ `dca-feedback-integration.js` - Duplicate external JS
- ❌ `debug-test.html` - Debug testing file
- ❌ `deploy-ready.html` - Development deployment test
- ❌ `index.html` - Unclear purpose, not linked
- ❌ `test-main.html` - Development test file
- ❌ `test-simple.html` - Development test file
- ❌ `archive/` folder - Contains 4 old HTML versions

### DCA-Training Folder
- ❓ `index.html` - Check if needed
- ✅ `training.html` - Working standalone training page

## Cleanup Options

### Option 1: Conservative Cleanup (Recommended)
- Create `/dev-backup/` folder
- Move all development files there
- Keep only essential production files in root

### Option 2: Archive and Clean
- Create archive with git tag before cleanup
- Delete development files completely
- Keep minimal production structure

### Option 3: Full Clean Production Deploy
- Create new `/production/` folder with only:
  - index.html
  - firetrainer/comprehensive.html  
  - Michael_9028-Bkgd-square.jpg
  - DEPLOYMENT_CHECKLIST.md

## Analysis Results

### Files Referenced by index.html:
- `firetrainer/comprehensive.html` ✅ (Main fire training link)
- `Michael_9028-Bkgd-square.jpg` ✅ (Profile image)

### Files That Are Self-Contained:
- All HTML files now have embedded JavaScript
- No external dependencies between files
- Each can work independently

### Estimated Space Savings:
- Development files: ~15-20 files
- Archive folder: 4 duplicate HTML files
- Unused JS files: 3 files
- Total cleanup: ~75% of files can be safely removed

## Recommended Action Plan

1. **Test Current Setup** - Verify firetrainer/comprehensive.html works perfectly
2. **Create Development Archive** - Move dev files to backup folder
3. **Clean Production Structure** - Keep only essential files
4. **Test Deployment** - Deploy clean version to verify nothing breaks
5. **Document Clean Structure** - Update deployment guide

## Next Steps
Choose your preferred cleanup option and I'll execute it safely with git backup.