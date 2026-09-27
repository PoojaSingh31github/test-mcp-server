"""Math Text MCP Server - Main Server Module."""

import logging
import os
import sys
from typing import Optional

from mcp.server.mcpserver import MCPServer
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

from src.prompts import register_prompts
from src.resources import register_resources
from src.tools import register_tools

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("math-text-mcp-server")


def create_server() -> MCPServer:
    app_version = os.getenv("APP_VERSION", "1.0.0")

    server = MCPServer(
        name="math-text-mcp-server",
        version=app_version,
        description=(
            "Production-ready MCP Server providing math and text tools, "
            "resources, and prompts."
        ),
    )

    register_tools(server)
    register_resources(server)
    register_prompts(server)

    # Root endpoint - Browser me direct 404 Not Found aane se rokega
    @server.custom_route("/", methods=["GET", "HEAD"])
    async def root_view(request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "status": "healthy",
                "service": "math-text-mcp-server",
                "endpoints": {
                    "sse": "/sse",
                    "messages": "/messages",
                    "health": "/health",
                },
            }
        )

    # Health check route
    @server.custom_route("/health", methods=["GET"])
    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "status": "healthy",
                "service": "math-text-mcp-server",
                "version": app_version,
            }
        )

    return server


def create_app(server: Optional[MCPServer] = None) -> Starlette:
    if server is None:
        server = create_server()

    # Agent Nexus compatible SSE transport
    app = server.sse_app(sse_path="/sse", message_path="/messages")

    # CORS allow sabhi external tools ke liye
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    # Render ka injected PORT environment variable padhega
    port = int(os.getenv("PORT", "8000"))

    logger.info("Starting MCP Server on %s:%d", host, port)
    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()