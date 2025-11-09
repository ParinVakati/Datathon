# Quick Start Guide

Get the Developer Intelligence MCP Server running in 5 minutes!

## Step 1: Start the Server

```bash
cd MCP
python server.py
```

The server will start on `http://localhost:8000`

## Step 2: Test It Works

Open a new terminal and run:

```bash
# Health check
curl http://localhost:8000/health

# Or test with Python
python test_client.py
```

## Step 3: (Optional) Add API Keys

For full functionality, set environment variables:

**On Linux/Mac:**
```bash
export GITHUB_TOKEN="your_token"
export GITHUB_USERNAME="your_username"
export WEATHER_API_KEY="your_key"
```

**On Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="your_token"
$env:GITHUB_USERNAME="your_username"
$env:WEATHER_API_KEY="your_key"
```

Then restart the server.

## Step 4: Try Example Queries

```bash
# Time query (works without API keys)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What day is it today?"}'

# Weather query (needs WEATHER_API_KEY)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the weather like?"}'

# GitHub query (needs GITHUB_TOKEN)
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are my open GitHub issues?"}'
```

## Getting API Keys

### GitHub Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:user`
4. Copy the token

### Weather API Key
1. Sign up at https://openweathermap.org/api
2. Get your free API key from the dashboard
3. Copy the key

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [example_usage.py](example_usage.py) for Python examples
- Run [test_client.py](test_client.py) for comprehensive testing

Happy coding! 🚀

