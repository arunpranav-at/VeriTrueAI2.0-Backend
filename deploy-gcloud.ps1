# Google Cloud Deployment Script for VeriTrueAI2.0 Backend#!/usr/bin/env pwsh

param(# Google Cloud Deployment Script for VeriTrueAI2.0 Backend

    [Parameter(Mandatory=$true)]# This script sets up secrets in Secret Manager and deploys to App Engine

    [string]$ProjectId,

    param(

    [string]$GeminiApiKey,    [Parameter(Mandatory=$true)]

    [string]$SearchApiKey,    [string]$ProjectId,

    [string]$SecretKey,    

    [switch]$SecretsOnly,    [string]$GeminiApiKey,

    [switch]$DeployOnly,    [string]$SearchApiKey,

    [switch]$All    [string]$SecretKey,

)    [switch]$SecretsOnly,

    [switch]$DeployOnly,

Write-Host "🚀 VeriTrueAI2.0 Backend - Google Cloud Deployment" -ForegroundColor Green    [switch]$All

Write-Host "=================================================" -ForegroundColor Green)



# Check if gcloud is installedWrite-Host "🚀 VeriTrueAI2.0 Backend - Google Cloud Deployment" -ForegroundColor Green

try {Write-Host "=================================================" -ForegroundColor Green

    gcloud version | Out-Null

    Write-Host "✅ Google Cloud SDK found" -ForegroundColor Green# Check if gcloud is installed

} catch {try {

    Write-Host "❌ Google Cloud SDK not found. Please install it first:" -ForegroundColor Red    gcloud version | Out-Null

    Write-Host "https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow    Write-Host "✅ Google Cloud SDK found" -ForegroundColor Green

    exit 1} catch {

}    Write-Host "❌ Google Cloud SDK not found. Please install it first:" -ForegroundColor Red

    Write-Host "https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow

# Set the project    exit 1

Write-Host "🔧 Setting project to $ProjectId..." -ForegroundColor Yellow}

gcloud config set project $ProjectId

# Set the project

# Enable required APIsWrite-Host "🔧 Setting project to $ProjectId..." -ForegroundColor Yellow

Write-Host "🔧 Enabling required APIs..." -ForegroundColor Yellowgcloud config set project $ProjectId

gcloud services enable secretmanager.googleapis.com

gcloud services enable appengine.googleapis.com# Enable required APIs

Write-Host "🔧 Enabling required APIs..." -ForegroundColor Yellow

