"""Tests for all 10 MCP Prompts."""

import pytest
from src.prompts import (
    prompt_summarize_text,
    prompt_translate_text,
    prompt_explain_code,
    prompt_review_code,
    prompt_generate_email,
    prompt_generate_blog,
    prompt_fix_grammar,
    prompt_create_test_cases,
    prompt_explain_error,
    prompt_generate_sql,
)
from src.server import create_server


def test_prompt_summarize_text():
    res = prompt_summarize_text("Antigravity is a next-generation AI agent framework.")
    assert "Antigravity is a next-generation" in res
    assert "summary" in res.lower()


def test_prompt_translate_text():
    res = prompt_translate_text("Hello world", "Spanish")
    assert "Hello world" in res
    assert "Spanish" in res
    assert "translate" in res.lower()


def test_prompt_explain_code():
    res = prompt_explain_code("def add(a, b): return a + b")
    assert "def add(a, b)" in res
    assert "beginner" in res.lower() or "explain" in res.lower()


def test_prompt_review_code():
    res = prompt_review_code("eval(user_input)")
    assert "eval(user_input)" in res
    assert "Security" in res
    assert "Bugs" in res


def test_prompt_generate_email():
    res = prompt_generate_email(
        purpose="Project update",
        recipient="Jane Doe",
        details="Phase 1 is complete. Launch scheduled next Monday.",
    )
    assert "Jane Doe" in res
    assert "Project update" in res
    assert "Phase 1 is complete" in res


def test_prompt_generate_blog():
    res = prompt_generate_blog("Model Context Protocol in 2026")
    assert "Model Context Protocol in 2026" in res
    assert "blog" in res.lower()


def test_prompt_fix_grammar():
    res = prompt_fix_grammar("They is going to the market yesterday.")
    assert "They is going to the market yesterday." in res
    assert "grammar" in res.lower()


def test_prompt_create_test_cases():
    res = prompt_create_test_cases("def divide(a, b): return a / b")
    assert "def divide(a, b)" in res
    assert "Happy-Path" in res
    assert "Edge-Case" in res
    assert "Invalid-Input" in res


def test_prompt_explain_error():
    res = prompt_explain_error("ZeroDivisionError: division by zero")
    assert "ZeroDivisionError" in res
    assert "Meaning" in res
    assert "Root Causes" in res


def test_prompt_generate_sql():
    res = prompt_generate_sql("Find the top 5 customers with highest total order spend in 2024")
    assert "top 5 customers" in res
    assert "SQL" in res
    assert "Schema Assumptions" in res


def test_prompt_validation_empty_inputs():
    with pytest.raises(ValueError, match="cannot be empty"):
        prompt_summarize_text("")

    with pytest.raises(ValueError, match="cannot be empty"):
        prompt_translate_text("hello", "   ")

    with pytest.raises(TypeError):
        prompt_explain_code(123)  # type: ignore


# --- Integration Test with MCPServer.get_prompt ---


@pytest.mark.asyncio
async def test_mcp_server_get_prompt_all():
    server = create_server()

    # 1. summarize_text
    p = await server.get_prompt("summarize_text", {"text": "AI models process tokens."})
    assert len(p.messages) > 0

    # 2. translate_text
    p = await server.get_prompt("translate_text", {"text": "Good morning", "language": "French"})
    assert len(p.messages) > 0

    # 3. explain_code
    p = await server.get_prompt("explain_code", {"code": "print('hello')"})
    assert len(p.messages) > 0

    # 4. review_code
    p = await server.get_prompt("review_code", {"code": "x = input()"})
    assert len(p.messages) > 0

    # 5. generate_email
    p = await server.get_prompt(
        "generate_email",
        {"purpose": "Meeting invite", "recipient": "Team", "details": "Sync at 2pm."},
    )
    assert len(p.messages) > 0

    # 6. generate_blog
    p = await server.get_prompt("generate_blog", {"topic": "Async Python Best Practices"})
    assert len(p.messages) > 0

    # 7. fix_grammar
    p = await server.get_prompt("fix_grammar", {"text": "She have three cats."})
    assert len(p.messages) > 0

    # 8. create_test_cases
    p = await server.get_prompt("create_test_cases", {"code": "def square(x): return x * x"})
    assert len(p.messages) > 0

    # 9. explain_error
    p = await server.get_prompt("explain_error", {"error": "KeyError: 'user_id'"})
    assert len(p.messages) > 0

    # 10. generate_sql
    p = await server.get_prompt("generate_sql", {"requirement": "Select active users"})
    assert len(p.messages) > 0
