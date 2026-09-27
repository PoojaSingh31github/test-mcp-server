"""Tests for all 10 MCP Resources."""

import json
import pytest
from src.resources import (
    get_about_resource,
    get_config_resource,
    get_users_resource,
    get_products_resource,
    get_orders_resource,
    get_readme_resource,
    get_docs_api_resource,
    get_countries_resource,
    get_languages_resource,
    get_faq_resource,
)
from src.server import create_server


def test_get_about_resource():
    about = get_about_resource()
    assert "Math Text MCP Server" in about
    assert "1.0.0" in about
    assert "Available MCP Tools (10)" in about
    assert "Available MCP Resources (10)" in about
    assert "Available MCP Prompts (10)" in about


def test_get_config_resource():
    config_json = get_config_resource()
    config = json.loads(config_json)
    assert config["app_name"] == "Math Text MCP Server"
    assert config["version"] == "1.0.0"
    assert "capabilities" in config
    assert config["capabilities"]["tools_count"] == 10
    assert config["capabilities"]["resources_count"] == 10
    assert config["capabilities"]["prompts_count"] == 10
    # Ensure no secrets leaked
    assert "secret" not in config_json.lower()
    assert "password" not in config_json.lower()
    assert "token" not in config_json.lower()


def test_get_users_resource():
    users_json = get_users_resource()
    users = json.loads(users_json)
    assert isinstance(users, list)
    assert len(users) >= 5
    assert any(u["name"] == "Alice Johnson" for u in users)
    assert all("id" in u and "email" in u and "role" in u for u in users)


def test_get_products_resource():
    products_json = get_products_resource()
    products = json.loads(products_json)
    assert isinstance(products, list)
    assert len(products) >= 5
    assert any(p["name"] == "Cloud AI Gateway" for p in products)
    assert all("id" in p and "price" in p and "sku" in p for p in products)


def test_get_orders_resource():
    orders_json = get_orders_resource()
    orders = json.loads(orders_json)
    assert isinstance(orders, list)
    assert len(orders) >= 3
    assert any(o["order_number"] == "ORD-2024-5001" for o in orders)
    assert all("items" in o and "total_amount" in o for o in orders)


def test_get_readme_resource():
    readme = get_readme_resource()
    assert isinstance(readme, str)
    assert len(readme) > 0


def test_get_docs_api_resource():
    docs_json = get_docs_api_resource()
    docs = json.loads(docs_json)
    assert "server" in docs
    assert "tools" in docs and len(docs["tools"]) == 10
    assert "resources" in docs and len(docs["resources"]) == 10
    assert "prompts" in docs and len(docs["prompts"]) == 10


def test_get_countries_resource():
    countries_json = get_countries_resource()
    countries = json.loads(countries_json)
    assert isinstance(countries, list)
    assert "India" in countries
    assert "United States" in countries
    assert "United Kingdom" in countries
    assert "Canada" in countries
    assert "Australia" in countries
    assert "Germany" in countries


def test_get_languages_resource():
    languages_json = get_languages_resource()
    languages = json.loads(languages_json)
    assert isinstance(languages, list)
    assert "English" in languages
    assert "Hindi" in languages
    assert "Spanish" in languages
    assert "French" in languages
    assert "German" in languages


def test_get_faq_resource():
    faq_json = get_faq_resource()
    faqs = json.loads(faq_json)
    assert isinstance(faqs, list)
    assert len(faqs) >= 5
    assert all("question" in f and "answer" in f for f in faqs)


# --- Integration Test with MCPServer.read_resource ---


@pytest.mark.asyncio
async def test_mcp_server_read_resource_all():
    server = create_server()
    expected_uris = [
        "app://about",
        "app://config",
        "app://users",
        "app://products",
        "app://orders",
        "file://readme",
        "docs://api",
        "data://countries",
        "data://languages",
        "app://faq",
    ]

    for uri in expected_uris:
        contents = await server.read_resource(uri)
        assert contents is not None
        assert len(contents) > 0
        content_item = contents[0]
        # Content item can be TextResourceContents or ReadResourceContents with content/text
        text_content = getattr(content_item, "content", getattr(content_item, "text", None))
        assert text_content is not None and len(str(text_content)) > 0
