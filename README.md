# VeriTrueAI2.0-Backend

VeriTrueAI2.0 is an advanced AI-powered misinformation detection system that provides comprehensive analysis for various forms of media, including text, URLs, images, and videos. This FastAPI backend service performs content analysis, web search for source verification, and LLM-based groundedness assessment to deliver accurate verdicts with confidence scores and supporting evidence.

## 🚀 Features

- **Multi-Modal Analysis**: Support for text, URLs, images, and videos
- **AI-Powered Detection**: Uses LLM for groundedness and truthfulness assessment
- **Source Verification**: Automated web search and credibility scoring
- **Batch Processing**: Analyze multiple items simultaneously
- **Analytics Dashboard**: Comprehensive analytics and reporting
- **History Tracking**: Complete analysis history with search capabilities
- **User Settings**: Customizable preferences and notifications
- **RESTful API**: Well-documented API endpoints
- **Cloud-Ready**: Ready for Google Cloud deployment

## 📋 API Endpoints

### Core Analysis
- `POST /api/v1/analyze/` - Analyze content for misinformation
- `POST /api/v1/analyze/batch` - Batch analysis of multiple items

### File Management
- `POST /api/v1/upload/` - Upload files (images/videos)
- `POST /api/v1/upload/multiple` - Upload multiple files
- `DELETE /api/v1/upload/{file_id}` - Delete uploaded file

### Source Search
- `GET /api/v1/search-sources/` - Search for relevant sources
- `GET /api/v1/search-sources/credible` - Search credible sources only
- `GET /api/v1/search-sources/fact-check` - Search fact-checking sources
- `GET /api/v1/search-sources/academic` - Search academic sources

### History & Analytics
- `GET /api/v1/history/` - Get analysis history
- `GET /api/v1/history/{analysis_id}` - Get specific analysis details
- `GET /api/v1/analytics/overview` - Analytics overview
- `GET /api/v1/analytics/trends` - Trend analysis

### Settings
- `GET /api/v1/settings/{user_id}` - Get user settings
- `PUT /api/v1/settings/{user_id}` - Update user settings

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- PostgreSQL (optional, for persistent storage)
- Redis (optional, for caching)
- OpenAI API key (optional, for enhanced LLM analysis)
- Google Custom Search API (optional, for web search)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/arunpranav-at/VeriTrueAI2.0-Backend.git
   cd VeriTrueAI2.0-Backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - OpenAPI Schema: http://localhost:8000/openapi.json
   - Health Check: http://localhost:8000/health

### Docker Deployment

```bash
# Build the image
docker build -t veritrue-ai-backend .

# Run the container
docker run -p 8000:8000 --env-file .env veritrue-ai-backend
```

### Google Cloud Deployment

1. **Install Google Cloud SDK**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Deploy to App Engine**
   ```bash
   gcloud app deploy app.yaml
   ```

3. **Set environment variables**
   ```bash
   gcloud app versions list
   gcloud app browse
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `development` |
| `DEBUG` | Enable debug mode | `True` |
| `OPENAI_API_KEY` | OpenAI API key for LLM | Required for AI analysis |
| `SEARCH_API_KEY` | Google Custom Search API key | Required for web search |
| `DATABASE_URL` | PostgreSQL connection URL | Optional |
| `REDIS_URL` | Redis connection URL | Optional |
| `MAX_UPLOAD_SIZE` | Maximum file upload size | `50MB` |

### API Configuration

The API supports various configuration options:

- **File Upload**: Supports images (JPEG, PNG, GIF, WebP) and videos (MP4, AVI, MOV, MKV)
- **Batch Processing**: Up to 10 items per batch request
- **Rate Limiting**: Configurable per-user rate limits
- **Source Credibility**: Adjustable credibility thresholds

## 📊 Usage Examples

### Analyze Text Content

```bash
curl -X POST "http://localhost:8000/api/v1/analyze/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Breaking: Scientists discover cure for common cold",
    "media_type": "text",
    "metadata": {}
  }'
```

### Upload and Analyze Image

```bash
# Upload image
curl -X POST "http://localhost:8000/api/v1/upload/" \
  -F "file=@image.jpg"

# Analyze uploaded image
curl -X POST "http://localhost:8000/api/v1/analyze/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "/uploads/image_id.jpg",
    "media_type": "image"
  }'
```

### Search Sources

```bash
curl -X GET "http://localhost:8000/api/v1/search-sources/?query=covid%20vaccine%20effectiveness&limit=5"
```

### Get Analytics

```bash
curl -X GET "http://localhost:8000/api/v1/analytics/overview?days=30"
```

## 🏗️ Architecture

### Core Components

- **FastAPI Application**: High-performance async web framework
- **Analysis Service**: Content processing and analysis coordination
- **LLM Service**: AI-powered groundedness assessment
- **Web Search Service**: Source gathering and credibility scoring
- **File Service**: Upload and media file handling
- **History Service**: Analysis tracking and retrieval
- **Analytics Service**: Usage statistics and reporting

### Data Flow

1. **Content Input**: Text, URL, image, or video submitted via API
2. **Content Processing**: Extract searchable text and metadata
3. **Source Search**: Find relevant sources using web search
4. **LLM Analysis**: Assess groundedness against sources
5. **Verdict Generation**: Produce verdict with confidence and evidence
6. **Result Storage**: Store analysis in history for future reference

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_analysis.py
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email [support@veritrue.ai](mailto:support@veritrue.ai) or open an issue on GitHub.

## 🔮 Roadmap

- [ ] Multi-language support
- [ ] Advanced video analysis with frame extraction
- [ ] Real-time misinformation alerts
- [ ] Integration with social media platforms
- [ ] Mobile app companion
- [ ] Blockchain-based verification

---

**Built with ❤️ by the VeriTrueAI Team**
