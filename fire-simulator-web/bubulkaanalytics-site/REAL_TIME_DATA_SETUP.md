# Little Falls Dashboard - Real-Time Data Integration

## Overview

The Little Falls Safety Analysis Dashboard has been updated to fetch **real-time USGS water data** instead of displaying static/hardcoded values. This document explains the three implementations and how to deploy them.

## Three Dashboard Versions

### 1. **potomac_dashboard_live.html** - Direct USGS API (Recommended for Direct Deployment)
- **Direct USGS API calls** from JavaScript
- No proxy needed
- Simple deployment - just upload the HTML file
- **Best for:** Local testing and simple deployments
- **Limitation:** May have CORS issues depending on browser/host

**Usage:**
```
https://bubulkaanalytics.com/potomac_dashboard_live.html
```

### 2. **potomac_dashboard_hybrid.html** - Dual-Source with Fallback (Recommended for Netlify)
- **Primary:** Direct USGS API (faster, no proxy latency)
- **Fallback:** Netlify Function proxy (if direct fails)
- **Final Fallback:** Reference/demo data (if both fail)
- **Best for:** Netlify deployment with reliability
- Automatically detects which source was used and displays in UI
- Graceful degradation if USGS API is temporarily unavailable

**Usage:**
```
https://bubulkaanalytics.com/potomac_dashboard_hybrid.html
```

### 3. **Netlify Function: `/netlify/functions/fetch-usgs.js`** - Proxy Backend
- Backend proxy for USGS API calls
- Eliminates CORS issues
- 15-minute response caching
- Built-in error handling

**Function Endpoint:**
```
/.netlify/functions/fetch-usgs?siteNumber=01646500&days=7
```

## Current Status

The old hardcoded dashboard remains as **potomac_dashboard.html** (for reference/backup).

## Deployment Instructions

### For Netlify Deployment (Recommended)

1. **Ensure directory structure:**
```
bubulkaanalytics-site/
├── netlify/
│   └── functions/
│       └── fetch-usgs.js         ✓ Already created
├── netlify.toml                   ✓ Already configured
├── potomac_dashboard_hybrid.html  ✓ Use this version
└── potomac_dashboard.html         (Keep as backup)
```

2. **Update portfolio link in index-professional.html:**
   - Find: `<a href="potomac_dashboard.html" class="project-link">View Dashboard</a>`
   - Replace with: `<a href="potomac_dashboard_hybrid.html" class="project-link">View Dashboard</a>`

3. **Deploy to Netlify:**
   ```bash
   cd d:\projects\shipboard-fire-response\web\bubulkaanalytics-site
   git add .
   git commit -m "Add real-time USGS data integration with Netlify Functions"
   git push origin main
   ```

4. **Verify on Netlify dashboard:**
   - Check that `Functions` section shows `fetch-usgs` deployed
   - Test the dashboard at `https://bubulkaanalytics.com/potomac_dashboard_hybrid.html`

### For Local Testing

```html
<!-- Open in browser during development -->
file:///D:/projects/shipboard-fire-response/web/bubulkaanalytics-site/potomac_dashboard_live.html
```

## Data Flow

### Hybrid Version (Recommended)
```
┌─ Page Load ─┐
│             ↓
│      Try Direct USGS API
│      waterdata.usgs.gov/nwis/iv/
│             │
│      ┌──Yes├─ Use Direct Data ✓
│      │     │
│      No    │
│      ↓     │
│   Try Netlify Function
│   /.netlify/functions/fetch-usgs
│      │     │
│  ┌───Yes───┤─ Use Proxy Data ✓
│  │   │     │
│  │   No    │
│  │   ↓     │
│  │  Use Reference/Demo Data ✓
│  │   │     │
│  └───────────┘
│
└─ Update Dashboard ─┐
                     ↓
   Display current flow, safety score,
   forecasts, and data source indicator
```

## USGS Data Sources

