"""Math Text MCP Server - Main Server Module.

Initializes the MCP server, registers tools, resources, prompts, health check endpoint,
and configures the Streamable HTTP transport for local development and production deployment.
"""

import logging
import os
import sys
from typing import Optional

from mcp.server.mcpserver import MCPServer
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
import uvicorn

from src.prompts import register_prompts
from src.resources import register_resources
from src.tools import register_tools

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("math-text-mcp-server")


def create_server() -> MCPServer:
    """Create and configure the singleton MCPServer instance."""
    app_name = os.getenv("APP_NAME", "Math Text MCP Server")
    app_version = os.getenv("APP_VERSION", "1.0.0")

    server = MCPServer(
        name="math-text-mcp-server",
        version=app_version,
        description=(
            "Production-ready MCP Server providing 10 math and text tools, "
            "10 data/documentation resources, and 10 LLM prompts."
        ),
    )

    # Register modular capabilities
    register_tools(server)
    register_resources(server)
    register_prompts(server)

    # Register health endpoint
    @server.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        """Health check endpoint for deployment monitoring and load balancers."""
        return JSONResponse(
            {
                "status": "healthy",
                "service": "math-text-mcp-server",
                "version": app_version,
            }
        )

    logger.info(
        "MCPServer '%s' (v%s) initialized with 10 tools, 10 resources, 10 prompts, and /health endpoint.",
        app_name,
        app_version,
    )
    return server


def create_app(server: Optional[MCPServer] = None) -> Starlette:
    """Create the Starlette application exposing the HTTP MCP endpoint and health check."""
    if server is None:
        server = create_server()
    return server.streamable_http_app(streamable_http_path="/mcp")


def main() -> None:
    """Entrypoint to run the MCP Server over HTTP."""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    env = os.getenv("ENVIRONMENT", "development")

    logger.info("Starting Math Text MCP Server on http://%s:%d (env: %s)...", host, port, env)
    logger.info("MCP protocol endpoint: http://%s:%d/mcp", host, port)
    logger.info("Health check endpoint: http://%s:%d/health", host, port)

    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
