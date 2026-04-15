# Deployment Guide - Church Management System API

## 🚀 Deploy to Render (Free)

### Step 1: Create a Render Account
1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### Step 2: Create a PostgreSQL Database
1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. **Name**: `churchms-db`
3. **Region**: Choose closest to your location
4. **PostgreSQL Version**: 13 or higher
5. Click **"Create Database"**
6. Copy the **Internal Database URL** (you'll need this)

### Step 3: Deploy the Web Service
1. Click **"New +"** → **"Web Service"**
2. **Connect a repository**: Select your `churchMSAPI` GitHub repo
3. **Settings**:
   - **Name**: `churchms-api`
   - **Region**: Same as database
   - **Branch**: `master`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

### Step 4: Set Environment Variables
In the Render dashboard, go to **Environment** and add:

```
SECRET_KEY=very_long_random_string_min_32_chars_change_this
SESSION_SECRET_KEY=another_very_long_random_string_min_32_chars
DATABASE_URL=postgresql://user:password@hostname:5432/dbname
JWT_EXPIRE_MINUTES=20
ENV=production
```

**Get the DATABASE_URL from Step 2 (Internal Database URL)**

### Step 5: Deploy
1. Click **"Create Web Service"**
2. Render will automatically deploy from your GitHub repository
3. Your API will be live at: `https://churchms-api.onrender.com`

---

## 🔄 Auto-Deployment from GitHub

After the initial setup:
- Every time you push to `master` branch, Render automatically redeploys
- View logs in the Render dashboard
- Rollback to previous versions if needed

---

## 🔐 Security Best Practices for Production

### ✅ DO:
- Use strong random secret keys (at least 32 characters)
- Use environment variables for all secrets
- Use HTTPS only
- Keep dependencies updated
- Use PostgreSQL (not SQLite)
- Enable CORS only for your domain
- Set `JWT_EXPIRE_MINUTES` appropriately

### ❌ DON'T:
- Hardcode secrets in code
- Commit `.env` file
- Use SQLite in production
- Allow all CORS origins (`*`)
- Use default/weak passwords

---

## 🛠️ Generate Strong Secret Keys

Run this in Python to generate random keys:

```python
import secrets
print(secrets.token_urlsafe(32))
print(secrets.token_urlsafe(32))
```

---

## 📊 Monitoring & Logs

In Render dashboard:
- **Logs**: View real-time application logs
- **Metrics**: CPU, Memory, Requests per second
- **Events**: Deployment history and errors

---

## 🔗 Custom Domain (Optional)

1. In Render dashboard → Settings
2. Add your custom domain
3. Update DNS records (Render will guide you)
4. Wait for SSL certificate (auto-generated)

---

## ❓ Common Issues

### Database Connection Error
- Verify `DATABASE_URL` is correct
- Check if PostgreSQL service is running
- Wait 60 seconds after creating the database

### Port Already in Use
- Render automatically assigns the port via `$PORT` variable
- Build command: `gunicorn main:app --bind 0.0.0.0:$PORT`

### Deployment Fails
- Check the build logs in Render dashboard
- Ensure `Procfile` is in root directory
- Ensure `requirements.txt` is in `backend/` folder

### Import Errors
- Make sure all imports use relative paths
- Check that `python-dotenv` is in requirements.txt

---

## 📝 Alternative Deployment Options

### Railway
- Similar to Render but more generous free tier
- Go to https://railway.app
- Connect GitHub → Deploy

### PythonAnywhere
- Beginner-friendly
- Free tier available
- Good for learning

### AWS/Google Cloud
- More powerful but steeper learning curve
- Not recommended for beginners

---

## 🎯 Next Steps After Deployment

1. Test API endpoints at `https://yourapi.onrender.com/docs`
2. Test admin dashboard at `https://yourapi.onrender.com/admin`
3. Update CORS origins if you build a frontend
4. Monitor logs regularly
5. Set up regular backups of PostgreSQL database

---

## 📞 Need Help?

- Render Docs: https://docs.render.com
- FastAPI Docs: https://fastapi.tiangolo.com
- Contact support