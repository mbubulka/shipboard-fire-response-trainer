# Military Salary Estimator → GitHub → Netlify Deployment Plan

## Phase 1: GitHub Deployment (Immediate)

### Step 1: Create GitHub Repository
```bash
# GitHub Web Interface
Go to https://github.com/new
- Repository name: military-salary-estimator
- Description: GLM-based salary predictor for military-to-civilian transitions (96% accuracy)
- Visibility: Public
- Do NOT initialize with README (you have one)
- Click "Create repository"
```

### Step 2: Push to GitHub
```bash
cd "d:\R projects\week 15\Presentation Folder"

# Initialize git if not already done
git init
git config user.email "your-email@example.com"
git config user.name "Your Name"

# Add all files
git add .
git commit -m "Initial commit: Military-to-Civilian Salary Estimator with Shiny dashboard"

# Add remote and push
git remote add origin https://github.com/mbubulka/military-salary-estimator.git
git branch -M main
git push -u origin main
```

### Step 3: Verify on GitHub
- Check https://github.com/mbubulka/military-salary-estimator
- Confirm README displays correctly
- Verify archive folders are NOT present
- Test clone functionality

---

## Phase 2: Integrate with bubulkaanalytics.com

### Step 1: Create Project Directory in bubulkaanalytics Site

```bash
cd "d:\projects\shipboard-fire-response\web\bubulkaanalytics-site"

# Create projects directory structure
mkdir -p projects\military-salary-estimator
mkdir -p projects\military-salary-estimator\docs
mkdir -p projects\military-salary-estimator\assets
```

### Step 2: Create Project Hub Page

Create `projects\military-salary-estimator\index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Military Salary Estimator - Bubulka Analytics</title>
    <link rel="stylesheet" href="../../style.css">
    <style>
        .project-hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem 1rem;
            text-align: center;
        }
        .project-content {
            max-width: 1000px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }
        .stat-card {
            background: #f5f5f5;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="../../">← Back to Bubulka Analytics</a>
        </nav>
    </header>

    <div class="project-hero">
        <h1>Military-to-Civilian Salary Estimator</h1>
        <p>AI-powered salary prediction model for military personnel entering the civilian workforce</p>
    </div>

    <div class="project-content">
        <h2>Project Overview</h2>
        <p>
            A generalized linear model predicting civilian salary outcomes for military service members.
            Trained on 3,589 real military-to-civilian transitions with 96% accuracy.
        </p>

        <div class="stats">
            <div class="stat-card">
                <h3>96%</h3>
                <p>Model Accuracy (R² = 0.9627)</p>
            </div>
            <div class="stat-card">
                <h3>3,589</h3>
                <p>Training Records</p>
            </div>
            <div class="stat-card">
                <h3>±$3,246</h3>
                <p>Prediction Error (MAE)</p>
            </div>
            <div class="stat-card">
                <h3>Live</h3>
                <p>Interactive Shiny Dashboard</p>
            </div>
        </div>

        <h2>Quick Links</h2>
        <ul>
            <li><a href="https://github.com/yourusername/military-salary-estimator" target="_blank">
                📊 GitHub Repository
            </a></li>
            <li><a href="https://github.com/yourusername/military-salary-estimator#quick-start" target="_blank">
                🚀 Quick Start Guide
            </a></li>
            <li><a href="https://github.com/yourusername/military-salary-estimator/blob/main/README.md" target="_blank">
                📖 Full Documentation
            </a></li>
            <li><a href="http://127.0.0.1:8100" target="_blank">
                💻 Live Dashboard (local run)
            </a></li>
        </ul>

        <h2>Key Features</h2>
        <ul>
            <li>✅ <strong>High Accuracy:</strong> R² = 0.9627 on independent test set</li>
            <li>✅ <strong>Interpretable:</strong> GLM coefficients explain salary drivers</li>
            <li>✅ <strong>Interactive:</strong> Shiny dashboard for real-time salary estimation</li>
            <li>✅ <strong>Reproducible:</strong> Full pipeline with cross-validation</li>
            <li>✅ <strong>Open Source:</strong> MIT licensed, code available on GitHub</li>
        </ul>

        <h2>Technical Stack</h2>
        <ul>
            <li><strong>Algorithm:</strong> Generalized Linear Model (GLM)</li>
            <li><strong>Language:</strong> R 4.0+</li>
            <li><strong>Dashboard:</strong> Shiny interactive web framework</li>
            <li><strong>Data:</strong> 3,589 military-to-civilian transitions</li>
            <li><strong>Accuracy:</strong> 96.27% variance explained</li>
        </ul>

        <h2>Model Insights</h2>
        <p>
            Military rank explains 95%+ of salary variation in civilian employment,
            reflecting direct salary-based rank correspondence and career progression alignment.
        </p>

        <h2>Getting Started</h2>
        <ol>
            <li>Clone the repository from GitHub</li>
            <li>Install R dependencies: <code>source("requirements.R")</code></li>
            <li>Launch the dashboard: <code>runApp("10_shiny_dashboard/app_simple.R", port = 8100)</code></li>
            <li>Explore the data pipeline in <code>02_code/</code></li>
        </ol>

        <h2>Project Details</h2>
        <p>
            This project demonstrates end-to-end data science methodology from data acquisition and cleaning
            through exploratory analysis, feature engineering, model development, cross-validation, and deployment
            as an interactive web application.
        </p>
        <p>
            The model helps military service members understand expected civilian salary outcomes based on rank,
            years of service, occupational specialty, and industry type.
        </p>

        <h2>License & Attribution</h2>
        <p>
            This project is licensed under the MIT License. 
            <a href="https://github.com/yourusername/military-salary-estimator" target="_blank">
                View on GitHub
            </a>
        </p>
    </div>
</body>
</html>
```

