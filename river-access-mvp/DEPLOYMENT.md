# Deployment Guide

This guide covers deploying River Access MVP to production using Railway or Render.

---

## Prerequisites

- GitHub account with repository pushed
- (Optional) Custom domain `bubulkaanalytics.com`
- (Optional) PlanetScale account for cloud MySQL

---

## Option 1: Railway (Recommended)

Railway makes it simple to deploy Docker Compose apps. Estimated cost: $30-50/month

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project

### Step 2: Connect GitHub Repository

1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub"
3. Connect your GitHub account
4. Select `river-access-mvp` repository

### Step 3: Configure Environment

Railway auto-detects `docker-compose.yml`. Set environment variables:

```bash
MYSQL_ROOT_PASSWORD=<secure-password>
MYSQL_USER=river_user
MYSQL_PASSWORD=<secure-password>
MYSQL_DATABASE=river_access
DATABASE_URL=mysql+pymysql://river_user:<password>@mysql:3306/river_access
API_URL=http://python-api:8000
```

### Step 4: Add MySQL Service

1. In Railway dashboard, add service from marketplace
2. Select "MySQL"
3. Railway automatically configures DATABASE_URL

### Step 5: Deploy

1. Click "Deploy"
2. Railway builds Docker images
3. Services start in ~5 minutes
4. View logs to verify startup

### Step 6: Get Public URL

- Railway provides URL like `https://river-access-mvp.railway.app`
- Copy this URL

### Step 7: Configure Custom Domain

1. Buy domain `bubulkaanalytics.com` (Namecheap, GoDaddy, etc.)
2. In Railway project settings → Domains
3. Add `bubulkaanalytics.com`
4. Follow Railway instructions to add DNS records
5. Propagation takes 24-48 hours

---

## Option 2: Render.com

Render has a free tier but with limitations. Similar to Railway workflow.

### Quick Steps

1. Go to [render.com](https://render.com)
2. Connect GitHub
3. Create new "Web Service" from repo
4. Point to `docker-compose.yml`
5. Add MySQL service from marketplace
6. Deploy
7. Configure custom domain in Settings

---

## Database Considerations

### Option A: Cloud MySQL (Recommended)

Use PlanetScale (MySQL-compatible, generous free tier):

1. Create PlanetScale account
2. Create database
3. Get connection string
4. Update `DATABASE_URL` in Railway/Render

### Option B: Platform-provided MySQL

- Railway: Add MySQL from marketplace
- Render: Add MySQL from marketplace
- Database is auto-backed up

---

## Environment Variables for Production

Update `.env` before deployment:

```bash
# Use strong passwords
MYSQL_ROOT_PASSWORD=<strong-random-password>
MYSQL_PASSWORD=<strong-random-password>

# Point to cloud services
DATABASE_URL=mysql+pymysql://river_user:PASSWORD@HOST:3306/river_access
API_URL=https://bubulkaanalytics.com  # Update after domain setup

# Optional: Add real API keys for production
USGS_API_KEY=<if-needed>
```

---

## Monitoring & Logs

### Railway
```bash
# View real-time logs
railway logs --follow
```

### Render
- Logs visible in dashboard
- Email alerts available

---

## Troubleshooting

### Database connection errors
- Verify DATABASE_URL is correct
- Check MySQL service is running
- Ensure credentials match

### Streamlit can't reach API
- Verify API service is running
- Check API_URL environment variable
- API should be `http://python-api:8000` for internal communication

### High memory usage
- Reduce ARIMA model frequency
- Scale to more memory ($5 → $10/month tier)

---

## Cost Breakdown

### Railway (Monthly Estimate)

| Service | Cost |
|---------|------|
| Streamlit container | $10-15 |
| FastAPI container | $5-10 |
| MySQL database | $10-15 |
| Domain (annual) | $12 |
| **Total** | **$35-50/month** |

### Render (Monthly Estimate)

Similar pricing, free tier available with limitations.

---

## Scaling

As traffic increases:

1. **Increase container memory** (via Railway/Render settings)
2. **Add database replicas** (PlanetScale feature)
3. **Enable caching** (add Redis)
4. **CDN for static assets** (CloudFlare, AWS CloudFront)

---

## Security Best Practices

1. **Never commit `.env`** - Use `.env.example` only
2. **Rotate credentials regularly**
3. **Use HTTPS only** (automatic with Railway/Render)
4. **Enable database backups**
5. **Monitor error logs for security issues**

---

## CI/CD Pipeline

For automatic deployments on GitHub push:

### Railway
- Automatic deployments on GitHub push (default)
- Rollback available via dashboard

### Render
- Configure auto-deploy in settings
- Link to GitHub branch

---

## Domain Setup

### After deployment to Railway/Render:

1. Get the platform's DNS records
2. Go to your domain registrar (Namecheap, GoDaddy)
3. Update DNS to point to Railway/Render
4. Wait 24-48 hours for propagation
5. Access via `https://bubulkaanalytics.com`

---

## Backup Strategy

### Database Backups
- Railway: Auto-backs up MySQL daily
- PlanetScale: Automatic backups, point-in-time recovery

### Code Backups
- GitHub is your code backup
- Tag releases for production versions

---

## Performance Optimization

### Streamlit
- Enable caching for frequently accessed data
- Use `@st.experimental_singleton` for model reuse

### FastAPI
- Add response caching headers
- Use database indexes (already configured)
- Consider Redis for session caching

### Database
- Analyze slow queries: `EXPLAIN SELECT ...`
- Add indexes on frequently filtered columns
- Archive old data after 1 year

---

## Next Steps

1. ✅ Verify local deployment works
2. ✅ Push code to GitHub
3. ✅ Create Railway account
4. ✅ Deploy via Railway
5. ✅ Test all features in production
6. ✅ Configure custom domain
7. ✅ Update portfolio with live link
8. ✅ Share with potential employers

---

## Support & Debugging

### Railway Support
- Dashboard troubleshooting
- Email support for paid plans

### Render Support
- Documentation at render.com/docs
- Email support

### Common Issues

**"Connection refused"**
- Containers still starting up
- Wait 2-3 minutes and refresh

**"502 Bad Gateway"**
- FastAPI backend crashed
- Check logs for errors
- Restart service

**"Database unavailable"**
- MySQL container initializing
- Check MySQL logs
- May take 30 seconds on first start

---

## Portfolio Benefits

Deploying to production shows employers you can:
- ✅ Deploy containerized applications
- ✅ Manage cloud infrastructure
- ✅ Handle production databases
- ✅ Monitor and troubleshoot real systems
- ✅ Implement DevOps workflows

Perfect talking points for interviews!
