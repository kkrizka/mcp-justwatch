# MCP JustWatch Server

A Model Context Protocol (MCP) server built to provide access to JustWatch streaming availability data. Search for movies and TV shows and find out where they're available to stream across different platforms and countries.

## Features

- **Search Content**: Search for movies and TV shows by title with detailed metadata
- **Streaming Availability**: Get comprehensive information about where content is available to stream
- **Multi-Country Support**: Query streaming availability across multiple countries simultaneously
- **Detailed Information**: Access IMDb/TMDb scores, genres, runtime, release dates, and more
- **Offer Details**: Get pricing, quality (HD/4K), and direct URLs to streaming platforms

## Technology Stack

This server is built using:
- **[FastMCP](https://github.com/jlowin/fastmcp)**: A modern, decorator-based framework for building MCP servers with minimal boilerplate
- **[simple-justwatch-python-api](https://github.com/Electronic-Mango/simple-justwatch-python-api)**: GraphQL-based wrapper for the JustWatch API

## Installation

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### From Release

Skip to "As an MCP Server" as a section to automatically download the package inside common MCP clients.

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

### For Development

Install with development dependencies:
```bash
pip install -e ".[dev]"
```

## Usage

### As an MCP Server

This server is designed to be used with MCP clients. Add it to your MCP client configuration:

#### Claude Desktop Configuration

Add to your `claude_desktop_config.json` to automatically download the package at the start of the session using `uvx`.

```json
{
  "mcpServers": {
    "justwatch": {
      "command": "uvx",
      "args": ["mcp-justwatch", "python", "-m", "mcp_justwatch.server"]
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This project uses the [simple-justwatch-python-api](https://github.com/Electronic-Mango/simple-justwatch-python-api), an unofficial JustWatch API wrapper. This API is in no way affiliated, associated, authorized, endorsed by, or in any way officially connected with JustWatch. This is an independent and unofficial project. Use at your own risk and discretion.
