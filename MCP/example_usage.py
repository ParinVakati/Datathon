"""
Simple example showing how to use the Developer Intelligence MCP Server
"""

import requests
import json


def example_usage():
    """Demonstrate basic usage of the MCP server."""
    
    base_url = 'http://localhost:25000'
    
    # Example 1: Simple time query
    print("Example 1: Time Query")
    print("-" * 60)
    response = requests.post(
        f'{base_url}/query',
        json={'query': 'What day is it today?'}
    )
    if response.status_code == 200:
        result = response.json()
        print(result['formatted_context'])
    print("\n")
    
    # Example 2: Weather query
    print("Example 2: Weather Query")
    print("-" * 60)
    response = requests.post(
        f'{base_url}/query',
        json={'query': "What's the weather like today?"}
    )
    if response.status_code == 200:
        result = response.json()
        print(result['formatted_context'])
    print("\n")
    
    # Example 3: GitHub query (requires API keys)
    print("Example 3: GitHub Query")
    print("-" * 60)
    response = requests.post(
        f'{base_url}/query',
        json={'query': 'What are my recent GitHub repositories?'}
    )
    if response.status_code == 200:
        result = response.json()
        print(result['formatted_context'])
    print("\n")
    
    # Example 4: Combined query
    print("Example 4: Combined Query")
    print("-" * 60)
    response = requests.post(
        f'{base_url}/query',
        json={'query': 'What day is it and what is the weather forecast for tomorrow?'}
    )
    if response.status_code == 200:
        result = response.json()
        print(result['formatted_context'])


if __name__ == '__main__':
    try:
        example_usage()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server.")
        print("Please make sure the server is running:")
        print("  python server.py")
    except Exception as e:
        print(f"❌ Error: {e}")

