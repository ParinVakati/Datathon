# Developer Intelligence MCP Server

A smart context engine that intelligently fetches, filters, and formats data from multiple real-world services (GitHub, Weather APIs, Time/Date) to provide rich, contextual information for AI-powered developer assistance.

##  Purpose

This MCP (Model Context Protocol) server acts as a "smart context engine" that enhances AI assistants by providing relevant, real-time context from multiple data sources. When a developer asks a question, the server automatically:

1. **Analyzes the query** to understand what context is needed
2. **Fetches relevant data** from GitHub, Weather APIs, and time/date services
3. **Assembles a context package** with filtered, formatted information
4. **Delivers the package** to the AI model for hyper-relevant responses

## 🛠 What It Does

### Query Analysis
The server uses intelligent keyword detection to determine which data sources to query:
- **GitHub keywords**: `github`, `repo`, `repository`, `issue`, `pr`, `pull request`, `commit`, `code`, `branch`
- **Weather keywords**: `weather`, `temperature`, `rain`, `snow`, `forecast`, `outside`
- **Time keywords**: `today`, `tomorrow`, `yesterday`, `now`, `time`, `date`, `schedule`

### Data Sources

#### 1. **GitHub API** 
- Fetches user repositories (recent, starred, updated)
- Retrieves open issues and pull requests
- Provides code context and project status
- Supports repository-specific queries

#### 2. **Weather API** 
- Current weather conditions (temperature, humidity, wind)
- Weather forecasts for planning
- Location-aware context (configurable city)

#### 3. **Time/Date Service** 
- Current date and time
- Day of week, week number
- Relative dates (tomorrow, yesterday)
- Time-of-day context (morning, afternoon, evening)

##  Quick Start

### Prerequisites

- Python 3.7 or higher
- API keys (optional, for full functionality):
  - GitHub Personal Access Token (for GitHub features)
  - OpenWeatherMap API Key (for weather features)

### Installation

1. **Clone or navigate to the MCP directory:**
   ```bash
   cd MCP
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Note: This server uses only Python standard library, so no external packages are required!

3. **Set up environment variables (optional):**
   
   Create a `.env` file or export environment variables:
   ```bash
   # GitHub API (optional)
   export GITHUB_TOKEN="your_github_personal_access_token"
   export GITHUB_USERNAME="your_github_username"
   
   # Weather API (optional)
   export WEATHER_API_KEY="your_openweathermap_api_key"
   export WEATHER_CITY="New York"  # Default: "New York"
   ```
   
   **Getting API Keys:**
   - **GitHub Token**: Go to GitHub Settings → Developer settings → Personal access tokens → Generate new token (classic). Grant `repo` and `read:user` scopes.
   - **Weather API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/api) (free tier available)

4. **Run the server:**
   ```bash
   python server.py
   ```
   
   Or specify a custom port:
   ```bash
   python server.py 8080
   ```

5. **Verify the server is running:**
   ```bash
   curl http://localhost:8000/health
   ```

##  API Endpoints

### POST `/query`
Submit a query to get contextual information.

**Request:**
```json
{
  "query": "What are my open GitHub issues?"
}
```

**Response:**
```json
{
  "success": true,
  "query": "What are my open GitHub issues?",
  "context_package": {
    "query": "What are my open GitHub issues?",
    "timestamp": "2024-01-15T10:30:00",
    "sources": ["GitHub", "Time/Date"],
    "context": {
      "github": {
        "source": "GitHub",
        "issues": [
          {
            "title": "Fix bug in authentication",
            "number": 42,
            "state": "open",
            "repo": "username/my-repo",
            "url": "https://github.com/username/my-repo/issues/42"
          }
        ]
      },
      "time": {
        "source": "Time/Date",
        "current_time": "2024-01-15 10:30:00",
        "current_date": "Monday, January 15, 2024"
      }
    }
  },
  "formatted_context": "...",
  "sources_used": ["GitHub", "Time/Date"]
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "MCP Developer Intelligence Server"
}
```

### GET `/`
Service information endpoint.

##  Example Prompts

### GitHub Context Examples

**Query:** `"What are my open GitHub issues?"`
- **Context Fetched:** Recent open issues from your repositories
- **AI Response:** "You have 3 open issues: #42 in my-repo (Fix bug), #38 in other-repo (Add feature), ..."

**Query:** `"Show me my recent repositories"`
- **Context Fetched:** Your most recently updated repositories
- **AI Response:** "Your recent repos: my-project (Python, 15 stars, updated 2 days ago), ..."

**Query:** `"What pull requests are open in repo:my-project?"`
- **Context Fetched:** Open PRs in the specified repository
- **AI Response:** "There are 2 open PRs in my-project: #25 (Add tests), #24 (Refactor API)"

### Weather Context Examples

**Query:** `"What's the weather like today?"`
- **Context Fetched:** Current weather conditions
- **AI Response:** "It's currently 22°C (feels like 20°C) in New York with clear skies. Humidity is 65% and wind speed is 5 m/s."

**Query:** `"What's the weather forecast for tomorrow?"`
- **Context Fetched:** Weather forecast for tomorrow
- **AI Response:** "Tomorrow's forecast: Morning 18°C with light rain, afternoon 21°C with scattered clouds..."

### Time Context Examples

**Query:** `"What day is it today?"`
- **Context Fetched:** Current date and time information
- **AI Response:** "Today is Monday, January 15, 2024. It's currently 10:30 AM (Morning)."

**Query:** `"Is it a weekend?"`
- **Context Fetched:** Day of week and weekend status
- **AI Response:** "No, today is Monday, so it's a weekday. The weekend starts in 5 days."

### Combined Context Examples

**Query:** `"Should I work on GitHub issues today or wait until tomorrow? What's the weather like?"`
- **Context Fetched:** GitHub issues, weather, and time context
- **AI Response:** "You have 3 open issues that need attention. Today's weather is perfect for focused work (22°C, clear). Tomorrow's forecast shows rain, so today might be better for coding. Consider tackling issue #42 first..."

##  Testing the Server

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Submit a query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my open GitHub issues?"}'
```

