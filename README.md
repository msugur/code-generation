# 🤖 AI Agent Code Generation Framework

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-Powered-purple.svg)](https://mistral.ai/)
[![ReAct](https://img.shields.io/badge/Pattern-ReAct-orange.svg)](https://react-lm.github.io/)

> A sophisticated multi-agent orchestration framework featuring ReAct (Reasoning and Acting) agents for intelligent task automation and code generation. Built with Python, Flask, and integrated with Mistral AI for advanced language model capabilities.

## 🌟 Features

- **🧠 ReAct Agent Architecture**: Implements the Thought → Action → Observation pattern for intelligent decision-making
- **🔧 Modular Tool System**: Extensible tool framework for agent capabilities
- **🌐 RESTful API**: Full-featured Flask backend with CORS support
- **🎨 Interactive Web UI**: Real-time visualization of agent reasoning process
- **🤝 Multi-Agent Support**: Scalable architecture for multiple specialized agents
- **🔌 LLM Integration**: Seamless integration with Mistral AI (OpenAI-compatible)
- **📝 Todo Management**: Demonstration application showcasing agent capabilities

## 📁 Project Structure

```
code-generation/
├── 📱 app/                    # Flask application backend
│   ├── app.py                # Main Flask server with API endpoints
│   ├── requirements.txt      # Python dependencies
│   └── todos.json            # Data persistence
│
├── 🤖 agents/                # AI agent implementations
│   ├── react_agent.py        # ReAct agent with tool integration
│   └── README.md            # Agent documentation
│
├── 🧪 scripts-api-test/      # API testing utilities
│   ├── mistral_api_test.py  # Mistral API integration tests
│   └── README.md            # Testing documentation
│
├── 🌐 index.html             # Interactive web interface
└── 📖 README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Mistral API access (optional, for LLM features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/code-generation.git
   cd code-generation
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd app
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file in the app directory
   echo "API_KEY=your_mistral_api_key" > .env
   echo "PORT=5000" >> .env
   echo "TODOS_FILE=todos.json" >> .env
   ```

### Running the Application

1. **Start the Flask server**
   ```bash
   cd app
   python app.py
   ```
   The server will start on `http://localhost:5000`

2. **Open the web interface**
   - Navigate to `http://localhost:5000` in your browser
   - The interactive UI will display with agent controls

## 🎯 Key Components

### 🤖 [ReAct Agent](agents/)
The core intelligence system implementing reasoning and acting patterns:
- **Thought Generation**: Analyzes tasks and plans actions
- **Tool Execution**: Performs actions using available tools
- **Observation Processing**: Interprets results and adjusts strategy
- **Iterative Problem Solving**: Chains multiple steps to achieve goals

### 🔧 [Flask API Backend](app/)
RESTful API server providing:
- Todo CRUD operations
- Agent execution endpoints
- WebSocket support for real-time updates
- Data persistence layer

### 🧪 [API Testing Suite](scripts-api-test/)
Comprehensive testing utilities:
- Mistral API connectivity tests
- Model availability checks
- Performance benchmarking tools

## 📚 API Documentation

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve web interface |
| `/todos` | GET | List all todos |
| `/todos` | POST | Create new todo |
| `/todos/<id>` | GET | Get specific todo |
| `/todos/<id>` | PUT | Update todo |
| `/todos/<id>` | DELETE | Delete todo |
| `/agent/execute` | POST | Execute ReAct agent |

### Agent Execution Example

```python
# Execute agent via API
import requests

response = requests.post('http://localhost:5000/agent/execute', 
    json={
        "query": "Add a todo to buy groceries"
    }
)

result = response.json()
print(result['answer'])  # Agent's response
print(result['history']) # Step-by-step reasoning
```

## 🛠️ Development

### Adding New Tools

Create custom tools by extending the base `Tool` class:

```python
from agents.react_agent import Tool

class CustomTool(Tool):
    def __init__(self):
        super().__init__(
            name="custom_tool",
            description="Description of what the tool does"
        )
    
    def execute(self, input_data):
        # Tool implementation
        return "Tool result"
```

### Extending the Agent

The ReAct agent can be customized with:
- Custom reasoning prompts
- Additional tool integrations
- Modified observation processing
- Alternative LLM backends

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | Mistral API key | None |
| `PORT` | Flask server port | 5000 |
| `TODOS_FILE` | Todo storage file | todos.json |
| `FLASK_DEBUG` | Debug mode | True |

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Mistral AI](https://mistral.ai/) for LLM capabilities
- [ReAct Paper](https://react-lm.github.io/) for the agent architecture pattern
- Flask community for the excellent web framework
- Contributors and maintainers

## 🔗 Links

- [**Agent Documentation**](agents/) - Detailed agent implementation guide
- [**API Backend**](app/) - Flask application documentation
- [**Testing Suite**](scripts-api-test/) - API testing documentation
- [**Issues**](https://github.com/yourusername/code-generation/issues) - Report bugs or request features
- [**Discussions**](https://github.com/yourusername/code-generation/discussions) - Community discussions

---

<p align="center">
Built with ❤️ by the AI Agent Development Team
</p>