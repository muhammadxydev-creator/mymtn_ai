# myMTN NG AI Customer Support System

A Django-based web simulation of an AI-enhanced customer support system for the myMTN NG mobile application, featuring multilingual support (English, Yoruba, Hausa, Igbo, Pidgin), intent classification, entity extraction, and human-AI handoff capabilities.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- pip package manager

### 2. Installation

```bash
# Install dependencies
pip install django djangorestframework django-cors-headers channels redis psycopg2-binary pillow

# Navigate to project directory
cd chapter3
```

### 3. Database Setup

```bash
# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
# Or load sample data (includes admin user: admin/admin123)
python manage.py loaddata initial_data.json
```

### 4. Run Development Server

```bash
# Start the server
python manage.py runserver
```

Access the application:
- **Admin Interface**: http://127.0.0.1:8000/admin/
  - Username: `admin`
  - Password: `admin123`
- **API Root**: http://127.0.0.1:8000/api/
- **API Docs**: http://127.0.0.1:8000/api/docs/ (if DRF Spectacular installed)

## 📁 Project Structure

```
chapter3/
├── core/               # Staff, Projects, Platforms, Tags
├── visitors/           # Visitor management & sessions
├── chat/               # Conversations & Messages
├── nlp_service/        # NLP models, intents, entities
├── knowledge_base/     # Documents, Q&A, Web crawling
├── config/             # Project settings & URLs
└── manage.py
```

## 🔑 Key Features

- **Multilingual Support**: English, Yoruba, Hausa, Igbo, Nigerian Pidgin
- **AI-Powered Chat**: Intent classification (AfroXLMR ready), entity extraction
- **Smart Escalation**: Automatic handoff to human agents when needed
- **Multi-Channel**: Website, WhatsApp, Mobile App support
- **Real-Time Ready**: Django Channels configured for WebSocket support
- **Knowledge Base**: Q&A pairs, document upload, web crawling

## 🛠️ API Endpoints

After running the server, access these endpoints:

| Resource | Endpoint | Methods |
|----------|----------|---------|
| Staff | `/api/staff/` | GET, POST |
| Visitors | `/api/visitors/` | GET, POST |
| Sessions | `/api/sessions/` | GET, POST |
| Messages | `/api/messages/` | GET, POST |
| Intents | `/api/intents/` | GET, POST |
| Knowledge | `/api/knowledge/` | GET, POST |

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage (if coverage installed)
coverage run manage.py test
coverage report
```

## 📝 Chapter 3 Compliance

This implementation follows the methodology described in Chapter 3:
- ✅ Three-tier architecture (Presentation, Logic, Data)
- ✅ PostgreSQL-ready (SQLite for development)
- ✅ AfroXLMR transformer integration points
- ✅ Escalation logic for human handoff
- ✅ Multilingual support for Nigerian languages
- ✅ Comprehensive testing framework ready

## 🔐 Security Notes

- Change default admin password immediately
- Set `DEBUG=False` in production
- Use environment variables for sensitive settings
- Enable HTTPS in production

## 📄 License

Academic Project - Chapter 3 Implementation