**Station Used:** 01646500 - Potomac River at Little Falls Lock, MD
- **Parameter:** Discharge (00060) in cubic feet per second (cfs)
- **Data Type:** Real-time (updated every 15 minutes)
- **API:** USGS Water Services (waterdata.usgs.gov)
- **No authentication required:** Public API

**Optional Upstream Stations (Future Enhancement):**
- 01638500 - Point of Rocks, MD
- 01636500 - Harpers Ferry, WV (Potomac + Shenandoah)

## Technical Details

### Chart.js Initialization
- Charts update dynamically with fresh data
- Automatic resize when tab switches
- Safety score calculations based on flow rates
- 7-day linear trend forecasting

### Safety Score Algorithm
```
Safety Score = (Flow Component: 40%) + (Trend: 30%) + (Seasonal: 20%) + (Bonus: 10%)

Flow Component: Based on current flow vs. thresholds for Little Falls
Trend: 30 points if stable or improving
Seasonal: 20 points adjusted by month (spring high water, summer low, etc.)
Bonus: +10 points for experienced paddlers (adjustable)
```

### Data Caching
- **Direct API:** No caching (real-time)
- **Netlify Function:** 15-minute cache header (reduces USGS load)
- **Dashboard Refresh:** 15 minutes (configurable)

## Error Handling

The hybrid dashboard includes comprehensive error handling:

1. **Direct API Timeout:** Falls back to Netlify Function (2-5 second delay)
2. **Netlify Function Unavailable:** Uses cached reference data
3. **All Services Fail:** Displays error banner but continues with realistic demo data
4. **UI Updates:** Shows which data source is being used (Direct/Netlify/Reference)

## Removing ARIMA References

The README and methodology have been updated to reference "Linear Trend Regression" instead of "ARIMA" modeling.

**Files Updated:**
- ✓ `D:\R projects\week 8\README.md` - Removed "ARIMA forecasting"
- ✓ Git repository updated and pushed to GitHub
- Remaining ARIMA references in presentation files (R Markdown, PowerPoint) are in documentation/archived materials

## Testing Checklist

- [ ] Dashboard loads without JavaScript console errors
- [ ] Real-time flow data displays correctly
- [ ] Charts render with forecast data
- [ ] Data refreshes every 15 minutes
- [ ] Netlify Function endpoint works: `/.netlify/functions/fetch-usgs`
- [ ] Error banner shows when data source changes
- [ ] Tab switching resizes charts properly
- [ ] Mobile responsive design works
- [ ] Portfolio link navigates correctly
- [ ] "Back to Portfolio" button works

## Future Enhancements

1. **Upstream Gauge Correlation:** Add Point of Rocks and Harpers Ferry validation
2. **ARIMA Enhancement:** Replace linear trend with ARIMA for 7+ day forecasts
3. **Weather Integration:** Add weather data API for improved predictions
4. **Historical Comparison:** Show same date/flow from previous years
5. **Alert System:** Notify when flow reaches critical thresholds
6. **Analytics:** Track dashboard views and user interactions

## Troubleshooting

### Dashboard shows "Loading..." indefinitely
- Check browser console for errors
- Verify Netlify Function is deployed
- Ensure USGS API is accessible

### Data appears outdated
- USGS updates every 15 minutes (check timestamp)
- Dashboard auto-refreshes every 15 minutes
- Manually refresh browser to force update

### Netlify Function returns 500 error
- Check Netlify function logs: `Netlify UI → Functions → fetch-usgs → Logs`
- Verify Node.js version in `netlify.toml`
- Check fetch URL syntax

### CORS errors in console
- This is normal for direct USGS calls from some browsers
- Hybrid version automatically falls back to Netlify Function
- No action needed

## Support & Questions

Refer to:
- USGS API Documentation: https://waterservices.usgs.gov/
- Netlify Functions: https://docs.netlify.com/functions/overview/
- Chart.js Documentation: https://www.chartjs.org/
