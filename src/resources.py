"""MCP Resources for server information, configurations, datasets, and documentation."""

import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mcp.server.mcpserver import MCPServer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def _read_json_file(filename: str) -> str:
    """Safely read and format a JSON data file."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Data file '{filename}' was not found at {filepath}.")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, indent=2)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Data file '{filename}' contains invalid JSON: {exc}") from exc


def get_about_resource() -> str:
    """Return comprehensive server metadata and capability listing."""
    return """Math Text MCP Server
====================
Name: math-text-mcp-server
Description: Production-ready Python MCP Server providing math operations, unit conversions, text processing, data resources, and LLM prompts.
Version: 1.0.0
Purpose: High-performance, standardized Model Context Protocol (MCP) server for local development and remote registry deployments.

Available MCP Tools (10):
  1. add_numbers(a, b) - Add two numbers together
  2. subtract_numbers(a, b) - Subtract second number from first
  3. multiply_numbers(a, b) - Multiply two numbers together
  4. celsius_to_fahrenheit(celsius) - Convert Celsius to Fahrenheit
  5. fahrenheit_to_celsius(fahrenheit) - Convert Fahrenheit to Celsius
  6. km_to_miles(km) - Convert kilometers to miles
  7. kg_to_pounds(kg) - Convert kilograms to pounds
  8. uppercase_text(text) - Convert string to uppercase
  9. reverse_text(text) - Reverse character order of string
  10. count_words(text) - Count whitespace-delimited words

Available MCP Resources (10):
  1. app://about - Server overview, purpose, and capability catalog
  2. app://config - Safe runtime configuration parameters (JSON)
  3. app://users - Sample user records dataset (JSON)
  4. app://products - Sample product catalog dataset (JSON)
  5. app://orders - Sample customer order records dataset (JSON)
  6. file://readme - Complete server README documentation
  7. docs://api - Detailed API and MCP capability documentation
  8. data://countries - Global country reference dataset (JSON)
  9. data://languages - Supported languages reference dataset (JSON)
  10. app://faq - Frequently asked questions and troubleshooting (JSON)

Available MCP Prompts (10):
  1. summarize_text - Generate structured summary of text
  2. translate_text - Translate text into target language
  3. explain_code - Beginner-friendly code explanation
  4. review_code - Comprehensive code review and audit
  5. generate_email - Professional email drafting
  6. generate_blog - Structured blog article writing
  7. fix_grammar - Grammar correction with preservation of meaning
  8. create_test_cases - Unit test suite generation (happy, edge, invalid)
  9. explain_error - Error diagnostic and troubleshooting steps
  10. generate_sql - SQL query generation with assumptions and explanation