### Step 3: Create Project Navigation Update

Update `index.html` in bubulkaanalytics-site to include link to new project:

```html
<!-- Add to projects section -->
<a href="projects/military-salary-estimator/index.html" class="project-card">
    <h3>Military Salary Estimator</h3>
    <p>96% accurate GLM model predicting military-to-civilian salary transitions</p>
    <span class="tag">Data Science</span>
    <span class="tag">R Shiny</span>
</a>
```

---

## Phase 3: Netlify Deployment

### Step 1: Create Netlify Configuration

Create `netlify.toml` in bubulkaanalytics-site root:

```toml
# Netlify Configuration for bubulkaanalytics-site

[build]
  command = "echo 'Static site - no build required'"
  publish = "."

[build.environment]
  NODE_VERSION = "18"

# Redirect rules for SPA behavior
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

# Cache headers
[[headers]]
  for = "/*"
  [headers.values]
    Cache-Control = "public, max-age=3600"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000"

[[headers]]
  for = "*.html"
  [headers.values]
    Cache-Control = "public, max-age=3600"
```

### Step 2: Create _redirects File

Create `_redirects` in bubulkaanalytics-site root:

```
# Netlify redirects for single-page applications
/*  /index.html  200

# Project pages
/projects/military-salary-estimator/*  /projects/military-salary-estimator/index.html  200

# External redirects
/github  https://github.com/yourusername/military-salary-estimator  301
/salary-estimator-repo  https://github.com/yourusername/military-salary-estimator  301
```

### Step 3: Push to GitHub

```bash
cd "d:\projects\shipboard-fire-response\web\bubulkaanalytics-site"

git add .
git commit -m "Add Military Salary Estimator project to portfolio"
git push origin main
```

### Step 4: Deploy to Netlify

#### Option A: Connect GitHub to Netlify (Recommended)

1. Go to https://app.netlify.com/signup
2. Sign in with GitHub
3. Click "New site from Git"
4. Select "GitHub"
5. Choose the `shipboard-fire-response` repository
6. Configure:
   - **Base directory:** `web/bubulkaanalytics-site`
   - **Build command:** (leave blank - static site)
   - **Publish directory:** `.` (root of site folder)
7. Deploy!

#### Option B: Manual Deploy

```bash
# Install Netlify CLI (if not already installed)
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from bubulkaanalytics-site directory
cd "d:\projects\shipboard-fire-response\web\bubulkaanalytics-site"
netlify deploy --prod --dir=.
```

### Step 5: Configure Custom Domain

In Netlify Dashboard:
1. Go to **Site settings** → **Domain management**
2. Add custom domain: `bubulkaanalytics.com`
3. Configure DNS records at your domain registrar
4. Enable HTTPS (automatic with Netlify)

---

## Phase 4: Verification & Testing

### Before Going Live

- [ ] GitHub repo is public and accessible
- [ ] README displays correctly on GitHub
- [ ] bubulkaanalytics site builds without errors
- [ ] Project page links to GitHub repo
- [ ] All assets load correctly
- [ ] Netlify deployment successful
- [ ] Custom domain points to Netlify
- [ ] HTTPS enabled
- [ ] Mobile responsive design verified

### Test Links

After deployment, verify:
- [ ] https://bubulkaanalytics.com/ loads
- [ ] https://bubulkaanalytics.com/projects/military-salary-estimator/ displays project
- [ ] GitHub links work
- [ ] All images and styles load
- [ ] No console errors

---

## Quick Reference Commands

### GitHub Push
```bash
cd "d:\R projects\week 15\Presentation Folder"
git add .
git commit -m "Message"
git push origin main
```

### Netlify Deploy (CLI)
```bash
cd "d:\projects\shipboard-fire-response\web\bubulkaanalytics-site"
netlify deploy --prod --dir=.
```

### Update After Changes
```bash
cd "d:\projects\shipboard-fire-response\web\bubulkaanalytics-site"
git add .
git commit -m "Update portfolio"
git push origin main
# Auto-deploys if connected to Netlify
```

---

## Support & Questions

**GitHub Issues:** Use GitHub Issues tab for bug reports  
**Netlify Status:** Check https://app.netlify.com for deployment status  
**Domain Issues:** Check DNS propagation at https://dnschecker.org  

---

**Status:** Ready for Phase 1 (GitHub Push)  
**Next Step:** Create GitHub repository and run push commands  
**Timeline:** ~30 minutes for full deployment  

