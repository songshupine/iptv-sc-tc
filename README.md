# Python Cloud Functions - FastAPI | EdgeOne Pages

A demonstration website showcasing how to deploy high-performance FastAPI applications as serverless functions on EdgeOne Pages.

## 🚀 Features

- **FastAPI Framework**: Modern, fast (high-performance) web framework for building APIs
- **Automatic OpenAPI**: Swagger UI & ReDoc documentation generated automatically
- **Pydantic Validation**: Automatic request/response validation with type hints
- **Async Support**: Native async/await for high performance
- **Type Safety**: Full Python type hints support

## 🛠️ Tech Stack

### Frontend
- **Next.js 15** - React full-stack framework
- **React 19** - User interface library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS 4** - Utility-first CSS framework

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation using Python type hints
- **Cloud Functions** - EdgeOne Pages serverless functions

## 📁 Project Structure

```
python-fastapi-template/
├── src/                    # Next.js frontend
├── cloud-functions/        # Python cloud functions
│   ├── api/
│   │   └── [[default]].py # FastAPI application
│   └── requirements.txt   # Python dependencies
├── public/                # Static assets
└── package.json          # Project configuration
```

## 🚀 Quick Start

### Requirements

- Node.js 18+ 
- Python 3.9+
- EdgeOne CLI

### Install Dependencies

```bash
npm install
```

### Development Mode

```bash
edgeone pages dev
```

Visit [http://localhost:8088](http://localhost:8088) to view the application.

## 🎯 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/ | Root endpoint |
| GET | /api/health | Health check |
| GET | /api/info | Function information |
| GET | /api/time | Current server time |
| GET/POST | /api/echo | Echo request info |
| POST | /api/json | Handle JSON body |
| GET | /api/users/{user_id} | Get user by ID |
| POST | /api/users | Create new user |
| GET | /api/search | Search with query params |
| GET | /api/docs | Swagger UI documentation |
| GET | /api/redoc | ReDoc documentation |

## 📚 Documentation

- **FastAPI Documentation**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **EdgeOne Pages Docs**: [https://pages.edgeone.ai/document/python](https://pages.edgeone.ai/document/python)

## Deploy

[![Deploy with EdgeOne Pages](https://cdnstatic.tencentcs.com/edgeone/pages/deploy.svg)](https://edgeone.ai/pages/new?from=github&template=python-fastapi-template)

## 📄 License

This project is licensed under the MIT License.
