"""Integration tests for Server capabilities, HTTP endpoints, and health check."""

import pytest
from starlette.testclient import TestClient
from src.server import create_server, create_app


@pytest.mark.asyncio
async def test_server_capability_counts():
    """Verify that the MCP server exposes exactly 10 tools, 10 resources, and 10 prompts."""
    server = create_server()

    tools = await server.list_tools()
    assert len(tools) == 10, f"Expected 10 tools, got {len(tools)}: {[t.name for t in tools]}"

    resources = await server.list_resources()
    assert len(resources) == 10, f"Expected 10 resources, got {len(resources)}: {[str(r.uri) for r in resources]}"

    prompts = await server.list_prompts()
    assert len(prompts) == 10, f"Expected 10 prompts, got {len(prompts)}: {[p.name for p in prompts]}"


def test_health_endpoint():
    """Verify that the GET /health endpoint returns 200 OK and expected JSON schema."""
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "math-text-mcp-server"
        assert data["version"] == "1.0.0"


def test_streamable_http_routes():
    """Verify that the Starlette application mounts the /mcp and /health routes."""
    app = create_app()
    route_paths = [r.path for r in app.routes if hasattr(r, "path")]
    assert "/mcp" in route_paths
    assert "/health" in route_paths
