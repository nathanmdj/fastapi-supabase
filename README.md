# FastAPI Supabase Backend

A modern FastAPI backend with Supabase integration designed for complex algorithm processing. Built with clean architecture principles and SOLID design patterns.

## 🚀 Features

- **Authentication**: JWT-based authentication using Supabase Auth
- **Algorithm Processing**: Support for multiple algorithm types (Fibonacci, Prime Check, Sorting, Matrix Multiplication)
- **Clean Architecture**: Separation of concerns with clear layer boundaries
- **Type Safety**: Full type hints with Pydantic validation
- **Modern Python**: Built with Python 3.11+ and latest dependencies
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Pre-configured with Black, isort, flake8, and mypy

## 🏗️ Architecture

```
app/
├── api/           # HTTP endpoints and routing
├── core/          # Configuration, security, database
├── models/        # Domain entities
├── schemas/       # Pydantic request/response models
├── services/      # Business logic and external integrations
└── utils/         # Helper functions
```

## 📋 Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Supabase project with authentication enabled

## ⚡ Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd fastapi-supabase
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
JWT_SECRET_KEY=your-jwt-secret-key
BACKEND_CORS_ORIGINS=http://localhost:3000
```

### 4. Database Setup

Create the required tables in your Supabase database:

```sql
-- Algorithm processing requests
CREATE TABLE algorithm_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    algorithm_type TEXT NOT NULL,
    input_data JSONB NOT NULL,
    result JSONB,
    status TEXT NOT NULL DEFAULT 'pending',
    error TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- User profiles (optional)
CREATE TABLE profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    first_name TEXT,
    last_name TEXT,
    avatar_url TEXT,
    preferences JSONB,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 5. Run the Application

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

## 🔧 Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test file
uv run pytest tests/test_algorithms.py
```

### Code Quality

```bash
# Format code
uv run black .

# Sort imports
uv run isort .

# Lint code
uv run flake8

# Type checking
uv run mypy app/

# Run all checks
uv run black . && uv run isort . && uv run flake8 && uv run mypy app/
```

## 📡 API Endpoints

### Authentication
- `GET /api/v1/auth/me` - Get current user info
- `GET /api/v1/auth/profile` - Get user profile
- `PUT /api/v1/auth/profile` - Update user profile
- `POST /api/v1/auth/verify-token` - Verify JWT token

### Algorithms
- `POST /api/v1/algorithms/process` - Process algorithm request
- `GET /api/v1/algorithms/history` - Get processing history
- `GET /api/v1/algorithms/types` - Get available algorithm types
- `GET /api/v1/algorithms/stats` - Get user statistics

### System
- `GET /` - Root endpoint
- `GET /health` - Health check

## 🧮 Supported Algorithms

### Fibonacci Sequence
```json
{
  "algorithm_type": "fibonacci",
  "input_data": {"n": 10}
}
```

### Prime Number Check
```json
{
  "algorithm_type": "prime_check",
  "input_data": {"number": 17}
}
```

### Array Sorting
```json
{
  "algorithm_type": "sorting",
  "input_data": {
    "array": [3, 1, 4, 1, 5, 9],
    "algorithm": "quicksort"
  }
}
```

### Matrix Multiplication
```json
{
  "algorithm_type": "matrix_multiply",
  "input_data": {
    "matrix_a": [[1, 2], [3, 4]],
    "matrix_b": [[5, 6], [7, 8]]
  }
}
```

## 🔐 Authentication

This backend uses Supabase Auth for user management. Authentication flow:

1. Users authenticate via your NextJS frontend using Supabase Auth
2. Frontend sends requests with `Authorization: Bearer <supabase_jwt_token>` header
3. Backend validates the JWT token and extracts user information
4. Protected endpoints require valid authentication

## 🏢 Production Deployment

### Environment Variables

Required for production:

```env
ENVIRONMENT=production
DEBUG=false
SUPABASE_URL=your-production-supabase-url
SUPABASE_KEY=your-production-anon-key
SUPABASE_SERVICE_KEY=your-production-service-key
JWT_SECRET_KEY=your-secure-jwt-secret
BACKEND_CORS_ORIGINS=https://yourdomain.com
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv sync --no-dev

COPY app/ app/

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Integration with NextJS Frontend

This backend is designed to work seamlessly with a NextJS frontend:

1. **Shared Authentication**: Uses the same Supabase project for user management
2. **CORS Configuration**: Allows requests from your frontend domain
3. **Type Safety**: Pydantic schemas ensure consistent API contracts
4. **Error Handling**: Standardized error responses for easy frontend handling

## 📚 Project Structure

- **Clean Architecture**: Clear separation between business logic, data access, and presentation
- **Dependency Injection**: FastAPI's dependency system for loose coupling
- **Service Layer**: Business logic isolated in service classes
- **Repository Pattern**: Generic database operations with domain-specific services
- **Type Safety**: Full type hints throughout the codebase

## 🔄 Adding New Algorithms

To add a new algorithm type:

1. Add the algorithm type to `AlgorithmType` enum in `app/schemas/algorithm.py`
2. Implement the algorithm logic in `app/services/algorithm_service.py`
3. Add input validation schema if needed
4. Update the algorithm types endpoint
5. Add tests in `tests/test_algorithms.py`

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the CLAUDE.md file for development guidance
3. Check the test files for usage examples