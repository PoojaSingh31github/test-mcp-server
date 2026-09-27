"""Tests for all 10 MCP Tools."""

import math
import pytest
from src.tools import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    km_to_miles,
    kg_to_pounds,
    uppercase_text,
    reverse_text,
    count_words,
)
from src.server import create_server


# --- Unit Tests for Pure Tool Functions ---


def test_add_numbers_basic():
    assert add_numbers(10, 20) == 30
    assert add_numbers(0, 0) == 0
    assert add_numbers(-5, 15) == 10
    assert add_numbers(2.5, 3.5) == 6
    assert add_numbers(1.2, 3.4) == pytest.approx(4.6)


def test_subtract_numbers_basic():
    assert subtract_numbers(20, 5) == 15
    assert subtract_numbers(0, 10) == -10
    assert subtract_numbers(10.5, 0.5) == 10
    assert subtract_numbers(-5, -5) == 0


def test_multiply_numbers_basic():
    assert multiply_numbers(5, 6) == 30
    assert multiply_numbers(0, 100) == 0
    assert multiply_numbers(-4, 5) == -20
    assert multiply_numbers(2.5, 4) == 10


def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(25) == 77
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert celsius_to_fahrenheit(-40) == -40


def test_fahrenheit_to_celsius():
    assert fahrenheit_to_celsius(77) == 25
    assert fahrenheit_to_celsius(32) == 0
    assert fahrenheit_to_celsius(212) == 100
    assert fahrenheit_to_celsius(-40) == -40


def test_km_to_miles():
    assert km_to_miles(10) == pytest.approx(6.21371, rel=1e-4)
    assert km_to_miles(0) == 0
    assert km_to_miles(1) == 0.62137


def test_kg_to_pounds():
    assert kg_to_pounds(10) == pytest.approx(22.0462, rel=1e-4)
    assert kg_to_pounds(0) == 0
    assert kg_to_pounds(1) == 2.2046


def test_uppercase_text():
    assert uppercase_text("hello") == "HELLO"
    assert uppercase_text("Hello World!") == "HELLO WORLD!"
    assert uppercase_text("") == ""
    assert uppercase_text("123 abc") == "123 ABC"


def test_reverse_text():
    assert reverse_text("hello") == "olleh"
    assert reverse_text("racecar") == "racecar"
    assert reverse_text("") == ""
    assert reverse_text("12345") == "54321"


def test_count_words():
    assert count_words("hello how are you") == 4
    assert count_words("   single   ") == 1
    assert count_words("") == 0
    assert count_words("   \t\n  ") == 0
    assert count_words("one\ntwo\tthree  four") == 4


# --- Validation and Error Handling Tests ---


def test_numeric_validation_nan_and_inf():
    with pytest.raises(ValueError, match="must be a finite number"):
        add_numbers(float("nan"), 10)

    with pytest.raises(ValueError, match="must be a finite number"):
        multiply_numbers(10, float("inf"))

    with pytest.raises(TypeError):
        add_numbers("invalid", 10)  # type: ignore


def test_temperature_below_absolute_zero():
    with pytest.raises(ValueError, match="absolute zero"):
        celsius_to_fahrenheit(-300)

    with pytest.raises(ValueError, match="absolute zero"):
        fahrenheit_to_celsius(-500)


def test_negative_distance_and_weight():
    with pytest.raises(ValueError, match="cannot be negative"):
        km_to_miles(-5)

    with pytest.raises(ValueError, match="cannot be negative"):
        kg_to_pounds(-10)


def test_text_type_validation():
    with pytest.raises(TypeError, match="must be a string"):
        uppercase_text(123)  # type: ignore

    with pytest.raises(TypeError, match="must be a string"):
        reverse_text(None)  # type: ignore

    with pytest.raises(TypeError, match="must be a string"):
        count_words(456)  # type: ignore


# --- Integration Test with MCPServer.call_tool ---


@pytest.mark.asyncio
async def test_mcp_server_call_tool_all():
    server = create_server()

    # 1. add_numbers
    res = await server.call_tool("add_numbers", {"a": 10, "b": 20})
    assert not res.is_error
    assert res.structured_content == {"result": 30}

    # 2. subtract_numbers
    res = await server.call_tool("subtract_numbers", {"a": 20, "b": 5})
    assert not res.is_error
    assert res.structured_content == {"result": 15}

    # 3. multiply_numbers
    res = await server.call_tool("multiply_numbers", {"a": 5, "b": 6})
    assert not res.is_error
    assert res.structured_content == {"result": 30}

    # 4. celsius_to_fahrenheit
    res = await server.call_tool("celsius_to_fahrenheit", {"celsius": 25})
    assert not res.is_error
    assert res.structured_content == {"result": 77}

    # 5. fahrenheit_to_celsius
    res = await server.call_tool("fahrenheit_to_celsius", {"fahrenheit": 77})
    assert not res.is_error
    assert res.structured_content == {"result": 25}

    # 6. km_to_miles
    res = await server.call_tool("km_to_miles", {"km": 10})
    assert not res.is_error
    assert res.structured_content == {"result": 6.21371}

    # 7. kg_to_pounds
    res = await server.call_tool("kg_to_pounds", {"kg": 10})
    assert not res.is_error
    assert res.structured_content == {"result": 22.0462}

    # 8. uppercase_text
    res = await server.call_tool("uppercase_text", {"text": "hello"})
    assert not res.is_error
    assert res.structured_content == {"result": "HELLO"}

    # 9. reverse_text
    res = await server.call_tool("reverse_text", {"text": "hello"})
    assert not res.is_error
    assert res.structured_content == {"result": "olleh"}

    # 10. count_words
    res = await server.call_tool("count_words", {"text": "hello how are you"})
    assert not res.is_error
    assert res.structured_content == {"result": 4}