### Using Python

```python
import requests
import json

# Health check
response = requests.get('http://localhost:8000/health')
print(response.json())

# Submit a query
query = {
    "query": "What's the weather like today?"
}
response = requests.post('http://localhost:8000/query', json=query)
result = response.json()
print(result['formatted_context'])
```

### Using the Test Script

A test script is included (`test_client.py`) that demonstrates various query types:

```bash
python test_client.py
```

##  Architecture

```
User Query
    ↓
Context Analyzer (determines what data sources to query)
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
│ GitHub Fetcher  │ Weather Fetcher │  Time Fetcher   │
│                 │                 │                 │
│ - Repos         │ - Current       │ - Date/Time     │
│ - Issues        │ - Forecast      │ - Day of Week   │
│ - PRs           │ - Conditions    │ - Relative      │
└─────────────────┴─────────────────┴─────────────────┘
    ↓
Context Assembler (combines and formats data)
    ↓
Formatted Context Package
    ↓
AI Model (receives rich context for response)
```

## Key Features

### 1. **Intelligent Query Analysis**
- Automatically detects what context is needed
- Only fetches relevant data (efficient)
- Supports natural language queries

### 2. **Multi-Source Integration**
- Combines data from GitHub, Weather, and Time services
- Handles API failures gracefully
- Works even if some APIs are unavailable

### 3. **Smart Context Formatting**
- Formats data for optimal AI consumption
- Provides both structured (JSON) and human-readable formats
- Includes metadata and source attribution

### 4. **Robust Error Handling**
- Graceful degradation when APIs are unavailable
- Clear error messages
- Continues working with partial data

### 5. **Extensible Design**
- Easy to add new data sources
- Modular architecture
- Clean separation of concerns

##  Security & Privacy

- **API Keys**: Store in environment variables, never commit to version control
- **No Data Storage**: Server doesn't store queries or responses
- **HTTPS Recommended**: For production, use HTTPS with proper certificates
- **Rate Limiting**: Consider implementing rate limiting for production use

##  Limitations & Future Enhancements

### Current Limitations
- Weather API requires API key (free tier available)
- GitHub API requires authentication for private repos
- No caching (each query fetches fresh data)
- Single-threaded server (can handle concurrent requests but not optimized)

### Potential Enhancements
- Add more data sources (Slack, Jira, Calendar, Email)
- Implement caching for frequently accessed data
- Add authentication/authorization
- Support for multiple users/sessions
- WebSocket support for real-time updates
- GraphQL endpoint
- Rate limiting and request throttling

##  Example Integration with AI Models

### With OpenAI API

```python
import requests
import openai

# Get context from MCP server
mcp_response = requests.post('http://localhost:8000/query', 
    json={'query': user_query})
context = mcp_response.json()['formatted_context']

# Send to OpenAI with context
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful developer assistant."},
        {"role": "user", "content": f"{context}\n\nUser Query: {user_query}"}
    ]
)
```

### With Claude API

```python
import requests
import anthropic

# Get context from MCP server
mcp_response = requests.post('http://localhost:8000/query',
    json={'query': user_query})
context = mcp_response.json()['formatted_context']

# Send to Claude with context
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": f"{context}\n\nUser Query: {user_query}"
    }]
)
```

##  Contributing

This is a competition submission. Feel free to fork and extend it!

##  License

This project is created for the Build-Your-Own-MCP Challenge.

##  Acknowledgments

- GitHub API for repository and issue data
- OpenWeatherMap for weather data
- Python standard library for making this dependency-free

---

**Built with  for the Build-Your-Own-MCP Challenge**

*Making AI assistants more personal, aware, and useful through intelligent context.*

