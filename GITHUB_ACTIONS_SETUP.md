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
   - **Value:** Copy the ENTIRE content from `github-actions-key.json` file

   ```json
   {
     "type": "service_account",
     "project_id": "veritrueai",
     "private_key_id": "5a638328fcf467c5260798762277b8e5de0c0355",
     "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDZ/fK93n7lbPlj\nI9X0e3g0ghD5gyN7LBwVvyYTcQLMy2DpdQFwJKY95ObyRZBvpgmwgVgSa3Xte9uI\nNXYAVB89YYulsz93rbybwUfoWLaVx1bLB9AopZnYV+JuwbNBp4UCI0XNw4OA+RtB\nk3VYgK2i9D0boAbOXl+8qvXFz2If1JOWWELEkGFeXZuIa4BepecJnAmwCo7Uxzc5\nBEtDpx1nhklBb+2XZSUih4elEEmOUEsvYNNFygJHFgc9cYvepQ17hTkv1HsYCOee\nu487gSo962BF3ZfLdAKFfbvh4n1cmMs8Tghg77ZXdt35yMJPVNhVe0IBRnb0P/j4\nvLPG83njAgMBAAECggEAAa4ERdRGFAx/63SmPGkLJxRtfw60oklXug8sAvBW/i7/\nAy2EolGV+loeMXW5xDJ6VqLYg+PSF89hhK4sx5neV8G9qrwz2/85udWGcVLlrUfI\n8m2P/BAynEkpFINnlzTsQHT3H7vG8qJ4xEuXluP+8oeBRQo5ozN092Y12J1dezNL\nfebJ3WNByDXvuz/EmkGdqT2n7Hp4JhjURRQmV57lPS32coIV6Q7IQdgsD7Z8WDTn\nH+sNZ6AToVD4+i33R1C57R2fjk6X46RJ8lT4YDPMt4cdzqfzjQiJgA5zpofRZw2U\nAYigJKEIOL2dVJDFwtEXI+8EZ8brQk9OHDGh8kwqAQKBgQD77weOQ9TDSMEhKmhZ\n7jDjak5F+HR3pexki3zIGT3RovhE68iYfl+Xd1edjNklf9UwCW8mVOhlB/SzXXoG\nAlor1QDYE0Omd2HFAE4kYQqCgAU5TwO+1xgA1dNj7NAEMrCaNTNlOcZqsHU9y9Nr\nSvZdoW5PMD3CCiqwT98o7fCy4wKBgQDdgqyT+E6KlYAehMr0v21zugKnxJE10Zc3\nGMkzL932DvipWvWxyxw0o12WAJ6GjpvjegE6B/S/hMf1gjaoMHDHXsLl9nhl/1vP\nrKnj7B37ue2WGPAMKYrhctuqFsyM/9du0Qyba4IVhqVUDHLkqLCfsnMtN8bJlSPF\nnlmrU6HNAQKBgHY2F0aCv2+OUMieHG6uHBRpSib8yLFnkn8vEDLX3TDjljjIpcwf\n5/yrS9oqP62fyMmMc7H5vz3AuOn8n4f4TJUqkgXRLDoM5DxKw1/AhOzs4wab87b1\nOFcT/edyM7z0h/cjpWUG8foXqDuBy0cZ2nXejGLt0NyeZp9qKt0KoJlfAoGBAInL\nABAMJs+OsGRLtvUJH80dqQkz/iC8gJSFlqOA41JtfcHcE3rGHoWgGld1iyepDtAy\n1RCEYnvA3aKbneSCPaXIDPWAnOTWNQa7IfPmrcApqOH2IV1vejVEfeEQza3oeNs2\nr+D+v60kVTQzikUzqqutFnjKeZ5saBRGrQEmxUABAoGBAI3An03kjisKxkreAUNB\nBMiqVfwnJjlBMGKJ48jvg8TYC8hG60wa8TSOBAQdYFdcfs4UdNPP2BKPueRSPdMc\nYyd0XeWdnP1klwXOpzUrOkO7xeaiirbw3XT3dwyZdp8UnarL+p1KrVasK1R51hPH\nX9K32AwRWU13I47MXRIA6Cff\n-----END PRIVATE KEY-----\n",
     "client_email": "github-actions@veritrueai.iam.gserviceaccount.com",
     "client_id": "111605996380684451819",
     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
     "token_uri": "https://oauth2.googleapis.com/token",
     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/github-actions%40veritrueai.iam.gserviceaccount.com",
     "universe_domain": "googleapis.com"
   }
   ```

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