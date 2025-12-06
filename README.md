# 🔗 URL Shortener - Fast & Efficient Link Shortening Service

[![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-latest-green.svg)](https://flask.palletsprojects.com/)
[![Redis](https://img.shields.io/badge/redis-latest-red.svg)](https://redis.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

> A lightweight, high-performance URL shortener application built with Flask and Redis. Transform long URLs into short, shareable links with ease. Perfect for social media, marketing campaigns, and clean link management.

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Local Setup](#local-setup)
  - [Docker Setup](#docker-setup)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)
- [Contact](#-contact)

## 🌟 Overview

**URL Shortener V1** is a modern, easy-to-use URL shortening service that helps you create compact, manageable links from long URLs. Built with Python Flask and Redis, this application provides a fast, reliable solution for link shortening needs with a clean web interface and RESTful API.

### Why Use This URL Shortener?

- **Fast Performance**: Lightning-quick URL shortening and retrieval powered by Redis in-memory database
- **Simple Interface**: Clean, intuitive web UI for non-technical users
- **RESTful API**: Easy integration with other applications and services
- **Docker Ready**: Containerized deployment for consistent environments
- **Open Source**: Free to use, modify, and distribute under MIT license

## ✨ Features

### Core Functionality
- ✅ **Instant URL Shortening**: Convert long URLs to short, 6-character keys
- ✅ **Quick Redirection**: Fast redirect from short URL to original destination
- ✅ **Web Interface**: User-friendly HTML form for easy URL shortening
- ✅ **REST API**: Programmatic access for integration with other tools
- ✅ **Redis Storage**: High-performance, in-memory data storage
- ✅ **URL Validation**: Automatic protocol handling and validation
- ✅ **View All URLs**: Admin endpoint to list all shortened URLs
- ✅ **Docker Support**: Easy deployment with Docker and Docker Compose

### Additional Features
- Random alphanumeric key generation for unique short URLs
- Automatic URL protocol detection and correction
- Error handling with meaningful messages
- Containerized application with redis service orchestration
- Environment-based configuration

## 🎥 Demo

The URL Shortener provides a simple web interface where users can:
1. Enter a long URL in the input field
2. Click "Shorten" to generate a short URL
3. Receive a shortened link that redirects to the original URL

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.9** | Backend programming language |
| **Flask** | Lightweight web framework |
| **Redis** | In-memory database for URL storage |
| **HTML/CSS** | Frontend user interface |
| **Docker** | Containerization and deployment |
| **Docker Compose** | Multi-container orchestration |

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher** - [Download Python](https://www.python.org/downloads/)
- **Redis Server** (for local setup) - [Download Redis](https://redis.io/download)
- **Docker & Docker Compose** (for containerized setup) - [Download Docker](https://www.docker.com/get-started)
- **Git** - [Download Git](https://git-scm.com/downloads)

## 🚀 Installation

### Local Setup

Follow these steps to run the URL shortener on your local machine:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/pritesh1991/UrlShortnerV1.git
   cd UrlShortnerV1
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   
   Create a `.env` file in the project root or modify the existing one:
   ```env
   SERVER_NAME=localhost:6000
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

5. **Start Redis Server**
   ```bash
   # On macOS (with Homebrew)
   brew services start redis
   
   # On Linux
   sudo systemctl start redis
   
   # Or run directly
   redis-server
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**
   
   Open your browser and navigate to: `http://localhost:6000`

### Docker Setup

The easiest way to run the URL shortener is using Docker:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/pritesh1991/UrlShortnerV1.git
   cd UrlShortnerV1
   ```

2. **Build and Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**
   
   Open your browser and navigate to: `http://localhost:6000`

4. **Stop the Application**
   ```bash
   docker-compose down
   ```

## 💡 Usage

### Web Interface

1. **Shorten a URL**:
   - Open `http://localhost:6000` in your browser
   - Enter a long URL in the input field (e.g., `https://www.example.com/very/long/url/path`)
   - Click the "Shorten" button
   - Copy the generated short URL

2. **Use the Short URL**:
   - Visit the short URL (e.g., `http://localhost:6000/Abc123`)
   - You'll be automatically redirected to the original long URL

### API Usage

#### Shorten a URL (via API)

```bash
curl -X POST http://localhost:6000/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "url=https://www.example.com/long/url"
```

#### Access a Shortened URL

```bash
curl -L http://localhost:6000/{short_key}
```

#### List All Shortened URLs

```bash
curl http://localhost:6000/all
```

**Response Example:**
```json
{
  "Abc123": "https://www.example.com/long/url",
  "Xyz789": "https://www.google.com",
  "Def456": "https://www.github.com"
}
```

## 📚 API Documentation

### Endpoints

#### 1. Home Page / Shorten URL

**GET /** - Display the web interface

**POST /** - Shorten a URL

- **Content-Type**: `application/x-www-form-urlencoded`
- **Body Parameters**:
  - `url` (required): The long URL to shorten
- **Success Response**: HTML page with the shortened URL
- **Error Response**: HTML page with error message

#### 2. Redirect to Original URL

**GET /{short_key}** - Redirect to the original URL

- **URL Parameters**:
  - `short_key`: The 6-character short key
- **Success Response**: 302 redirect to original URL
- **Error Response**: 
  ```json
  {
    "error": "Short URL not found"
  }
  ```
  Status: 404

#### 3. List All URLs

**GET /all** - Get all shortened URLs

- **Success Response**:
  ```json
  {
    "short_key1": "original_url1",
    "short_key2": "original_url2"
  }
  ```
  Status: 200

## ⚙️ Configuration

The application can be configured using environment variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `SERVER_NAME` | Server hostname and port | `localhost:6000` |
| `REDIS_HOST` | Redis server hostname | `redis` (Docker) / `localhost` (Local) |
| `REDIS_PORT` | Redis server port | `6379` |

### Modifying Configuration

1. **For Local Setup**: Edit the `.env` file in the project root
2. **For Docker Setup**: Edit the `docker-compose.yml` file under the `environment` section

## 📂 Project Structure

```
UrlShortnerV1/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose orchestration
├── .env                   # Environment variables
├── LICENSE                # MIT License
├── README.md             # Project documentation
├── templates/
│   └── index.html        # Web interface template
└── static/
    └── styles.css        # CSS styling for web interface
```

### Key Files

- **app.py**: Contains the Flask application logic, routes, and Redis integration
- **templates/index.html**: HTML template for the web interface
- **static/styles.css**: Styling for the web interface
- **docker-compose.yml**: Defines services (web app and Redis) for Docker deployment
- **Dockerfile**: Instructions for building the Docker image
- **requirements.txt**: Python package dependencies

## 🤝 Contributing

Contributions are welcome! Here's how you can help improve the URL Shortener:

1. **Fork the Repository**
   ```bash
   git clone https://github.com/pritesh1991/UrlShortnerV1.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style
   - Test your changes thoroughly

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Describe your changes in detail

### Contribution Ideas

- Add custom short URL keys (user-defined aliases)
- Implement URL expiration/TTL
- Add click tracking and analytics
- Create a URL management dashboard
- Add authentication and user accounts
- Implement rate limiting
- Add URL validation and safety checks
- Create mobile-responsive design improvements
- Add database persistence options (PostgreSQL, MongoDB)
- Implement QR code generation for short URLs

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Redis Connection Error

**Problem**: `redis.exceptions.ConnectionError: Error connecting to Redis`

**Solution**:
- Ensure Redis is running: `redis-cli ping` (should return `PONG`)
- Check Redis host and port in `.env` file
- For Docker: Make sure redis service is running: `docker-compose ps`

#### 2. Port Already in Use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solution**:
- Check if port 6000 is already in use: `lsof -i :6000`
- Kill the process: `kill -9 <PID>`
- Or change the port in `app.py` and `docker-compose.yml`

#### 3. Module Not Found Error

**Problem**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

#### 4. Docker Build Fails

**Problem**: Docker build or compose fails

**Solution**:
- Ensure Docker is running: `docker --version`
- Rebuild without cache: `docker-compose build --no-cache`
- Check Docker logs: `docker-compose logs`

#### 5. Short URL Returns 404

**Problem**: Accessing a short URL returns "Short URL not found"

**Solution**:
- Verify the URL was created successfully
- Check Redis data: `redis-cli KEYS *`
- Ensure Redis data persistence if needed

### Getting Help

If you encounter other issues:
1. Check the [Issues](https://github.com/pritesh1991/UrlShortnerV1/issues) page
2. Create a new issue with:
   - Detailed description of the problem
   - Steps to reproduce
   - Error messages and logs
   - Your environment (OS, Python version, Docker version)

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What This Means

- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ⚠️ No warranty provided
- ⚠️ No liability

## 📧 Contact

**Pritesh Patel**

- GitHub: [@pritesh1991](https://github.com/pritesh1991)
- Repository: [UrlShortnerV1](https://github.com/pritesh1991/UrlShortnerV1)

### Support

- 🐛 **Bug Reports**: [Create an issue](https://github.com/pritesh1991/UrlShortnerV1/issues/new)
- 💡 **Feature Requests**: [Create an issue](https://github.com/pritesh1991/UrlShortnerV1/issues/new)
- 💬 **Questions**: [Start a discussion](https://github.com/pritesh1991/UrlShortnerV1/discussions)

---

## 🔍 Keywords

`url-shortener`, `flask`, `redis`, `python`, `link-shortener`, `short-url`, `url-shortening-service`, `docker`, `web-application`, `rest-api`, `flask-application`, `redis-database`, `python-flask`, `url-management`, `link-management`, `docker-compose`, `containerization`, `open-source`, `mit-license`, `python3`

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star! ⭐**

Made with ❤️ by [Pritesh Patel](https://github.com/pritesh1991)

</div>
