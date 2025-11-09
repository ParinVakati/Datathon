"""
Developer Intelligence MCP Server
A smart context engine that combines GitHub, Weather, and Time data
to provide rich context for AI-powered developer assistance.
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.parse
import urllib.error


class ContextAnalyzer:
    """Analyzes user queries to determine what context is needed."""
    
    # Keywords that indicate what context to fetch
    GITHUB_KEYWORDS = [
        'github', 'repo', 'repository', 'issue', 'pr', 'pull request',
        'commit', 'code', 'branch', 'merge', 'push', 'pull'
    ]
    
    WEATHER_KEYWORDS = [
        'weather', 'temperature', 'rain', 'snow', 'sunny', 'cloudy',
        'forecast', 'outside', 'outdoor', 'meeting outside'
    ]
    
    TIME_KEYWORDS = [
        'today', 'tomorrow', 'yesterday', 'now', 'time', 'date',
        'schedule', 'deadline', 'due', 'when'
    ]
    
    def analyze(self, query: str) -> Dict[str, bool]:
        """Analyze query and return what context sources are needed."""
        query_lower = query.lower()
        
        return {
            'github': any(keyword in query_lower for keyword in self.GITHUB_KEYWORDS),
            'weather': any(keyword in query_lower for keyword in self.WEATHER_KEYWORDS),
            'time': any(keyword in query_lower for keyword in self.TIME_KEYWORDS),
            'always_fetch_time': True  # Always include time context
        }


class GitHubContextFetcher:
    """Fetches context from GitHub API."""
    
    def __init__(self, token: Optional[str] = None, username: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN', '')
        self.username = username or os.getenv('GITHUB_USERNAME', '')
        self.base_url = 'https://api.github.com'
    
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """Make authenticated request to GitHub API."""
        if not self.token:
            return None
        
        url = f"{self.base_url}{endpoint}"
        req = urllib.request.Request(url)
        req.add_header('Authorization', f'token {self.token}')
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header('User-Agent', 'MCP-Developer-Intelligence-Server')
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"GitHub API error: {e}")
            return None
    
    def get_user_repos(self, limit: int = 5) -> List[Dict]:
        """Get user's recent repositories."""
        if not self.username:
            return []
        
        data = self._make_request(f'/users/{self.username}/repos?sort=updated&per_page={limit}')
        if not data:
            return []
        
        repos = []
        for repo in data[:limit]:
            repos.append({
                'name': repo.get('name', ''),
                'description': repo.get('description', ''),
                'language': repo.get('language', ''),
                'stars': repo.get('stargazers_count', 0),
                'updated_at': repo.get('updated_at', ''),
                'url': repo.get('html_url', '')
            })
        return repos
    
    def get_recent_issues(self, repo: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """Get recent issues from user's repos or specific repo."""
        if not self.username:
            return []
        
        if repo:
            endpoint = f'/repos/{self.username}/{repo}/issues?state=open&per_page={limit}'
        else:
            endpoint = f'/user/issues?filter=all&state=open&per_page={limit}'
        
        data = self._make_request(endpoint)
        if not data:
            return []
        
        issues = []
        for issue in data[:limit]:
            issues.append({
                'title': issue.get('title', ''),
                'number': issue.get('number', 0),
                'state': issue.get('state', ''),
                'repo': issue.get('repository', {}).get('full_name', '') if 'repository' in issue else repo or '',
                'url': issue.get('html_url', '')
            })
        return issues
    
    def get_recent_prs(self, repo: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """Get recent pull requests."""
        if not self.username:
            return []
        
        if repo:
            endpoint = f'/repos/{self.username}/{repo}/pulls?state=open&per_page={limit}'
        else:
            endpoint = f'/search/issues?q=author:{self.username}+type:pr+state:open&per_page={limit}'
        
        data = self._make_request(endpoint)
        if not data:
            return []
        
        # Handle search API response format
        if 'items' in data:
            data = data['items']
        
        prs = []
        for pr in data[:limit]:
            prs.append({
                'title': pr.get('title', ''),
                'number': pr.get('number', 0),
                'state': pr.get('state', ''),
                'repo': pr.get('repository', {}).get('full_name', '') if 'repository' in pr else repo or '',
                'url': pr.get('html_url', '')
            })
        return prs
    
    def get_context(self, query: str) -> Dict[str, Any]:
        """Get comprehensive GitHub context based on query."""
        context = {
            'source': 'GitHub',
            'repos': [],
            'issues': [],
            'prs': []
        }
        
        # Extract repo name from query if mentioned
        repo_match = re.search(r'repo[sitory]*[: ]+(\w+)', query, re.IGNORECASE)
        repo = repo_match.group(1) if repo_match else None
        
        # Fetch relevant data
        if 'repo' in query.lower() or 'repository' in query.lower():
            context['repos'] = self.get_user_repos(limit=5)
        
        if 'issue' in query.lower():
            context['issues'] = self.get_recent_issues(repo=repo, limit=5)
        
        if 'pr' in query.lower() or 'pull request' in query.lower():
            context['prs'] = self.get_recent_prs(repo=repo, limit=5)
        
        # If no specific keyword, fetch general context
        if not context['repos'] and not context['issues'] and not context['prs']:
            context['repos'] = self.get_user_repos(limit=3)
            context['issues'] = self.get_recent_issues(limit=3)
        
        return context


class WeatherContextFetcher:
    """Fetches weather context from OpenWeatherMap API."""
    
    def __init__(self, api_key: Optional[str] = None, city: Optional[str] = None):
        self.api_key = api_key or os.getenv('WEATHER_API_KEY', '')
        self.city = city or os.getenv('WEATHER_CITY', 'New York')
        self.base_url = 'https://api.openweathermap.org/data/2.5'
    
    def _make_request(self, endpoint: str) -> Optional[Dict]:
        """Make request to Weather API."""
        if not self.api_key:
            return None
        
        url = f"{self.base_url}{endpoint}&appid={self.api_key}"
        
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Weather API error: {e}")
            return None
    
    def get_current_weather(self) -> Optional[Dict]:
        """Get current weather for configured city."""
        data = self._make_request(f'/weather?q={urllib.parse.quote(self.city)}&units=metric')
        if not data:
            return None
        
        return {
            'city': data.get('name', self.city),
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'wind_speed': data.get('wind', {}).get('speed', 0)
        }
    
    def get_forecast(self, days: int = 1) -> List[Dict]:
        """Get weather forecast."""
        data = self._make_request(f'/forecast?q={urllib.parse.quote(self.city)}&units=metric&cnt={days * 8}')
        if not data or 'list' not in data:
            return []
        
        forecasts = []
        for item in data['list'][:days * 2]:  # Limit results
            forecasts.append({
                'time': datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M'),
                'temperature': round(item['main']['temp']),
                'description': item['weather'][0]['description'].title()
            })
        
        return forecasts
    
    def get_context(self, query: str) -> Dict[str, Any]:
        """Get weather context based on query."""
        context = {
            'source': 'Weather',
            'current': None,
            'forecast': []
        }
        
        # Check if forecast is requested
        needs_forecast = 'forecast' in query.lower() or 'tomorrow' in query.lower()
        
        context['current'] = self.get_current_weather()
        
        if needs_forecast:
            days = 1 if 'tomorrow' in query.lower() else 3
            context['forecast'] = self.get_forecast(days=days)
        
        return context


class TimeContextFetcher:
    """Provides time and date context."""
    
    def get_context(self, query: str) -> Dict[str, Any]:
        """Get time/date context."""
        now = datetime.now()
        
        context = {
            'source': 'Time/Date',
            'current_time': now.strftime('%Y-%m-%d %H:%M:%S'),
            'current_date': now.strftime('%A, %B %d, %Y'),
            'day_of_week': now.strftime('%A'),
            'time_of_day': self._get_time_of_day(now),
            'week_number': now.isocalendar()[1],
            'is_weekend': now.weekday() >= 5
        }
        
        # Add relative dates if mentioned
        if 'tomorrow' in query.lower():
            tomorrow = now + timedelta(days=1)
            context['tomorrow'] = tomorrow.strftime('%A, %B %d, %Y')
        
        if 'yesterday' in query.lower():
            yesterday = now - timedelta(days=1)
            context['yesterday'] = yesterday.strftime('%A, %B %d, %Y')
        
        return context
    
    def _get_time_of_day(self, dt: datetime) -> str:
        """Get time of day description."""
        hour = dt.hour
        if hour < 6:
            return 'Early Morning'
        elif hour < 12:
            return 'Morning'
        elif hour < 17:
            return 'Afternoon'
        elif hour < 21:
            return 'Evening'
        else:
            return 'Night'


class ContextAssembler:
    """Assembles and formats context from multiple sources."""
    
    def __init__(self):
        self.analyzer = ContextAnalyzer()
        self.github_fetcher = GitHubContextFetcher()
        self.weather_fetcher = WeatherContextFetcher()
        self.time_fetcher = TimeContextFetcher()
    
    def assemble_context(self, query: str) -> Dict[str, Any]:
        """Assemble context package based on query."""
        # Analyze what context is needed
        needs = self.analyzer.analyze(query)
        
        context_package = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'sources': [],
            'context': {}
        }
        
        # Fetch GitHub context
        if needs['github']:
            github_ctx = self.github_fetcher.get_context(query)
            if github_ctx.get('repos') or github_ctx.get('issues') or github_ctx.get('prs'):
                context_package['sources'].append('GitHub')
                context_package['context']['github'] = github_ctx
        
        # Fetch Weather context
        if needs['weather']:
            weather_ctx = self.weather_fetcher.get_context(query)
            if weather_ctx.get('current'):
                context_package['sources'].append('Weather')
                context_package['context']['weather'] = weather_ctx
        
        # Always include time context
        if needs['time'] or needs['always_fetch_time']:
            time_ctx = self.time_fetcher.get_context(query)
            context_package['sources'].append('Time/Date')
            context_package['context']['time'] = time_ctx
        
        return context_package
    
    def format_for_ai(self, context_package: Dict[str, Any]) -> str:
        """Format context package as a readable string for AI models."""
        lines = [
            "=" * 80,
            "CONTEXT PACKAGE FOR AI MODEL",
            "=" * 80,
            f"Query: {context_package['query']}",
            f"Timestamp: {context_package['timestamp']}",
            f"Data Sources: {', '.join(context_package['sources']) if context_package['sources'] else 'None'}",
            "",
        ]
        
        # Format GitHub context
        if 'github' in context_package['context']:
            github = context_package['context']['github']
            lines.append("--- GITHUB CONTEXT ---")
            
            if github.get('repos'):
                lines.append("\nRecent Repositories:")
                for repo in github['repos']:
                    lines.append(f"  • {repo['name']} ({repo['language']}) - {repo['stars']} stars")
                    if repo['description']:
                        lines.append(f"    {repo['description']}")
                    lines.append(f"    Updated: {repo['updated_at']}")
                    lines.append(f"    URL: {repo['url']}")
            
            if github.get('issues'):
                lines.append("\nOpen Issues:")
                for issue in github['issues']:
                    lines.append(f"  • #{issue['number']}: {issue['title']}")
                    lines.append(f"    Repo: {issue['repo']}")
                    lines.append(f"    URL: {issue['url']}")
            
            if github.get('prs'):
                lines.append("\nOpen Pull Requests:")
                for pr in github['prs']:
                    lines.append(f"  • #{pr['number']}: {pr['title']}")
                    lines.append(f"    Repo: {pr['repo']}")
                    lines.append(f"    URL: {pr['url']}")
            
            lines.append("")
        
        # Format Weather context
        if 'weather' in context_package['context']:
            weather = context_package['context']['weather']
            lines.append("--- WEATHER CONTEXT ---")
            
            if weather.get('current'):
                curr = weather['current']
                lines.append(f"\nCurrent Weather in {curr['city']}:")
                lines.append(f"  Temperature: {curr['temperature']}°C (feels like {curr['feels_like']}°C)")
                lines.append(f"  Conditions: {curr['description']}")
                lines.append(f"  Humidity: {curr['humidity']}%")
                lines.append(f"  Wind Speed: {curr['wind_speed']} m/s")
            
            if weather.get('forecast'):
                lines.append("\nForecast:")
                for fc in weather['forecast']:
                    lines.append(f"  • {fc['time']}: {fc['temperature']}°C, {fc['description']}")
            
            lines.append("")
        
        # Format Time context
        if 'time' in context_package['context']:
            time_ctx = context_package['context']['time']
            lines.append("--- TIME/DATE CONTEXT ---")
            lines.append(f"\nCurrent Date: {time_ctx['current_date']}")
            lines.append(f"Current Time: {time_ctx['current_time']}")
            lines.append(f"Day of Week: {time_ctx['day_of_week']}")
            lines.append(f"Time of Day: {time_ctx['time_of_day']}")
            lines.append(f"Week Number: {time_ctx['week_number']}")
            lines.append(f"Is Weekend: {time_ctx['is_weekend']}")
            
            if 'tomorrow' in time_ctx:
                lines.append(f"Tomorrow: {time_ctx['tomorrow']}")
            if 'yesterday' in time_ctx:
                lines.append(f"Yesterday: {time_ctx['yesterday']}")
            
            lines.append("")
        
        lines.append("=" * 80)
        lines.append("END OF CONTEXT PACKAGE")
        lines.append("=" * 80)
        
        return "\n".join(lines)


class MCPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for MCP server."""
    
    def __init__(self, *args, **kwargs):
        self.assembler = ContextAssembler()
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        """Handle POST requests with user queries."""
        if self.path != '/query':
            self._send_error(404, "Not Found")
            return
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            query = data.get('query', '')
            if not query:
                self._send_error(400, "Missing 'query' field")
                return
            
            # Assemble context
            context_package = self.assembler.assemble_context(query)
            formatted_context = self.assembler.format_for_ai(context_package)
            
            # Prepare response
            response = {
                'success': True,
                'query': query,
                'context_package': context_package,
                'formatted_context': formatted_context,
                'sources_used': context_package['sources']
            }
            
            self._send_json_response(200, response)
            
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
        except Exception as e:
            self._send_error(500, f"Internal Server Error: {str(e)}")
    
    def do_GET(self):
        """Handle GET requests for health check."""
        if self.path == '/health':
            self._send_json_response(200, {'status': 'healthy', 'service': 'MCP Developer Intelligence Server'})
        elif self.path == '/':
            self._send_json_response(200, {
                'service': 'Developer Intelligence MCP Server',
                'version': '1.0.0',
                'endpoints': {
                    'POST /query': 'Submit a query to get context',
                    'GET /health': 'Health check endpoint'
                }
            })
        else:
            self._send_error(404, "Not Found")
    
    def _send_json_response(self, status_code: int, data: Dict):
        """Send JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def _send_error(self, status_code: int, message: str):
        """Send error response."""
        self._send_json_response(status_code, {'success': False, 'error': message})
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def run_server(port: int = 8000):
    """Run the MCP server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MCPRequestHandler)
    print(f"🚀 Developer Intelligence MCP Server running on http://localhost:{port}")
    print(f" Health check: http://localhost:{port}/health")
    print(f" Submit queries to: http://localhost:{port}/query")
    print("\nPress Ctrl+C to stop the server.")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n Shutting down server...")
        httpd.shutdown()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)

