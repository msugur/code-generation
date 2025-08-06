# 🔧 Flask API Backend

[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![CORS](https://img.shields.io/badge/CORS-Enabled-brightgreen.svg)](https://flask-cors.readthedocs.io/)

> RESTful API backend powering the AI Agent Code Generation Framework with todo management and agent execution capabilities.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Data Model](#-data-model)
- [Agent Integration](#-agent-integration)
- [Development](#-development)

## 🎯 Overview

This Flask application serves as the backend for the AI Agent framework, providing:
- Complete CRUD operations for todo management
- Agent execution endpoints for AI-powered operations
- File-based persistence with JSON storage
- CORS support for cross-origin requests
- Integration with ReAct agents for intelligent task automation

## ✨ Features

- **📝 Todo Management**: Full CRUD operations with timestamp tracking
- **🤖 Agent Execution**: Integrated endpoint for running ReAct agents
- **💾 Persistent Storage**: JSON-based file storage for data persistence
- **🔐 Environment Configuration**: Secure configuration via environment variables
- **🌐 CORS Support**: Enabled for frontend integration
- **🚀 Hot Reload**: Development server with automatic reloading

## 📦 Installation

### Requirements

```txt
Flask==2.3.2
flask-cors==4.0.0
python-dotenv==1.0.0
```

### Setup

1. **Navigate to the app directory**
   ```bash
   cd app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   ```bash
   cat > .env << EOF
   API_KEY=your_mistral_api_key
   PORT=5000
   TODOS_FILE=todos.json
   FLASK_DEBUG=True
   EOF
   ```

4. **Run the server**
   ```bash
   python app.py
   ```

## 🌐 API Endpoints

### Todo Management

#### Get All Todos
```http
GET /todos
```
**Response:**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "completed": false,
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### Get Single Todo
```http
GET /todos/<id>
```
**Response:**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": false,
  "created_at": "2024-01-15T10:30:00"
}
```

#### Create Todo
```http
POST /todos
Content-Type: application/json

{
  "title": "New todo item",
  "completed": false
}
```
**Response:** `201 Created`
```json
{
  "id": 2,
  "title": "New todo item",
  "completed": false,
  "created_at": "2024-01-15T11:00:00"
}
```

#### Update Todo
```http
PUT /todos/<id>
Content-Type: application/json

{
  "title": "Updated title",
  "completed": true
}
```
**Response:**
```json
{
  "id": 1,
  "title": "Updated title",
  "completed": true,
  "created_at": "2024-01-15T10:30:00"
}
```

#### Delete Todo
```http
DELETE /todos/<id>
```
**Response:**
```json
{
  "message": "Todo deleted"
}
```

### Agent Execution

#### Execute ReAct Agent
```http
POST /agent/execute
Content-Type: application/json

{
  "query": "Add a todo to buy milk"
}
```
**Response:**
```json
{
  "success": true,
  "query": "Add a todo to buy milk",
  "answer": "Successfully added todo: 'buy milk' with ID 3",
  "history": [
    {
      "type": "thought",
      "content": "I need to add a new todo item for buying milk"
    },
    {
      "type": "action",
      "content": "add_todo[buy milk]"
    },
    {
      "type": "observation",
      "content": "Successfully added todo: 'buy milk' with ID 3"
    }
  ]
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | Mistral API key for agent LLM | - | No |
| `PORT` | Server port | 5000 | No |
| `TODOS_FILE` | JSON file for todo storage | todos.json | No |
| `FLASK_DEBUG` | Enable debug mode | True | No |

### File Structure

```
app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── todos.json         # Data storage (auto-created)
└── .env              # Environment configuration
```

## 📊 Data Model

### Todo Object

```python
{
    "id": int,           # Unique identifier
    "title": str,        # Todo description
    "completed": bool,   # Completion status
    "created_at": str    # ISO format timestamp
}
```

## 🤖 Agent Integration

The app integrates with the [ReAct Agent](../agents/) system:

```python
# Agent initialization in app.py
tools = [
    AddTodoTool(api_url=f"http://localhost:{PORT}"),
    DeleteTodoTool(api_url=f"http://localhost:{PORT}"),
    ListTodosTool(api_url=f"http://localhost:{PORT}")
]

agent = ReActAgent(tools, verbose=False)
result = agent.run(query)
```

### Available Agent Tools

- **AddTodoTool**: Creates new todos
- **DeleteTodoTool**: Removes existing todos
- **ListTodosTool**: Retrieves all todos

## 🛠️ Development

### Running Tests

```bash
# Test the API endpoints
python ../scripts-api-test/test_endpoints.py

# Test agent integration
python test_agent.py
```

### Adding New Endpoints

1. Define the route in `app.py`
2. Implement the handler function
3. Add appropriate error handling
4. Update this documentation

### Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Successful GET/PUT/DELETE
- `201 Created`: Successful POST
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## 🔄 Integration

### With Frontend

The app serves the HTML interface at the root endpoint:

```python
@app.route('/')
def index():
    return send_file('index.html')
```

### With Agents

Import path for agent integration:

```python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.react_agent import ReActAgent
```

## 📚 Related Documentation

- [🏠 Main Project README](../) - Project overview
- [🤖 Agent Documentation](../agents/) - ReAct agent details
- [🧪 API Testing](../scripts-api-test/) - Testing utilities

## 🐛 Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

View request details:
```python
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
```

---

<p align="center">
Part of the <a href="../">AI Agent Code Generation Framework</a>
</p>