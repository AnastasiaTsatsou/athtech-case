# Expense Tracker - Microservices Application

## 📋 Project Overview

This project implements a two-tier microservices application for personal expense management. The application demonstrates modern cloud-native development practices including containerization, automated CI, and comprehensive monitoring.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git for version control
- Python 3.12+ (for local development)

### Running the Application

1. **Clone the repository**
   ```bash
   git clone https://github.com/AnastasiaTsatsou/athtech-case.git
   cd athtech-case
   ```

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Metrics: http://localhost:8000/metrics

### API Endpoints

- `GET /expenses` - Retrieve all expenses
- `GET /expenses?category={category}` - Filter expenses by category
- `POST /expenses` - Create new expense
- `PUT /expenses/{id}` - Update existing expense
- `DELETE /expenses/{id}` - Delete expense
- `GET /health` - Application health status
- `GET /metrics` - Application metrics

## 🔄 CI/CD Pipeline

The project includes automated CI/CD pipeline using GitHub Actions:

- **Continuous Integration**: Automated testing on every push and pull request
- **Container Building**: Automated Docker image building and testing
- **Deployment**: Automated deployment to staging/production environments
- **Security Scanning**: Vulnerability scanning for containers and dependencies

### Pipeline Triggers

- Push to `main` branch
- Pull request creation and updates
- Manual workflow dispatch

## 📊 Monitoring

The application includes comprehensive monitoring capabilities:

- **Health Checks**: Container and application health monitoring
- **Metrics Collection**: Performance and business metrics

## 🌿 Git Workflow

The project follows Git Flow branching strategy:

- `main` - Production-ready code
- `dev` - Development integration branch
