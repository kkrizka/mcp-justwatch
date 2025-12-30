# MCP JustWatch Server

A Model Context Protocol (MCP) server built to provide access to JustWatch streaming availability data. Search for movies and TV shows and find out where they're available to stream across different platforms and countries.

## Features

- **Search Content**: Search for movies and TV shows by title with detailed metadata
- **Streaming Availability**: Get comprehensive information about where content is available to stream
- **Multi-Country Support**: Query streaming availability across multiple countries simultaneously
- **Detailed Information**: Access IMDb/TMDb scores, genres, runtime, release dates, and more
- **Offer Details**: Get pricing, quality (HD/4K), and direct URLs to streaming platforms

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### From Source

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-justwatch
```

2. Install the package:
```bash
pip install -e .
```

Or using `uv`:
```bash
uv pip install -e .
```

### For Development

Install with development dependencies:
```bash
pip install -e ".[dev]"
```

## Usage

### As an MCP Server

This server is designed to be used with MCP clients. Add it to your MCP client configuration:

#### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "justwatch": {
      "command": "python",
      "args": ["-m", "mcp_justwatch.server"]
    }
  }
}
```

Or if installed in a virtual environment:

```json
{
  "mcpServers": {
    "justwatch": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "mcp_justwatch.server"]
    }
  }
}
```

#### Other MCP Hosts

See the `mcphost-config.yaml` example file for configuration with other MCP hosts.

## Available Tools

### search_content

Search for movies and TV shows on JustWatch with detailed information including streaming availability, scores, and metadata.

**Parameters:**
- `query` (required): The title to search for
- `country` (optional): Two-letter ISO 3166-1 alpha-2 country code (default: "US")
- `language` (optional): ISO 639-1 language code (default: "en")
- `count` (optional): Maximum number of results to return, 1-20 (default: 5)
- `best_only` (optional): Return only best quality offers per platform (default: true)

**Example:**
```json
{
  "query": "The Matrix",
  "country": "US",
  "language": "en",
  "count": 5,
  "best_only": true
}
```

**Returns:** List of matching entries with title, node ID, type, release year, genres, scores, runtime, and streaming offers.

### get_details

Get detailed information about a specific movie or TV show using its JustWatch node ID (obtained from search results).

**Parameters:**
- `node_id` (required): The JustWatch node ID from search results
- `country` (optional): Two-letter ISO 3166-1 alpha-2 country code (default: "US")
- `language` (optional): ISO 639-1 language code (default: "en")
- `best_only` (optional): Return only best quality offers per platform (default: true)

**Example:**
```json
{
  "node_id": "tm12345",
  "country": "GB",
  "language": "en",
  "best_only": true
}
```

**Returns:** Detailed information for the specified content including all metadata and streaming offers.

### get_offers_for_countries

Get streaming offers for a specific content across multiple countries simultaneously.

**Parameters:**
- `node_id` (required): The JustWatch node ID from search results
- `countries` (required): Array of two-letter country codes (e.g., ["US", "GB", "DE"])
- `language` (optional): ISO 639-1 language code (default: "en")
- `best_only` (optional): Return only best quality offers per platform (default: true)

**Example:**
```json
{
  "node_id": "tm12345",
  "countries": ["US", "GB", "CA", "AU"],
  "language": "en",
  "best_only": true
}
```

**Returns:** Streaming offers organized by country, showing availability, pricing, quality, and direct URLs.

## Supported Locales

This API uses ISO standard codes:
- **Countries**: ISO 3166-1 alpha-2 (2-letter, uppercase) - e.g., `US`, `GB`, `DE`, `FR`, `ES`, `IT`, `CA`, `AU`, `JP`
- **Languages**: ISO 639-1 (usually 2-letter, lowercase) - e.g., `en`, `es`, `fr`, `de`, `ja`
- **Country-specific languages**: Supported - e.g., `es-MX` for Mexican Spanish (country part must be uppercase)

Common country codes:
- `US` - United States
- `GB` - United Kingdom  
- `DE` - Germany
- `FR` - France
- `ES` - Spain
- `IT` - Italy
- `CA` - Canada
- `AU` - Australia
- `JP` - Japan

See [JustWatch REST API documentation](https://apis.justwatch.com/docs/api/#tips) for a complete list of supported locales.

## Examples

The `examples/` directory contains example Python scripts demonstrating direct usage of the `simple-justwatch-python-api`:

```bash
python examples/example_usage.py
```

This shows how to:
- Search for content with various parameters
- Get detailed information using node IDs
- Query offers across multiple countries
- Use different languages and locales

These examples help understand what data the MCP server returns when tools are called.

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

Format code with Black:
```bash
black src tests
```

Lint with Ruff:
```bash
ruff check src tests
```

## Technology Stack

This server is built using:
- **[FastMCP](https://github.com/jlowin/fastmcp)**: A modern, decorator-based framework for building MCP servers with minimal boilerplate
- **[simple-justwatch-python-api](https://github.com/Electronic-Mango/simple-justwatch-python-api)**: GraphQL-based wrapper for the JustWatch API
- **Python 3.10+**: Modern Python with type hints

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This project uses the [simple-justwatch-python-api](https://github.com/Electronic-Mango/simple-justwatch-python-api), an unofficial JustWatch API wrapper. This API is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with JustWatch. This is an independent and unofficial project. Use at your own risk and discretion.