"""


def get_config_resource() -> str:
    """Return safe runtime configuration without secrets."""
    config_data = {
        "app_name": os.getenv("APP_NAME", "Math Text MCP Server"),
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", "8000")),
        "capabilities": {
            "tools_count": 10,
            "resources_count": 10,
            "prompts_count": 10,
        },
        "transport": {
            "type": "streamable_http",
            "mcp_endpoint": "/mcp",
            "health_endpoint": "/health",
        },
    }
    return json.dumps(config_data, indent=2)


def get_users_resource() -> str:
    """Return sample users dataset as JSON."""
    return _read_json_file("users.json")


def get_products_resource() -> str:
    """Return sample products dataset as JSON."""
    return _read_json_file("products.json")


def get_orders_resource() -> str:
    """Return sample orders dataset as JSON."""
    return _read_json_file("orders.json")


def get_readme_resource() -> str:
    """Return server README documentation."""
    readme_path = PROJECT_ROOT / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "# Math Text MCP Server\n\nProduction-ready MCP server for math and text operations."


def get_docs_api_resource() -> str:
    """Return API/MCP capability documentation describing available tools, resources, and prompts."""
    api_docs = {
        "server": {
            "name": "math-text-mcp-server",
            "version": "1.0.0",
            "mcp_spec": "2024-11-05 / Streamable HTTP",
        },
        "tools": [
            {"name": "add_numbers", "parameters": {"a": "number", "b": "number"}, "returns": "number", "example": "10 + 20 -> 30"},
            {"name": "subtract_numbers", "parameters": {"a": "number", "b": "number"}, "returns": "number", "example": "20 - 5 -> 15"},
            {"name": "multiply_numbers", "parameters": {"a": "number", "b": "number"}, "returns": "number", "example": "5 * 6 -> 30"},
            {"name": "celsius_to_fahrenheit", "parameters": {"celsius": "number"}, "returns": "number", "example": "25 C -> 77 F"},
            {"name": "fahrenheit_to_celsius", "parameters": {"fahrenheit": "number"}, "returns": "number", "example": "77 F -> 25 C"},
            {"name": "km_to_miles", "parameters": {"km": "number"}, "returns": "number", "example": "10 km -> ~6.21371 miles"},
            {"name": "kg_to_pounds", "parameters": {"kg": "number"}, "returns": "number", "example": "10 kg -> ~22.0462 lb"},
            {"name": "uppercase_text", "parameters": {"text": "string"}, "returns": "string", "example": "'hello' -> 'HELLO'"},
            {"name": "reverse_text", "parameters": {"text": "string"}, "returns": "string", "example": "'hello' -> 'olleh'"},
            {"name": "count_words", "parameters": {"text": "string"}, "returns": "integer", "example": "'hello how are you' -> 4"},
        ],
        "resources": [
            {"uri": "app://about", "mime_type": "text/plain", "description": "Server overview and metadata"},
            {"uri": "app://config", "mime_type": "application/json", "description": "Safe runtime configuration"},
            {"uri": "app://users", "mime_type": "application/json", "description": "Sample users dataset"},
            {"uri": "app://products", "mime_type": "application/json", "description": "Sample products catalog"},
            {"uri": "app://orders", "mime_type": "application/json", "description": "Sample customer orders"},
            {"uri": "file://readme", "mime_type": "text/markdown", "description": "README documentation"},
            {"uri": "docs://api", "mime_type": "application/json", "description": "API capability documentation"},
            {"uri": "data://countries", "mime_type": "application/json", "description": "Reference countries list"},
            {"uri": "data://languages", "mime_type": "application/json", "description": "Reference languages list"},
            {"uri": "app://faq", "mime_type": "application/json", "description": "Frequently asked questions"},
        ],
        "prompts": [
            {"name": "summarize_text", "arguments": ["text"], "description": "Text summarization prompt"},
            {"name": "translate_text", "arguments": ["text", "language"], "description": "Language translation prompt"},
            {"name": "explain_code", "arguments": ["code"], "description": "Beginner code explanation prompt"},
            {"name": "review_code", "arguments": ["code"], "description": "Comprehensive code review prompt"},
            {"name": "generate_email", "arguments": ["purpose", "recipient", "details"], "description": "Professional email prompt"},
            {"name": "generate_blog", "arguments": ["topic"], "description": "Blog article generation prompt"},
            {"name": "fix_grammar", "arguments": ["text"], "description": "Grammar correction prompt"},
            {"name": "create_test_cases", "arguments": ["code"], "description": "Unit test suite prompt"},
            {"name": "explain_error", "arguments": ["error"], "description": "Error explanation and fix prompt"},
            {"name": "generate_sql", "arguments": ["requirement"], "description": "SQL query generation prompt"},
        ],
    }
    return json.dumps(api_docs, indent=2)


def get_countries_resource() -> str:
    """Return country reference dataset as JSON."""
    countries = [
        "India",
        "United States",
        "United Kingdom",
        "Canada",
        "Australia",
        "Germany",
        "Japan",
        "France",
        "Brazil",
        "Singapore",
    ]
    return json.dumps(countries, indent=2)


def get_languages_resource() -> str:
    """Return language reference dataset as JSON."""
    languages = [
        "English",
        "Hindi",
        "Spanish",
        "French",
        "German",
        "Japanese",
        "Mandarin Chinese",
        "Portuguese",
        "Arabic",
        "Russian",
    ]
    return json.dumps(languages, indent=2)


def get_faq_resource() -> str:
    """Return frequently asked questions as JSON."""
    faqs = [
        {
            "question": "What is the Math Text MCP Server?",
            "answer": "It is a standardized Model Context Protocol (MCP) server providing math tools, unit conversion tools, text processing tools, sample data resources, and LLM prompt templates.",
        },
        {
            "question": "How do I connect an MCP client to this server?",
            "answer": "Configure your MCP client to connect via HTTP transport to http://localhost:8000/mcp (or your deployed remote domain URL).",
        },
        {
            "question": "Are the resources read-only?",
            "answer": "Yes, all MCP resources are strictly read-only and do not alter application state.",
        },
        {
            "question": "How can I verify server health?",
            "answer": "Send a GET request to http://localhost:8000/health to receive a 200 OK status with service metadata.",
        },
        {
            "question": "How do I run tests across all capabilities?",
            "answer": "Run 'uv run pytest' from the project root directory.",
        },
    ]
    return json.dumps(faqs, indent=2)


def register_resources(server: "MCPServer") -> None:
    """Register all 10 MCP resources on the server instance."""
    server.resource(
        "app://about",
        name="About Server",
        description="Provide comprehensive information about the MCP server and available capabilities.",
        mime_type="text/plain",
    )(get_about_resource)

    server.resource(
        "app://config",
        name="Application Configuration",
        description="Return safe application configuration parameters as JSON.",
        mime_type="application/json",
    )(get_config_resource)

    server.resource(
        "app://users",
        name="Users Dataset",
        description="Return a list of sample user accounts as JSON.",
        mime_type="application/json",
    )(get_users_resource)

    server.resource(
        "app://products",
        name="Products Dataset",
        description="Return a list of sample catalog products as JSON.",
        mime_type="application/json",
    )(get_products_resource)

    server.resource(
        "app://orders",
        name="Orders Dataset",
        description="Return a list of sample customer orders as JSON.",
        mime_type="application/json",
    )(get_orders_resource)

    server.resource(
        "file://readme",
        name="Project README",
        description="Return the server README documentation content.",
        mime_type="text/markdown",
    )(get_readme_resource)

    server.resource(
        "docs://api",
        name="API Documentation",
        description="Return API and MCP capability documentation describing available tools, resources, and prompts.",
        mime_type="application/json",
    )(get_docs_api_resource)

    server.resource(
        "data://countries",
        name="Countries Reference",
        description="Return a list of supported countries as JSON.",
        mime_type="application/json",
    )(get_countries_resource)

    server.resource(
        "data://languages",
        name="Languages Reference",
        description="Return a list of available languages as JSON.",
        mime_type="application/json",
    )(get_languages_resource)

    server.resource(
        "app://faq",
        name="Frequently Asked Questions",
        description="Return frequently asked questions about the server as JSON.",
        mime_type="application/json",
    )(get_faq_resource)
