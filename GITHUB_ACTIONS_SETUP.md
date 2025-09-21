# 🚀 GitHub Actions Auto-Deployment Setup Guide

## Overview
This guide sets up automatic deployment to Google Cloud Run whenever you push code to the `main` branch. The GitHub Action will:

1. **Build a new container** from your latest code
2. **Replace the previous version** with zero downtime
3. **Keep the same URL** - no changes needed in your frontend
4. **Test the deployment** automatically
5. **Show deployment info** in the GitHub Actions log

## 🔧 Setup Instructions

### Step 1: Add GitHub Secret

1. **Go to your GitHub repository**: `https://github.com/arunpranav-at/VeriTrueAI2.0-Backend`

2. **Navigate to Settings** → **Secrets and variables** → **Actions**

3. **Click "New repository secret"**

4. **Set the secret:**
   - **Name:** `GCP_SA_KEY`
   - **Value:** Copy the ENTIRE content from the `github-actions-key.json` file that was generated during setup

   ⚠️ **SECURITY NOTE:** The service account key contains sensitive information including private keys. Never share this content publicly or commit it to version control.

5. **Click "Add secret"**

### Step 2: Commit and Push

1. **Add all files to git:**
   ```bash
   git add .
   git commit -m "Add GitHub Actions auto-deployment"
   git push origin main
   ```

2. **Watch the magic happen:**
   - Go to **Actions** tab in your GitHub repo
   - You'll see the deployment workflow running
   - It will take 2-3 minutes to complete

## 🎯 How It Works

### Automatic Deployment Process:

1. **Trigger:** Push to `main` branch (ignores README/docs changes)
2. **Build:** Creates new Docker container with your latest code
3. **Deploy:** Replaces the old version on Cloud Run
4. **Test:** Automatically tests health and docs endpoints
5. **Report:** Shows deployment URLs and status

### Zero-Downtime Deployment:
- **Cloud Run handles traffic switching** seamlessly
- **Old version stays running** until new version is ready
- **Same URL maintained:** `https://veritrueai-backend-527144243268.us-central1.run.app`
- **No frontend changes needed**

### Version Management:
- **Previous versions are kept** for 30 days (configurable)
- **Rollback available** through Google Cloud Console
- **Traffic splitting possible** for A/B testing

## 🔍 Monitoring Deployments

### GitHub Actions:
- **View logs:** GitHub repo → Actions tab
- **See deployment status:** Green ✅ = success, Red ❌ = failed
- **Build time:** Typically 2-3 minutes

### Google Cloud Console:
- **Cloud Run service:** https://console.cloud.google.com/run
- **Deployment history:** Shows all revisions
- **Logs and metrics:** Real-time monitoring

## 🛠️ Customization Options

### Modify `.github/workflows/deploy.yml` to:

1. **Change resource limits:**
   ```yaml
   --memory 2Gi \
   --cpu 2 \
   ```

2. **Add environment variables:**
   ```yaml
   --set-env-vars="DEBUG=False,LOG_LEVEL=INFO" \
   ```

3. **Configure scaling:**
   ```yaml
   --min-instances 1 \
   --max-instances 20 \
   ```

4. **Add different branches:**
   ```yaml
   on:
     push:
       branches: [ main, staging, development ]
   ```

## 🚨 Troubleshooting

### Common Issues:

1. **Secret not found:**
   - Check `GCP_SA_KEY` is added to GitHub secrets
   - Ensure entire JSON is copied correctly

2. **Permission denied:**
   - Service account has required roles (already set up)
   - Check project ID is correct in workflow

3. **Build fails:**
   - Check Dockerfile syntax
   - Ensure requirements.txt is valid

4. **Deployment fails:**
   - Check Cloud Run quotas
   - Verify service name is unique

## 📋 Summary

✅ **Service Account Created:** `github-actions@veritrueai.iam.gserviceaccount.com`
✅ **Permissions Granted:** Cloud Run Admin, Storage Admin, Cloud Build
✅ **GitHub Workflow:** `.github/workflows/deploy.yml` 
✅ **Auto-deployment:** Triggered on push to main

### Your API will remain at:
🌐 **https://veritrueai-backend-527144243268.us-central1.run.app**

Every time you push code, this URL will serve your latest version automatically! 🚀