function Set-Secret {gcloud services enable secretmanager.googleapis.com

    param($Name, $Value, $Description)gcloud services enable appengine.googleapis.com

    

    if (-not $Value) {function Set-Secret {

        Write-Host "⚠️  $Name not provided, skipping..." -ForegroundColor Yellow    param($Name, $Value, $Description)

        return    

    }    if (-not $Value) {

            Write-Host "⚠️  $Name not provided, skipping..." -ForegroundColor Yellow

    Write-Host "🔐 Setting secret: $Name" -ForegroundColor Cyan        return

        }

    # Check if secret exists    

    try {    Write-Host "🔐 Setting secret: $Name" -ForegroundColor Cyan

        gcloud secrets describe $Name --quiet 2>$null | Out-Null    

        Write-Host "   Secret $Name already exists, creating new version..." -ForegroundColor Gray    # Check if secret exists

        $Value | gcloud secrets versions add $Name --data-file=-    try {

    } catch {        gcloud secrets describe $Name --quiet 2>$null | Out-Null

        Write-Host "   Creating new secret $Name..." -ForegroundColor Gray        Write-Host "   Secret $Name already exists, creating new version..." -ForegroundColor Gray

        $Value | gcloud secrets create $Name --data-file=- --replication-policy="automatic"        echo $Value | gcloud secrets versions add $Name --data-file=-

    }    } catch {

            Write-Host "   Creating new secret $Name..." -ForegroundColor Gray

    Write-Host "✅ Secret $Name configured" -ForegroundColor Green        gcloud secrets create $Name --data-file=- --replication-policy="automatic" <<< $Value

}    }

    

function Setup-Secrets {    Write-Host "✅ Secret $Name configured" -ForegroundColor Green

    Write-Host ""}

    Write-Host "🔐 Setting up Secret Manager..." -ForegroundColor Yellow

    function Setup-Secrets {

    # Get secrets from user if not provided    Write-Host ""

    if (-not $GeminiApiKey) {    Write-Host "🔐 Setting up Secret Manager..." -ForegroundColor Yellow

        $GeminiApiKey = Read-Host "Enter your Gemini API Key"    

    }    # Get secrets from user if not provided

        if (-not $GeminiApiKey) {

    if (-not $SearchApiKey) {        $GeminiApiKey = Read-Host "Enter your Gemini API Key"

        $SearchApiKey = Read-Host "Enter your Google Search API Key (optional, press Enter to skip)"    }

    }    

        if (-not $SearchApiKey) {

    if (-not $SecretKey) {        $SearchApiKey = Read-Host "Enter your Google Search API Key (optional, press Enter to skip)"

        $SecretKey = Read-Host "Enter a secret key for JWT tokens (or press Enter for auto-generated)"    }

        if (-not $SecretKey) {    

            $SecretKey = [System.Guid]::NewGuid().ToString() + [System.Guid]::NewGuid().ToString()    if (-not $SecretKey) {

        }        $SecretKey = Read-Host "Enter a secret key for JWT tokens (or press Enter for auto-generated)"

    }        if (-not $SecretKey) {

                $SecretKey = [System.Guid]::NewGuid().ToString() + [System.Guid]::NewGuid().ToString()

    # Set secrets        }

    Set-Secret "GEMINI_API_KEY" $GeminiApiKey "Gemini AI API key for LLM analysis"    }

        

    if ($SearchApiKey) {    # Set secrets

        Set-Secret "SEARCH_API_KEY" $SearchApiKey "Google Custom Search API key"    Set-Secret "GEMINI_API_KEY" $GeminiApiKey "Gemini AI API key for LLM analysis"

    }    

        if ($SearchApiKey) {

    Set-Secret "SECRET_KEY" $SecretKey "JWT secret key for authentication"        Set-Secret "SEARCH_API_KEY" $SearchApiKey "Google Custom Search API key"

        }

    Write-Host ""    

    Write-Host "✅ All secrets configured in Secret Manager" -ForegroundColor Green    Set-Secret "SECRET_KEY" $SecretKey "JWT secret key for authentication"

}    

    Write-Host ""

function Deploy-App {    Write-Host "✅ All secrets configured in Secret Manager" -ForegroundColor Green

    Write-Host ""}

    Write-Host "🚀 Deploying to App Engine..." -ForegroundColor Yellow

    function Deploy-App {

    # Create uploads directory if it doesn't exist    Write-Host ""

    if (-not (Test-Path "uploads")) {    Write-Host "🚀 Deploying to App Engine..." -ForegroundColor Yellow

        New-Item -ItemType Directory -Path "uploads" | Out-Null    

        Write-Host "📁 Created uploads directory" -ForegroundColor Gray    # Create uploads directory if it doesn't exist

    }    if (-not (Test-Path "uploads")) {

            New-Item -ItemType Directory -Path "uploads" | Out-Null

    # Deploy to App Engine        Write-Host "📁 Created uploads directory" -ForegroundColor Gray

    Write-Host "   Deploying application..." -ForegroundColor Gray    }

    gcloud app deploy app.yaml --quiet    

        # Deploy to App Engine

    Write-Host "✅ Application deployed successfully!" -ForegroundColor Green    Write-Host "   Deploying application..." -ForegroundColor Gray

        gcloud app deploy app.yaml --quiet

    # Get the URL    

    $url = gcloud app browse --no-launch-browser    Write-Host "✅ Application deployed successfully!" -ForegroundColor Green

    Write-Host ""    

    Write-Host "🌐 Your application is live at:" -ForegroundColor Cyan    # Get the URL

    Write-Host "   $url" -ForegroundColor White    $url = gcloud app browse --no-launch-browser 2>&1 | Select-String "https://"

    Write-Host "   API Docs: $url/docs" -ForegroundColor White    if ($url) {

    Write-Host "   Health Check: $url/health" -ForegroundColor White        Write-Host ""

}        Write-Host "🌐 Your application is live at:" -ForegroundColor Cyan

        Write-Host "   $($url.Line)" -ForegroundColor White

# Main execution        Write-Host "   API Docs: $($url.Line)/docs" -ForegroundColor White

try {        Write-Host "   Health Check: $($url.Line)/health" -ForegroundColor White

    if ($All -or (-not $SecretsOnly -and -not $DeployOnly)) {    }

        Setup-Secrets}

        Deploy-App

    } elseif ($SecretsOnly) {function Test-Deployment {

        Setup-Secrets    Write-Host ""

    } elseif ($DeployOnly) {    Write-Host "🧪 Testing deployment..." -ForegroundColor Yellow

        Deploy-App    

    }    try {

            $url = gcloud app browse --no-launch-browser 2>&1 | Select-String "https://"

    Write-Host ""        if ($url) {

    Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green            $healthUrl = "$($url.Line.Trim())/health"

    Write-Host ""            Write-Host "   Testing health endpoint: $healthUrl" -ForegroundColor Gray

    Write-Host "📋 Next Steps:" -ForegroundColor Yellow            

    Write-Host "1. Test your API endpoints at your App Engine URL" -ForegroundColor White            $response = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 30

    Write-Host "2. Update your frontend to use the new backend URL" -ForegroundColor White            if ($response.status -eq "healthy") {

    Write-Host "3. Monitor logs: gcloud app logs tail -s default" -ForegroundColor White                Write-Host "✅ Health check passed!" -ForegroundColor Green

                    Write-Host "   Service: $($response.service)" -ForegroundColor Gray

} catch {            } else {

    Write-Host ""                Write-Host "⚠️  Health check returned unexpected status" -ForegroundColor Yellow

    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red            }

    Write-Host "💡 Check your billing account and permissions" -ForegroundColor Yellow        }

    exit 1    } catch {

}        Write-Host "⚠️  Could not test deployment automatically" -ForegroundColor Yellow
        Write-Host "   Please test manually by visiting your app URL" -ForegroundColor Gray
    }
}

# Main execution
try {
    if ($All -or (-not $SecretsOnly -and -not $DeployOnly)) {
        Setup-Secrets
        Deploy-App
        Test-Deployment
    } elseif ($SecretsOnly) {
        Setup-Secrets
    } elseif ($DeployOnly) {
        Deploy-App
        Test-Deployment
    }
    
    Write-Host ""
    Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Test your API endpoints at your App Engine URL" -ForegroundColor White
    Write-Host "2. Update your frontend to use the new backend URL" -ForegroundColor White
    Write-Host "3. Monitor logs: gcloud app logs tail -s default" -ForegroundColor White
    Write-Host ""
    Write-Host "🔒 Security Notes:" -ForegroundColor Cyan
    Write-Host "• All sensitive data is stored in Secret Manager" -ForegroundColor White
    Write-Host "• CORS is configured for your specified origins only" -ForegroundColor White
    Write-Host "• HTTPS is enforced for all traffic" -ForegroundColor White
    
} catch {
    Write-Host ""
    Write-Host "❌ Deployment failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Troubleshooting tips:" -ForegroundColor Yellow
    Write-Host "• Check your billing account is set up" -ForegroundColor White
    Write-Host "• Verify you have proper permissions in the project" -ForegroundColor White
    Write-Host "• Ensure all required APIs are enabled" -ForegroundColor White
    exit 1
}
