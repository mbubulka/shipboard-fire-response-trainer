# Quick Start - Preview Professional Portfolio Locally

## The Fast Track (2 minutes)

### On Windows PowerShell:

```powershell
# Navigate to your project directory
cd "d:\projects\shipboard-fire-response\web\bubulkaanalytics-site"

# Start a local web server
python -m http.server 8000

# Then open your browser to:
# http://localhost:8000/index-professional.html
```

**In your browser:**
- Visit: `http://localhost:8000/index-professional.html` (main portfolio)
- Then visit: `http://localhost:8000/firetrainer-professional.html` (fire trainer)

---

## Testing Checklist

### Homepage (index-professional.html)
- [ ] Profile image displays
- [ ] Navigation links scroll smoothly
- [ ] "View Projects" button scrolls to projects section
- [ ] "Get In Touch" button scrolls to contact
- [ ] Skills section shows all 4 categories
- [ ] Projects show 3 project cards with descriptions
- [ ] Stats section displays properly
- [ ] Contact information shows email, GitHub, LinkedIn links
- [ ] Resize browser window - layout adapts smoothly
- [ ] Open DevTools (F12) and set to mobile view - responsive design works

### Fire Trainer Page (firetrainer-professional.html)
- [ ] "← Back to Portfolio" link works
- [ ] Page displays training scenarios
- [ ] Click "Begin Training" on any scenario
- [ ] Questions display with options
- [ ] Select an answer - feedback appears
- [ ] Quiz presents question 2
- [ ] "Reset Training" button works
- [ ] Responsive - works on mobile view

---

## Mobile Testing

### Desktop DevTools Method (Recommended):
1. Open the page in Chrome
2. Press `F12` to open DevTools
3. Click the mobile icon (top-left of DevTools, looks like 📱)
4. Select "iPhone 12 Pro" from dropdown
5. Test all navigation, buttons, and scroll behavior

### Real Mobile Device:
1. Find your computer's IP address:
   ```powershell
   ipconfig
   # Look for "IPv4 Address" (usually 192.168.x.x)
   ```
2. On your phone, open: `http://YOUR_IP:8000/index-professional.html`
3. Test all touch interactions and layout

---

## Customization Before Deployment

### Critical Updates Needed:

1. **Email Address** (2 places):
   - Homepage: Contact section
   - Fire trainer page: Contact info
   - Replace: `mbubulka@example.com`

2. **Social Links** (2 places):
   - Homepage: Contact section + GitHub links in projects
   - Replace: `https://github.com/mbubulka` with your actual GitHub

3. **Profile Image**:
   - File: `Michael_9028-Bkgd-square.jpg` must exist in the directory
   - If you want a different image, replace or update the filename

4. **Project Links**:
   - Verify links point to correct pages:
     - Fire Trainer: `firetrainer/comprehensive.html`
     - River Flow: `potomac_dashboard.html`
     - Analytics: `analytics-dashboard.html`

5. **Statistics** (optional):
   - Update numbers to match your actual metrics:
     ```html
     50K+ Data Points Analyzed
     3+ Production Systems
     98% Model Accuracy
     12 GitHub Projects
     ```

---

## Design Features to Notice

### Professional Elements:
✓ **No emojis** - Replaced with professional headers and typography
✓ **Color scheme** - Deep professional blues (trust, stability, competence)
✓ **Clean layout** - Proper whitespace and visual hierarchy
✓ **Typography** - System fonts, readable sizing, consistent hierarchy
✓ **Responsive** - Works perfectly on desktop, tablet, mobile
✓ **Modern** - Current design standards and best practices
✓ **Accessible** - High contrast, proper semantic HTML

### Brand Message:
- **Hero**: Clear statement of role and value
- **About**: Military background + data science transition
- **Skills**: Organized by category (Languages, Data, ML, Specializations)
- **Projects**: Technical depth with real-world impact
- **Contact**: Multiple touchpoints for accessibility

---

## Comparison: Old vs. New

| Feature | Old | New |
|---------|-----|-----|
| Emojis | Many (🔥⚡📊) | None (professional headers) |
| Colors | Bright, multiple gradients | Professional blue palette |
| Tone | Casual/energetic | Professional/technical |
| Mobile | Basic | Fully responsive |
| Navigation | Unclear | Clear, sticky header |
| Fonts | Variable | System fonts, consistent |
| Spacing | Dense | Whitespace-rich |
| Professionalism | Medium | High |

---

## Troubleshooting

### Problem: Profile image not showing
**Solution**: 
- Ensure `Michael_9028-Bkgd-square.jpg` is in the same directory as `index-professional.html`
- Check image file name is exactly correct (case-sensitive)

### Problem: Styles not loading correctly
**Solution**:
- Make sure you're using a web server (not file://)
- Try: `python -m http.server 8000`
- Then visit: `http://localhost:8000/index-professional.html`
- Clear browser cache: `Ctrl+Shift+Del` (all files)

### Problem: Links not working
**Solution**:
- Ensure all referenced files exist (`potomac_dashboard.html`, etc.)
- Update GitHub URLs to your actual profile
- Test relative paths from the current directory

### Problem: Layout broken on mobile
**Solution**:
- Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- Test in DevTools mobile view, not just browser resize
- Check all CSS media queries load (check DevTools console for errors)

---

## Next Steps

### If You Like the Design:
1. Customize contact information
2. Update profile image if desired
3. Verify all project links
4. Test on mobile device
5. Get feedback from 3-5 people
6. Backup current pages
7. Deploy to GitHub

### If You Want Changes:
1. Note specific areas to modify
2. Update HTML content or colors
3. Test changes locally
4. Iterate until satisfied
5. Then deploy

### Deployment (When Ready):
```powershell
# Backup current pages
Rename-Item index.html index-backup.html

# Deploy new version
Rename-Item index-professional.html index.html

# Commit and push
git add -A
git commit -m "Deploy professional portfolio redesign"
git push origin main

# Netlify will auto-deploy from GitHub
```

---

## File Locations

```
d:\projects\shipboard-fire-response\web\bubulkaanalytics-site\
├── index-professional.html ← MAIN PORTFOLIO (preview here)
├── firetrainer-professional.html ← FIRE TRAINER (preview here)
├── index.html ← Current (keep as backup)
├── firetrainer\
│   └── comprehensive.html ← Current fire trainer
├── Michael_9028-Bkgd-square.jpg ← Your profile image
├── potomac_dashboard.html ← River flow predictor
├── analytics-dashboard.html ← Analytics dashboard
├── REDESIGN_README.md ← Setup instructions
└── DESIGN_RATIONALE.md ← Design philosophy
```

---

## Questions?

Refer to:
- **REDESIGN_README.md** - Detailed setup and testing guide
- **DESIGN_RATIONALE.md** - Design decisions and philosophy
- **Browser DevTools** (F12) - Check console for errors, test responsiveness

---

## Summary

1. **To preview**: `python -m http.server 8000` → `http://localhost:8000/index-professional.html`
2. **To test mobile**: Press F12, click mobile icon, resize window
3. **To customize**: Update email, links, profile image
4. **To deploy**: Backup current, rename professional versions, commit & push
5. **To iterate**: Make changes, test, gather feedback, repeat

**You're ready to go!** 🚀

---

*Professional portfolio redesigned with military-grade precision and data science credibility.*
