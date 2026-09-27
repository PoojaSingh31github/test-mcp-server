# Math Text MCP Server

Production-ready Model Context Protocol (MCP) server built with **Python 3.13+**, **uv**, and the official **MCP SDK (v2.x)**.

Provides mathematical calculations, unit conversions, string processing tools, structured data and documentation resources, and LLM prompt templates over a standardized **Streamable HTTP transport**.

---

## Features

- **10 MCP Tools**: Mathematical calculations, temperature conversions, unit conversions, and text transformations.
- **10 MCP Resources**: Application metadata, configuration, sample datasets (users, products, orders, countries, languages), API documentation, FAQs, and README.
- **10 MCP Prompts**: Specialized LLM generation templates for summarization, translation, code review, test case generation, SQL query generation, error diagnostics, and more.
- **Streamable HTTP Transport**: Modern HTTP transport (`/mcp`) compatible with remote MCP clients and MCP registries.
- **Health Check Endpoint**: `GET /health` returning standard service status for container orchestrators and load balancers.
- **Production Containerization**: Multi-stage, non-root Docker deployment.

---

## Requirements

- **Python**: `>= 3.13`
- **uv**: `>= 0.4.0` (for environment and dependency management)
- **Docker**: (Optional, for containerized deployment)

---

## Local Setup

### 1. Clone or Navigate to the Project

```bash
cd try-projects/mcp
```

### 2. Install Dependencies with `uv`

```bash
uv sync
```

### 3. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Default configuration in `.env`:
```env
APP_NAME=Math Text MCP Server
APP_VERSION=1.0.0
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000
```

---

## Running Locally

Start the MCP server using `uv`:

```bash
uv run python -m src.server
```

Or using the CLI entrypoint:

```bash
uv run math-text-mcp-server
```

### Server Endpoints

| Endpoint | Protocol / Method | Description |
| :--- | :--- | :--- |
| `http://localhost:8000/mcp` | MCP (Streamable HTTP) | Main MCP protocol endpoint for AI clients and registries |
| `http://localhost:8000/health` | HTTP `GET` | Health check endpoint returning JSON status |

#### Example Health Check Request

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "math-text-mcp-server",
  "version": "1.0.0"
}
```

---

## Testing

Run the full test suite with `pytest`:

```bash
uv run pytest
```

Run with verbose output and coverage:

```bash
uv run pytest -v
```

---

## Docker Deployment

### 1. Build the Docker Image

```bash
docker build -t math-text-mcp-server .
```

### 2. Run the Container

```bash
docker run -d --name math-text-mcp -p 8000:8000 --env-file .env.example math-text-mcp-server
```

### 3. Test Container Health

```bash
curl http://localhost:8000/health
```

---

## MCP Capabilities Reference

### 1. MCP Tools (10)

| Tool Name | Parameters | Return Type | Description & Example |
| :--- | :--- | :--- | :--- |
| `add_numbers` | `a: float, b: float` | `float` | Adds two numbers (`10 + 20 -> 30`) |
| `subtract_numbers` | `a: float, b: float` | `float` | Subtracts `b` from `a` (`20 - 5 -> 15`) |
| `multiply_numbers` | `a: float, b: float` | `float` | Multiplies two numbers (`5 * 6 -> 30`) |
| `celsius_to_fahrenheit` | `celsius: float` | `float` | Converts Celsius to Fahrenheit (`25°C -> 77°F`) |
| `fahrenheit_to_celsius` | `fahrenheit: float` | `float` | Converts Fahrenheit to Celsius (`77°F -> 25°C`) |
| `km_to_miles` | `km: float` | `float` | Converts kilometers to miles (`10 km -> 6.21371 mi`) |
| `kg_to_pounds` | `kg: float` | `float` | Converts kilograms to pounds (`10 kg -> 22.0462 lb`) |
| `uppercase_text` | `text: str` | `str` | Converts string to uppercase (`"hello" -> "HELLO"`) |
| `reverse_text` | `text: str` | `str` | Reverses string characters (`"hello" -> "olleh"`) |
| `count_words` | `text: str` | `int` | Counts whitespace-delimited words (`"hello how are you" -> 4`) |

### 2. MCP Resources (10)

| URI | MIME Type | Description |
| :--- | :--- | :--- |
| `app://about` | `text/plain` | Server metadata, capabilities catalog, and purpose |
| `app://config` | `application/json` | Safe runtime configuration (no secrets exposed) |
| `app://users` | `application/json` | Sample user accounts dataset (`data/users.json`) |
| `app://products` | `application/json` | Sample product catalog dataset (`data/products.json`) |
| `app://orders` | `application/json` | Sample customer orders dataset (`data/orders.json`) |
| `file://readme` | `text/markdown` | Server documentation and README contents |
| `docs://api` | `application/json` | Detailed MCP capability schema and API reference |
| `data://countries` | `application/json` | Global country reference list |
| `data://languages` | `application/json` | Supported languages reference list |
| `app://faq` | `application/json` | Frequently asked questions and connection guide |

### 3. MCP Prompts (10)

| Prompt Name | Arguments | Description |
| :--- | :--- | :--- |
| `summarize_text` | `text: str` | Prompt template for concise, structured text summarization |
| `translate_text` | `text: str, language: str` | Prompt template for high-accuracy language translation |
| `explain_code` | `code: str` | Beginner-friendly step-by-step code explanation prompt |
| `review_code` | `code: str` | Thorough code audit (bugs, security, performance, quality) |
| `generate_email` | `purpose: str, recipient: str, details: str` | Professional business email drafting prompt |
| `generate_blog` | `topic: str` | Structured, SEO-friendly blog article generation prompt |
| `fix_grammar` | `text: str` | Grammar and syntax correction preserving original voice |
| `create_test_cases` | `code: str` | Comprehensive test suite generator (happy, edge, invalid) |
| `explain_error` | `error: str` | Diagnostic prompt for error traces and resolution steps |
| `generate_sql` | `requirement: str` | SQL query generator with explanation and schema assumptions |

---

## Deployment & Registry Registration

When deployed to production (e.g. Kubernetes, Cloud Run, AWS ECS, or Virtual Machine behind a reverse proxy):

1. Expose the MCP endpoint:
   ```text
   https://<your-domain>/mcp
   ```
2. The health check endpoint is available at:
   ```text
   https://<your-domain>/health
   ```
3. Register the server in your external MCP registry or control plane (such as **Agent Nexus**) with:
   - **Name**: `math-text-mcp-server`
   - **Description**: `Production-ready MCP Server providing math/text tools, datasets, and prompts`
   - **Version**: `1.0.0`
   - **Transport**: `Streamable HTTP`
   - **MCP Protocol Endpoint**: `https://<your-domain>/mcp`
   - **Health Check URL**: `https://<your-domain>/health`
