"""
Test client for Developer Intelligence MCP Server
Demonstrates various query types and server capabilities.
"""

import json
import requests
import sys
from typing import Dict, Any


def test_health_check(base_url: str = 'http://localhost:8000'):
    """Test the health check endpoint."""
    print("\n" + "="*80)
    print("TEST 1: Health Check")
    print("="*80)
    
    try:
        response = requests.get(f'{base_url}/health', timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print(" ERROR: Could not connect to server. Is it running?")
        return False
    except Exception as e:
        print(f" ERROR: {e}")
        return False


def test_query(base_url: str, query: str, description: str):
    """Test a query and display results."""
    print("\n" + "="*80)
    print(f"TEST: {description}")
    print("="*80)
    print(f"Query: {query}")
    print("-"*80)
    
    try:
        response = requests.post(
            f'{base_url}/query',
            json={'query': query},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f" Success: {data.get('success', False)}")
            print(f" Sources Used: {', '.join(data.get('sources_used', []))}")
            print("\n" + "-"*80)
            print("FORMATTED CONTEXT:")
            print("-"*80)
            print(data.get('formatted_context', 'No formatted context'))
            print("\n" + "-"*80)
            print("STRUCTURED CONTEXT (JSON):")
            print("-"*80)
            print(json.dumps(data.get('context_package', {}), indent=2))
            return True
        else:
            print(f" Error: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(" ERROR: Could not connect to server. Is it running?")
        return False
    except Exception as e:
        print(f" ERROR: {e}")
        return False


def run_all_tests(base_url: str = 'http://localhost:8000'):
    """Run all test queries."""
    print("\n" + ""*40)
    print("DEVELOPER INTELLIGENCE MCP SERVER - TEST SUITE")
    print(""*40)
    
    # Test 1: Health check
    if not test_health_check(base_url):
        print("\n Server is not running. Please start the server first:")
        print("   python server.py")
        return
    
    # Test 2: Time/Date query
    test_query(
        base_url,
        "What day is it today?",
        "Time/Date Context"
    )
    
    # Test 3: Weather query
    test_query(
        base_url,
        "What's the weather like today?",
        "Weather Context"
    )
    
    # Test 4: GitHub query (if configured)
    test_query(
        base_url,
        "What are my recent GitHub repositories?",
        "GitHub Context - Repositories"
    )
    
    # Test 5: Combined query
    test_query(
        base_url,
        "What's the weather forecast for tomorrow? Also, what day is it?",
        "Combined Context - Weather + Time"
    )
    
    # Test 6: GitHub issues query
    test_query(
        base_url,
        "Show me my open GitHub issues",
        "GitHub Context - Issues"
    )
    
    # Test 7: Weekend check
    test_query(
        base_url,
        "Is it a weekend? What time is it?",
        "Time Context - Weekend Check"
    )
    
    print("\n" + "="*80)
    print(" TEST SUITE COMPLETE")
    print("="*80)
    print("\nNote: Some tests may show limited results if API keys are not configured.")
    print("To get full functionality:")
    print("  - Set GITHUB_TOKEN and GITHUB_USERNAME for GitHub features")
    print("  - Set WEATHER_API_KEY for weather features")


if __name__ == '__main__':
    base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8000'
    run_all_tests(base_url)

