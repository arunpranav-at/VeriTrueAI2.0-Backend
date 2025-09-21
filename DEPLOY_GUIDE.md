# Google Cloud Deployment Guide

## Quick Deployment

Run the automated deployment script:

```powershell
.\deploy-gcloud.ps1 -ProjectId "veritrueai" -All
```

This will:
1. Set up secrets in Google Secret Manager
2. Deploy your app to App Engine
3. Test the deployment

## Manual Steps (if needed)

### 1. Set Project and Enable APIs
```bash
gcloud config set project veritrueai
gcloud services enable secretmanager.googleapis.com
gcloud services enable appengine.googleapis.com
```

### 2. Create Secrets in Secret Manager
```bash
# Create Gemini API Key secret
echo "your-gemini-api-key" | gcloud secrets create GEMINI_API_KEY --data-file=-

# Create Search API Key secret (optional)
echo "your-search-api-key" | gcloud secrets create SEARCH_API_KEY --data-file=-

# Create JWT Secret Key
echo "your-secret-jwt-key" | gcloud secrets create SECRET_KEY --data-file=-
```

### 3. Deploy to App Engine
```bash
gcloud app deploy app.yaml
```

## Security Features

✅ **Secrets Protection**: All sensitive data stored in Secret Manager
✅ **CORS Security**: Only your specified origins allowed
✅ **HTTPS Enforced**: All traffic uses secure connections
✅ **Private Access**: Secrets not accessible in app.yaml or logs

## Your CORS Configuration

The backend will only accept requests from:
- `http://localhost:3000` (local development)
- `http://localhost:3001` (local development)
- `https://veritrueai-frontend-o5oapa7v5q-uc.a.run.app` (production frontend)

## Testing Your Deployment

After deployment, test these endpoints:
- Health Check: `https://veritrueai.uc.r.appspot.com/health`
- API Docs: `https://veritrueai.uc.r.appspot.com/docs`
- Analysis: `https://veritrueai.uc.r.appspot.com/api/v1/analyze/`

## Monitoring

View logs:
```bash
gcloud app logs tail -s default
```

View metrics in Google Cloud Console → App Engine → Services